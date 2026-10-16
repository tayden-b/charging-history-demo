import pytest
from fastapi.testclient import TestClient

from app.main import create_app

ALICE = {"X-Demo-User": "alice"}
BOB = {"X-Demo-User": "bob"}


def test_health_and_demo_context(client):
    assert client.get("/health").json() == {"status": "ok", "mode": "synthetic-training-only"}
    context = client.get("/api/demo/context").json()
    assert {user["id"] for user in context["users"]} == {"alice", "bob"}
    assert "python-multipart" in context["dependencies"]


@pytest.mark.parametrize("headers", [{}, {"X-Demo-User": "unknown"}])
@pytest.mark.parametrize(
    "path", ["/api/charging-sessions", "/api/summary", "/api/charging-sessions/CHG-1001"]
)
def test_identity_required(client, headers, path):
    assert client.get(path, headers=headers).status_code == 401


def test_list_is_scoped_to_actor(client):
    alice = client.get("/api/charging-sessions", headers=ALICE).json()
    bob = client.get("/api/charging-sessions", headers=BOB).json()
    assert [row["id"] for row in alice] == ["CHG-1002", "CHG-1001"]
    assert [row["id"] for row in bob] == ["CHG-2001"]
    assert all(row["owner_id"] == "alice" for row in alice)
    assert all(row["owner_id"] == "bob" for row in bob)


def test_get_own_record(client):
    response = client.get("/api/charging-sessions/CHG-1001", headers=ALICE)
    assert response.status_code == 200
    assert response.json()["owner_id"] == "alice"


def test_missing_record_is_404(client):
    response = client.get("/api/charging-sessions/CHG-9999", headers=ALICE)
    assert response.status_code == 404
    assert response.json() == {"detail": "Charging session not found."}


def test_summary_uses_integer_units_and_actor_scope(client):
    assert client.get("/api/summary", headers=ALICE).json() == {
        "sessions": 2,
        "energy_wh": 42500,
        "amount_minor": 1275,
        "currency": "USD",
    }
    assert client.get("/api/summary", headers=BOB).json()["amount_minor"] == 930


def test_instances_have_independent_data(client):
    with TestClient(create_app(enabled=True)) as other:
        assert other.app.state.store is not client.app.state.store


def test_ui_and_static_assets(client):
    page = client.get("/")
    assert page.status_code == 200
    assert "Synthetic training fixture" in page.text
    assert 'id="upload-form"' in page.text
    for path in [
        "/static/styles.css",
        "/static/app.js",
        "/examples/charging-upload.csv",
        "/openapi.json",
    ]:
        assert client.get(path).status_code == 200


def test_no_production_deployment_default():
    with TestClient(create_app()) as disabled:
        assert disabled.get("/health").status_code == 503


def test_untrusted_host_rejected(client):
    assert client.get("/health", headers={"Host": "untrusted.example"}).status_code == 400


def test_security_headers(client):
    response = client.get("/")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["cache-control"] == "no-store"
