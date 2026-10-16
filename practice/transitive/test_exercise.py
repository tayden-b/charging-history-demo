from exercise import app
from fastapi.testclient import TestClient


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_small_upload_contract():
    with TestClient(app) as client:
        response = client.post(
            "/upload", files={"file": ("sessions.csv", b"a,b\n1,2\n", "text/csv")}
        )
        assert response.status_code == 200
        assert response.json() == {"filename": "sessions.csv", "bytes": 8}


def test_missing_file():
    with TestClient(app) as client:
        assert client.post("/upload").status_code == 422
