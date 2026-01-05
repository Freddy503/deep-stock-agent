"""
Performance tracking and analysis service
"""
from datetime import date, timedelta
from decimal import Decimal
from typing import List, Dict, Any, Optional

from backend.db.supabase import (
    get_watchlist,
    get_decisions,
    get_prices,
    save_performance,
    get_portfolio
)


async def calculate_performance_metrics(
    symbol: Optional[str] = None,
    period: str = "daily"
) -> List[Dict[str, Any]]:
    """
    Calculate performance metrics for AI recommendations

    Args:
        symbol: Stock symbol (None for all stocks)
        period: Period type (daily, weekly, monthly)

    Returns:
        List of performance metrics
    """
    # Get stocks to analyze
    if symbol:
        stocks = [{"symbol": symbol}]
    else:
        stocks = await get_watchlist()

    results = []

    for stock in stocks:
        symbol = stock["symbol"]

        # Get decisions and prices
        decisions = await get_decisions(symbol, limit=100)
        prices = await get_prices(symbol, limit=100)

        if not decisions or not prices:
            continue

        # Calculate metrics based on period
        if period == "daily":
            metrics = _calculate_daily_metrics(symbol, decisions, prices)
        elif period == "weekly":
            metrics = _calculate_weekly_metrics(symbol, decisions, prices)
        elif period == "monthly":
            metrics = _calculate_monthly_metrics(symbol, decisions, prices)
        else:
            continue

        # Save to database
        for metric in metrics:
            await save_performance(metric)
            results.append(metric)

    return results


