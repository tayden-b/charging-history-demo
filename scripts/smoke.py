from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app

with TestClient(create_app(enabled=True)) as client:
    headers = {"X-Demo-User": "alice"}
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/api/charging-sessions", headers=headers).status_code == 200
    result = client.post(
        "/api/imports/csv",
        headers=headers,
        files={
            "file": ("charging.csv", Path("examples/charging-upload.csv").read_bytes(), "text/csv")
        },
    )
    assert result.status_code == 201, result.text
    assert result.json()["imported"] == 2
    assert client.get("/api/summary", headers=headers).json()["sessions"] == 4
    print("Application smoke passed: startup, UI assets, actor-scoped list, CSV import, summary.")
