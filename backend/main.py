from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from routers import validator, hunter

app = FastAPI(
    title="WinPilot API",
    description="AI-powered dropshipping product research backend",
    version="1.0.0",
)

# CORS — allow frontend origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validator.router, prefix="/api")
app.include_router(hunter.router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "WinPilot API"}
