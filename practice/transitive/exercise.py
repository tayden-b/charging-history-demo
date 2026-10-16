from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: Annotated[UploadFile, File()]) -> dict[str, int | str]:
    try:
        data = await file.read(1025)
        return {"filename": file.filename or "", "bytes": len(data)}
    finally:
        await file.close()
