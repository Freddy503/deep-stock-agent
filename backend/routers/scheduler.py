"""
Scheduler management API endpoints
"""
from fastapi import APIRouter, HTTPException

from backend.models.schemas import (
    ScheduleConfig,
    ScheduleStatus
)
from backend.services.scheduler import get_scheduler

router = APIRouter(prefix="/api/schedule", tags=["scheduler"])


@router.get("/status", response_model=ScheduleStatus)
async def get_schedule_status():
    """
    Get current scheduler status

    Returns:
        Scheduler status information
    """
    try:
        scheduler = get_scheduler()
        status = scheduler.get_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scheduler status: {str(e)}")


@router.post("/configure", response_model=ScheduleStatus)
async def configure_schedule(config: ScheduleConfig):
    """
    Configure the analysis schedule

    Args:
        config: Schedule configuration

    Returns:
        Updated scheduler status
    """
    try:
        scheduler = get_scheduler()

        if config.enabled:
            # Start scheduler with new configuration
            scheduler.start(
                hour=config.hour,
                minute=config.minute,
                timezone=config.timezone
            )
        else:
            # Stop scheduler
            scheduler.stop()

        status = scheduler.get_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to configure scheduler: {str(e)}")


@router.post("/run-now")
async def run_analysis_now():
    """
    Manually trigger analysis immediately

    Returns:
        Analysis results
    """
    try:
        scheduler = get_scheduler()
        result = await scheduler.run_now()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run analysis: {str(e)}")


@router.post("/start", response_model=ScheduleStatus)
async def start_scheduler(
    hour: int = 18,
    minute: int = 30,
    timezone: str = "America/New_York"
):
    """
    Start the scheduler

    Args:
        hour: Hour to run (0-23)
        minute: Minute to run (0-59)
        timezone: Timezone string

    Returns:
        Scheduler status
    """
    try:
        scheduler = get_scheduler()
        scheduler.start(hour, minute, timezone)
        status = scheduler.get_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")


@router.post("/stop", response_model=ScheduleStatus)
async def stop_scheduler():
    """
    Stop the scheduler

    Returns:
        Scheduler status
    """
    try:
        scheduler = get_scheduler()
        scheduler.stop()
        status = scheduler.get_status()
        return status

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop scheduler: {str(e)}")
