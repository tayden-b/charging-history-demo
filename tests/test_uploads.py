from pathlib import Path

import pytest

from app.imports import MAX_UPLOAD_BYTES
from app.middleware import MAX_REQUEST_BYTES

ALICE = {"X-Demo-User": "alice"}
BOB = {"X-Demo-User": "bob"}
HEADER = "session_id,charged_at,energy_kwh,amount_usd\n"
ROW = "CHG-1003,2026-09-15T09:00:00Z,12.500,3.75\n"


def upload(client, text, headers=None):
    content = text.encode() if isinstance(text, str) else text
    return client.post(
        "/api/imports/csv",
        headers=headers if headers is not None else ALICE,
        files={"file": ("sessions.csv", content, "text/csv")},
    )


def test_upload_accepts_sample_and_updates_totals(client):
    sample = Path("examples/charging-upload.csv").read_bytes()
    response = upload(client, sample)
    assert response.status_code == 201
    assert response.json() == {"imported": 2, "session_ids": ["CHG-1003", "CHG-1004"]}
    assert client.get("/api/summary", headers=ALICE).json() == {
        "sessions": 4,
        "energy_wh": 75000,
        "amount_minor": 2250,
        "currency": "USD",
    }
    assert len(client.get("/api/charging-sessions", headers=BOB).json()) == 1


def test_upload_attributes_records_to_selected_identity(client):
    response = upload(client, HEADER + ROW, BOB)
    assert response.status_code == 201
    rows = client.get("/api/charging-sessions", headers=BOB).json()
    created = next(row for row in rows if row["id"] == "CHG-1003")
    assert created["owner_id"] == "bob"
    assert created["vehicle"] == "Demo vehicle B"


def test_duplicate_upload_is_rejected_without_writes(client):
    assert upload(client, HEADER + ROW).status_code == 201
    assert upload(client, HEADER + ROW).status_code == 409
    assert len(client.get("/api/charging-sessions", headers=ALICE).json()) == 3


def test_duplicate_rows_are_atomic(client):
    response = upload(client, HEADER + ROW + ROW)
    assert response.status_code == 409
    assert len(client.get("/api/charging-sessions", headers=ALICE).json()) == 2


def test_existing_id_cannot_be_overwritten(client):
    response = upload(client, HEADER + ROW.replace("CHG-1003", "CHG-2001"))
    assert response.status_code == 409
    assert client.get("/api/charging-sessions/CHG-2001", headers=BOB).json()["owner_id"] == "bob"


@pytest.mark.parametrize(
    "content",
    [
        b"",
        HEADER,
        HEADER + "bad-row\n",
        b"\xff",
        HEADER + ROW + "\x00",
        "owner_id," + HEADER + "alice," + ROW,
        HEADER + ROW.replace("3.75", "-1"),
        HEADER + ROW.replace("3.75", "NaN"),
        HEADER + ROW.replace("3.75", "Infinity"),
        HEADER + ROW.replace("3.75", "0.001"),
        HEADER + ROW.replace("12.500", "0.0001"),
        HEADER + ROW.replace("12.500", "1000001"),
        HEADER + ROW.replace("09:00:00Z", "09:00:00"),
        HEADER + ROW.replace("2026-09-15", "not-a-date"),
        HEADER + ROW.replace("CHG-1003", "invalid-id"),
        HEADER + ROW.replace("3.75\n", "3.75,extra\n"),
    ],
)
def test_invalid_upload_rejected_without_writes(client, content):
    assert upload(client, content).status_code == 422
    assert len(client.get("/api/charging-sessions", headers=ALICE).json()) == 2


def test_invalid_later_row_rolls_back_whole_import(client):
    response = upload(
        client, HEADER + ROW + ROW.replace("CHG-1003", "CHG-1004").replace("3.75", "bad")
    )
    assert response.status_code == 422
    assert client.app.state.store.get("CHG-1003") is None


def test_utf8_bom_crlf_and_timezone_are_supported(client):
    text = "\ufeff" + (HEADER + ROW.replace("09:00:00Z", "10:00:00+01:00")).replace("\n", "\r\n")
    assert upload(client, text).status_code == 201
    row = client.get("/api/charging-sessions/CHG-1003", headers=ALICE).json()
    assert row["charged_at"] == "2026-09-15T09:00:00Z"


def test_more_than_100_rows_rejected(client):
    rows = "".join(ROW.replace("CHG-1003", f"CHG-{3000 + i}") for i in range(101))
    assert upload(client, HEADER + rows).status_code == 422
    assert len(client.get("/api/charging-sessions", headers=ALICE).json()) == 2


def test_file_limit(client):
    assert upload(client, b"x" * (MAX_UPLOAD_BYTES + 1)).status_code == 413


def test_body_limit(client):
    assert upload(client, b"x" * (MAX_REQUEST_BYTES + 1)).status_code == 413


def test_upload_requires_identity(client):
    assert upload(client, HEADER + ROW, {}).status_code == 401


def test_missing_file(client):
    assert client.post("/api/imports/csv", headers=ALICE).status_code == 422


@pytest.mark.parametrize("value", ["-1", "invalid"])
def test_bad_content_length(client, value):
    response = client.post("/api/imports/csv", headers={**ALICE, "Content-Length": value})
    assert response.status_code == 400