def _calculate_daily_metrics(
    symbol: str,
    decisions: List[Dict[str, Any]],
    prices: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Calculate daily performance metrics

    For each decision, check if the price moved in the predicted direction
    over the next day.
    """
    metrics = []

    # Create price lookup by date
    price_by_date = {p["price_date"]: p for p in prices}

    for decision in decisions:
        decision_date = decision["decision_date"]
        if isinstance(decision_date, str):
            decision_date = date.fromisoformat(decision_date)

        # Get price on decision date and next day
        next_date = decision_date + timedelta(days=1)

        # Find actual next trading day (skip weekends)
        max_days_forward = 5
        current_price = None
        next_price = None

        for i in range(max_days_forward):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                current_price = price_by_date[check_date]
                break

        for i in range(1, max_days_forward):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                next_price = price_by_date[check_date]
                break

        if not current_price or not next_price:
            continue

        # Calculate actual return
        current_close = Decimal(str(current_price["close_price"]))
        next_close = Decimal(str(next_price["close_price"]))
        actual_return = (next_close - current_close) / current_close

        # Determine if AI prediction was correct
        action = decision["action"]
        hit = False

        if action == "BUY" and actual_return > 0:
            hit = True
        elif action == "SELL" and actual_return < 0:
            hit = True
        elif action == "HOLD" and abs(actual_return) < Decimal("0.01"):  # < 1% change
            hit = True

        hit_rate = Decimal("1.0") if hit else Decimal("0.0")

        metrics.append({
            "symbol": symbol,
            "period": "daily",
            "start_date": decision_date,
            "end_date": next_price["price_date"],
            "ai_recommendation": action,
            "actual_return": float(actual_return),
            "hit_rate": float(hit_rate)
        })

    return metrics


def _calculate_weekly_metrics(
    symbol: str,
    decisions: List[Dict[str, Any]],
    prices: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Calculate weekly performance metrics"""
    metrics = []

    price_by_date = {p["price_date"]: p for p in prices}

    for decision in decisions:
        decision_date = decision["decision_date"]
        if isinstance(decision_date, str):
            decision_date = date.fromisoformat(decision_date)

        # Find price 7 days later
        end_date = decision_date + timedelta(days=7)

        current_price = None
        future_price = None

        # Find closest prices
        for i in range(5):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                current_price = price_by_date[check_date]
                break

        for i in range(7, 12):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                future_price = price_by_date[check_date]
                end_date = check_date
                break

        if not current_price or not future_price:
            continue

        current_close = Decimal(str(current_price["close_price"]))
        future_close = Decimal(str(future_price["close_price"]))
        actual_return = (future_close - current_close) / current_close

        action = decision["action"]
        hit = False

        if action == "BUY" and actual_return > 0:
            hit = True
        elif action == "SELL" and actual_return < 0:
            hit = True
        elif action == "HOLD" and abs(actual_return) < Decimal("0.02"):
            hit = True

        hit_rate = Decimal("1.0") if hit else Decimal("0.0")

        metrics.append({
            "symbol": symbol,
            "period": "weekly",
            "start_date": decision_date,
            "end_date": end_date,
            "ai_recommendation": action,
            "actual_return": float(actual_return),
            "hit_rate": float(hit_rate)
        })

    return metrics


def _calculate_monthly_metrics(
    symbol: str,
    decisions: List[Dict[str, Any]],
    prices: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Calculate monthly performance metrics"""
    metrics = []

    price_by_date = {p["price_date"]: p for p in prices}

    for decision in decisions:
        decision_date = decision["decision_date"]
        if isinstance(decision_date, str):
            decision_date = date.fromisoformat(decision_date)

        end_date = decision_date + timedelta(days=30)

        current_price = None
        future_price = None

        for i in range(5):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                current_price = price_by_date[check_date]
                break

        for i in range(28, 35):
            check_date = decision_date + timedelta(days=i)
            if check_date in price_by_date:
                future_price = price_by_date[check_date]
                end_date = check_date
                break

        if not current_price or not future_price:
            continue

        current_close = Decimal(str(current_price["close_price"]))
        future_close = Decimal(str(future_price["close_price"]))
        actual_return = (future_close - current_close) / current_close

        action = decision["action"]
        hit = False

        if action == "BUY" and actual_return > 0:
            hit = True
        elif action == "SELL" and actual_return < 0:
            hit = True
        elif action == "HOLD" and abs(actual_return) < Decimal("0.05"):
            hit = True

        hit_rate = Decimal("1.0") if hit else Decimal("0.0")

        metrics.append({
            "symbol": symbol,
            "period": "monthly",
            "start_date": decision_date,
            "end_date": end_date,
            "ai_recommendation": action,
            "actual_return": float(actual_return),
            "hit_rate": float(hit_rate)
        })

    return metrics


async def get_accuracy_stats(days: int = 30) -> Dict[str, Any]:
    """
    Calculate overall AI accuracy statistics

    Args:
        days: Number of days to look back

    Returns:
        Dictionary with accuracy statistics
    """
    from backend.db.supabase import get_performance

    # Get performance data
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get all performance records
    performance_data = await get_performance(period="daily", limit=1000)

    # Filter by date range
    filtered_data = [
        p for p in performance_data
        if start_date <= p["start_date"] <= end_date
    ]

    if not filtered_data:
        return {
            "total_predictions": 0,
            "correct_predictions": 0,
            "hit_rate": 0,
            "avg_return": 0,
            "by_action": {}
        }

    total = len(filtered_data)
    correct = sum(1 for p in filtered_data if p["hit_rate"] > 0.5)
    hit_rate = correct / total if total > 0 else 0

    avg_return = sum(p["actual_return"] for p in filtered_data) / total

    # Break down by action
    by_action = {}
    for action in ["BUY", "SELL", "HOLD"]:
        action_data = [p for p in filtered_data if p["ai_recommendation"] == action]
        if action_data:
            by_action[action] = {
                "total": len(action_data),
                "correct": sum(1 for p in action_data if p["hit_rate"] > 0.5),
                "hit_rate": sum(1 for p in action_data if p["hit_rate"] > 0.5) / len(action_data),
                "avg_return": sum(p["actual_return"] for p in action_data) / len(action_data)
            }

    return {
        "total_predictions": total,
        "correct_predictions": correct,
        "hit_rate": hit_rate,
        "avg_return": avg_return,
        "by_action": by_action,
        "period_days": days
    }
