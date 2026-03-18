from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.database import Base, engine
from routes.history import router as history_router
from routes.process import router as process_router
from routes.upload import router as upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice AI Assistant",
    description="Domain-specific AI agent for invoice extraction only.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(process_router)
app.include_router(history_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "scope": "invoice-only"}
