import os
import sys

# Ensure backend directory is in sys.path for module resolution
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
load_dotenv()
load_dotenv(os.path.join(backend_dir, ".env"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.market import router as market_router

app = FastAPI(
    title="KrishiSaathi Market API",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router, prefix="/api")


@app.get("/api/health")
@app.get("/api/health-check")
def health_check():
    return {
        "status": "healthy",
        "service": "KrishiSaathi Market Intelligence API",
        "environment": "vercel"
    }
