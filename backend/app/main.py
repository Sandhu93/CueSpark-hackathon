from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import jobs, uploads
from app.core.config import settings
from app.core.db import init_db
from app.core.storage import ensure_bucket


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — env={}", settings.env)
    await init_db()
    ensure_bucket()
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Hackathon API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.env}


app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
