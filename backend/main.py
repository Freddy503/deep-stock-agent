"""
Main FastAPI application for TradingAgents Portfolio Monitor
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.routers import analysis, portfolio, performance, scheduler
from backend.services.scheduler import get_scheduler

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    """
    # Startup
    print("Starting TradingAgents Portfolio Monitor...")

    # Initialize scheduler (but don't auto-start)
    scheduler_service = get_scheduler()
    print("Scheduler initialized (stopped by default)")

    # Optionally auto-start scheduler based on env var
    auto_start = os.getenv("AUTO_START_SCHEDULER", "false").lower() == "true"
    if auto_start:
        hour = int(os.getenv("ANALYSIS_SCHEDULE_HOUR", "18"))
        minute = int(os.getenv("ANALYSIS_SCHEDULE_MINUTE", "30"))
        timezone = os.getenv("TIMEZONE", "America/New_York")

        scheduler_service.start(hour, minute, timezone)
        print(f"Scheduler auto-started: {hour:02d}:{minute:02d} {timezone}")

    print("Application started successfully!")

    yield

    # Shutdown
    print("Shutting down application...")
    if scheduler_service.enabled:
        scheduler_service.stop()
        print("Scheduler stopped")

    print("Application stopped")


# Create FastAPI app
app = FastAPI(
    title="TradingAgents Portfolio Monitor",
    description="Portfolio monitoring and AI-powered stock recommendations using TradingAgents framework",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router)
app.include_router(portfolio.router)
app.include_router(performance.router)
app.include_router(scheduler.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "TradingAgents Portfolio Monitor",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TradingAgents Portfolio Monitor"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "true").lower() == "true"

    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=debug
    )
