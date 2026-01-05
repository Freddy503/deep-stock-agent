"""
Performance analytics API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import date, timedelta
from decimal import Decimal

from backend.models.schemas import (
    PerformanceResponse,
    DashboardSummary
)
from backend.db.supabase import (
    get_performance,
    get_portfolio,
    get_watchlist,
    get_latest_price,
    get_all_latest_decisions
)
from backend.services.performance import (
    calculate_performance_metrics,
    get_accuracy_stats
)

router = APIRouter(prefix="/api/performance", tags=["performance"])


@router.get("/{symbol}", response_model=List[PerformanceResponse])
async def get_stock_performance(
    symbol: str,
    period: str = None,
    limit: int = 100
):
    """
    Get performance metrics for a stock

    Args:
        symbol: Stock ticker symbol
        period: Period filter (daily, weekly, monthly)
        limit: Maximum number of records

    Returns:
        List of performance metrics
    """
    try:
        performance = await get_performance(symbol, period, limit)
        return performance

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch performance: {str(e)}")


@router.get("/", response_model=List[PerformanceResponse])
async def get_all_performance(
    period: str = None,
    limit: int = 100
):
    """
    Get performance metrics for all stocks

    Args:
        period: Period filter (daily, weekly, monthly)
        limit: Maximum number of records

    Returns:
        List of performance metrics
    """
    try:
        performance = await get_performance(None, period, limit)
        return performance

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch performance: {str(e)}")


@router.post("/calculate/{symbol}")
async def calculate_stock_performance(
    symbol: str,
    period: str = "daily"
):
    """
    Calculate and save performance metrics for a stock

    Args:
        symbol: Stock ticker symbol
        period: Period type (daily, weekly, monthly)

    Returns:
        Calculated performance metrics
    """
    try:
        metrics = await calculate_performance_metrics(symbol, period)
        return {
            "symbol": symbol,
            "period": period,
            "metrics_count": len(metrics),
            "metrics": metrics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate performance: {str(e)}")


@router.post("/calculate")
async def calculate_all_performance(period: str = "daily"):
    """
    Calculate and save performance metrics for all stocks

    Args:
        period: Period type (daily, weekly, monthly)

    Returns:
        Calculated performance metrics
    """
    try:
        metrics = await calculate_performance_metrics(None, period)
        return {
            "period": period,
            "metrics_count": len(metrics),
            "metrics": metrics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate performance: {str(e)}")


@router.get("/stats/accuracy")
async def get_accuracy_statistics(days: int = 30):
    """
    Get overall AI accuracy statistics

    Args:
        days: Number of days to analyze

    Returns:
        Accuracy statistics
    """
    try:
        stats = await get_accuracy_stats(days)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch accuracy stats: {str(e)}")


@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    """
    Get dashboard summary with key metrics

    Returns:
        Dashboard summary data
    """
    try:
        # Get portfolio value
        holdings = await get_portfolio()
        total_value = Decimal(0)
        total_cost = Decimal(0)

        for holding in holdings:
            symbol = holding["symbol"]
            shares = Decimal(str(holding["shares"]))
            avg_cost = Decimal(str(holding["avg_cost"]))

            # Get current price
            latest_price = await get_latest_price(symbol)
            if latest_price:
                current_price = Decimal(str(latest_price["close_price"]))
                total_value += shares * current_price
                total_cost += shares * avg_cost

        # Calculate portfolio change %
        portfolio_change_pct = Decimal(0)
        if total_cost > 0:
            portfolio_change_pct = ((total_value - total_cost) / total_cost) * 100

        # Get watchlist count
        watchlist = await get_watchlist(active_only=True)
        total_watchlist = len(watchlist)

        # Get today's recommendations
        today = date.today()
        decisions = await get_all_latest_decisions()
        recommendations_today = sum(
            1 for d in decisions
            if d.get("decision_date") == today or d.get("decision_date") == today.isoformat()
        )

        # Get AI accuracy
        stats_7d = await get_accuracy_stats(7)
        stats_30d = await get_accuracy_stats(30)

        return DashboardSummary(
            portfolio_value=total_value,
            portfolio_change_pct=portfolio_change_pct,
            total_holdings=len(holdings),
            total_watchlist=total_watchlist,
            recommendations_today=recommendations_today,
            ai_accuracy_7d=Decimal(str(stats_7d.get("hit_rate", 0))) if stats_7d.get("hit_rate") else None,
            ai_accuracy_30d=Decimal(str(stats_30d.get("hit_rate", 0))) if stats_30d.get("hit_rate") else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard summary: {str(e)}")
