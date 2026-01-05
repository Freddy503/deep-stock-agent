"""
Supabase database client and operations
"""
import os
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class SupabaseClient:
    """Singleton Supabase client"""

    _instance: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client"""
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

            cls._instance = create_client(url, key)

        return cls._instance


# Watchlist operations
async def get_watchlist(active_only: bool = True) -> List[Dict[str, Any]]:
    """Get all stocks in watchlist"""
    client = SupabaseClient.get_client()
    query = client.table("watchlist").select("*")

    if active_only:
        query = query.eq("is_active", True)

    response = query.execute()
    return response.data


async def add_to_watchlist(symbol: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Add stock to watchlist"""
    client = SupabaseClient.get_client()
    data = {"symbol": symbol.upper(), "name": name}

    response = client.table("watchlist").insert(data).execute()
    return response.data[0]


async def remove_from_watchlist(symbol: str) -> None:
    """Remove stock from watchlist (soft delete)"""
    client = SupabaseClient.get_client()
    client.table("watchlist").update({"is_active": False}).eq("symbol", symbol.upper()).execute()


async def get_watchlist_stock(symbol: str) -> Optional[Dict[str, Any]]:
    """Get single stock from watchlist"""
    client = SupabaseClient.get_client()
    response = client.table("watchlist").select("*").eq("symbol", symbol.upper()).execute()

    if response.data:
        return response.data[0]
    return None


# Decision operations
async def save_decision(decision_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save AI decision to database"""
    client = SupabaseClient.get_client()

    # Convert date to string if needed
    if isinstance(decision_data.get("decision_date"), date):
        decision_data["decision_date"] = decision_data["decision_date"].isoformat()

    # Upsert (insert or update if exists)
    response = client.table("decisions").upsert(decision_data).execute()
    return response.data[0]


async def get_decisions(
    symbol: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Get decision history for a stock"""
    client = SupabaseClient.get_client()
    query = client.table("decisions").select("*").eq("symbol", symbol.upper())

    if start_date:
        query = query.gte("decision_date", start_date.isoformat())
    if end_date:
        query = query.lte("decision_date", end_date.isoformat())

    query = query.order("decision_date", desc=True).limit(limit)
    response = query.execute()
    return response.data


async def get_latest_decision(symbol: str) -> Optional[Dict[str, Any]]:
    """Get most recent decision for a stock"""
    client = SupabaseClient.get_client()
    response = (
        client.table("decisions")
        .select("*")
        .eq("symbol", symbol.upper())
        .order("decision_date", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]
    return None


async def get_all_latest_decisions() -> List[Dict[str, Any]]:
    """Get latest decision for each stock"""
    client = SupabaseClient.get_client()

    # Get all unique symbols
    watchlist = await get_watchlist()
    results = []

    for stock in watchlist:
        decision = await get_latest_decision(stock["symbol"])
        if decision:
            results.append(decision)

    return results


# Price operations
async def save_prices(prices: List[Dict[str, Any]]) -> None:
    """Batch save price data"""
    client = SupabaseClient.get_client()

    # Convert dates to strings
    for price in prices:
        if isinstance(price.get("price_date"), date):
            price["price_date"] = price["price_date"].isoformat()

    client.table("prices").upsert(prices).execute()


async def get_prices(
    symbol: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 365
) -> List[Dict[str, Any]]:
    """Get price history for a stock"""
    client = SupabaseClient.get_client()
    query = client.table("prices").select("*").eq("symbol", symbol.upper())

    if start_date:
        query = query.gte("price_date", start_date.isoformat())
    if end_date:
        query = query.lte("price_date", end_date.isoformat())

    query = query.order("price_date", desc=True).limit(limit)
    response = query.execute()
    return response.data


async def get_latest_price(symbol: str) -> Optional[Dict[str, Any]]:
    """Get most recent price for a stock"""
    client = SupabaseClient.get_client()
    response = (
        client.table("prices")
        .select("*")
        .eq("symbol", symbol.upper())
        .order("price_date", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]
    return None


# Portfolio operations
async def get_portfolio() -> List[Dict[str, Any]]:
    """Get all portfolio holdings"""
    client = SupabaseClient.get_client()
    response = client.table("portfolio").select("*").execute()
    return response.data


async def get_portfolio_stock(symbol: str) -> Optional[Dict[str, Any]]:
    """Get single portfolio holding"""
    client = SupabaseClient.get_client()
    response = client.table("portfolio").select("*").eq("symbol", symbol.upper()).execute()

    if response.data:
        return response.data[0]
    return None


async def add_to_portfolio(portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add stock to portfolio"""
    client = SupabaseClient.get_client()

    # Convert dates to strings
    if isinstance(portfolio_data.get("first_purchase"), date):
        portfolio_data["first_purchase"] = portfolio_data["first_purchase"].isoformat()

    response = client.table("portfolio").upsert(portfolio_data).execute()
    return response.data[0]


async def update_portfolio(symbol: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update portfolio holding"""
    client = SupabaseClient.get_client()
    updates["last_updated"] = datetime.utcnow().isoformat()

    response = (
        client.table("portfolio")
        .update(updates)
        .eq("symbol", symbol.upper())
        .execute()
    )
    return response.data[0]


async def remove_from_portfolio(symbol: str) -> None:
    """Remove stock from portfolio"""
    client = SupabaseClient.get_client()
    client.table("portfolio").delete().eq("symbol", symbol.upper()).execute()


# Performance operations
async def save_performance(performance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save performance metrics"""
    client = SupabaseClient.get_client()

    # Convert dates to strings
    if isinstance(performance_data.get("start_date"), date):
        performance_data["start_date"] = performance_data["start_date"].isoformat()
    if isinstance(performance_data.get("end_date"), date):
        performance_data["end_date"] = performance_data["end_date"].isoformat()

    response = client.table("performance").insert(performance_data).execute()
    return response.data[0]


async def get_performance(
    symbol: Optional[str] = None,
    period: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Get performance metrics"""
    client = SupabaseClient.get_client()
    query = client.table("performance").select("*")

    if symbol:
        query = query.eq("symbol", symbol.upper())
    if period:
        query = query.eq("period", period)

    query = query.order("start_date", desc=True).limit(limit)
    response = query.execute()
    return response.data
