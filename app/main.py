from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.jobs import router as jobs_router
from app.db.database import engine, Base
import logging

# --- LOGGING CONFIGURATION ---
# We use standard logging to track background worker activity
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# --- DATABASE INITIALIZATION ---
# Create tables automatically on startup for demonstration purposes.
# In a real production app, we would use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Async Job Processor",
    description="A showcase of Clean Architecture & Background Tasks using FastAPI.",
    version="1.0.0",
)

# --- GLOBAL EXCEPTION HANDLING ---
# We ensure ALL errors follow our unified JSON format: { success, data, message }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches any unexpected server errors and prevents raw terminal leaks."""
    logger.error(f"SYSTEM CRASH: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "message": "A critical system error occurred.",
            "error_detail": str(exc)
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Catches specific HTTP errors like 404 (Not Found) or 401 (Unauthorized)."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "message": exc.detail
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Catches Pydantic validation errors (e.g. invalid UUID format)."""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "message": "Input validation failed",
            "errors": exc.errors()
        },
    )

# --- MIDDLEWARE ---
# Allow testing from any domain (essential for frontend demos/deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTERS ---
app.include_router(jobs_router)

@app.get("/", tags=["Health Check"])
async def root():
    """Welcome endpoint providing interactive documentation links."""
    return {
        "success": True,
        "data": {
            "status": "online",
            "documentation": "/docs"
        },
        "message": "FastAPI Job Processor is running smoothly."
    }

if __name__ == "__main__":
    import uvicorn
    # Start the server locally
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
