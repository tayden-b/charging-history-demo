import os
from importlib.metadata import version
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.imports import MAX_UPLOAD_BYTES, parse_upload
from app.middleware import DemoBoundaryMiddleware
from app.models import ChargingSession, ChargingSummary, ImportResult
from app.store import DEMO_USERS, SessionConflictError, SessionStore

ROOT = Path(__file__).resolve().parent.parent


def current_actor(x_demo_user: Annotated[str | None, Header()] = None) -> str:
    if x_demo_user not in DEMO_USERS:
        raise HTTPException(status_code=401, detail="Choose a synthetic demo user: alice or bob.")
    return x_demo_user


def get_store(request: Request) -> SessionStore:
    return request.app.state.store


Actor = Annotated[str, Depends(current_actor)]
Store = Annotated[SessionStore, Depends(get_store)]


def create_app(*, enabled: bool = False) -> FastAPI:
    application = FastAPI(
        title="ChargeLedger training API",
        description=(
            "Synthetic local-only fixture. Demo identities are not production authentication."
        ),
        docs_url=None,
        redoc_url=None,
    )
    application.state.store = SessionStore()
    application.add_middleware(DemoBoundaryMiddleware, enabled=enabled)
    application.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "testserver"]
    )
    application.mount("/static", StaticFiles(directory=ROOT / "app" / "static"), name="static")

    @application.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(ROOT / "app" / "static" / "index.html")

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "synthetic-training-only"}

    @application.get("/api/demo/context")
    def demo_context() -> dict:
        return {
            "users": [{"id": key, "name": name} for key, name in DEMO_USERS.items()],
            "dependencies": {
                "fastapi": version("fastapi"),
                "starlette": version("starlette"),
                "python-multipart": version("python-multipart"),
            },
            "identity": "X-Demo-User is a test identity selector, not production authentication.",
        }

    @application.get("/api/charging-sessions", response_model=list[ChargingSession])
    def list_sessions(actor: Actor, store: Store) -> list[ChargingSession]:
        return store.list_for(actor)

    @application.get("/api/charging-sessions/{session_id}", response_model=ChargingSession)
    def get_session(session_id: str, actor: Actor, store: Store) -> ChargingSession:
        session = store.get(session_id)
        if session is None or session.owner_id != actor:
            raise HTTPException(status_code=404, detail="Charging session not found.")
        return session

    @application.get("/api/summary", response_model=ChargingSummary)
    def summary(actor: Actor, store: Store) -> ChargingSummary:
        return store.summary_for(actor)

    @application.post("/api/imports/csv", response_model=ImportResult, status_code=201)
    async def import_csv(
        actor: Actor, store: Store, file: Annotated[UploadFile, File()]
    ) -> ImportResult:
        try:
            content = await file.read(MAX_UPLOAD_BYTES + 1)
            if len(content) > MAX_UPLOAD_BYTES:
                raise HTTPException(status_code=413, detail="CSV exceeds the 256 KiB file limit.")
            vehicle = DEMO_USERS[actor].split(" / ", 1)[1]
            rows = parse_upload(content, actor, vehicle)
            store.add_many(rows)
        except SessionConflictError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        finally:
            await file.close()
        return ImportResult(imported=len(rows), session_ids=[row.id for row in rows])

    @application.get("/examples/charging-upload.csv", include_in_schema=False)
    def sample_csv() -> FileResponse:
        return FileResponse(
            ROOT / "examples" / "charging-upload.csv",
            media_type="text/csv",
            filename="charging-upload.csv",
        )

    return application


app = create_app(enabled=os.getenv("CHARGING_DEMO") == "1")
