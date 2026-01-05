"""
Portfolio management API endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List
from decimal import Decimal

from backend.models.schemas import (
    WatchlistCreate,
    WatchlistResponse,
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse
)
from backend.db.supabase import (
    get_watchlist,
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist_stock,
    get_portfolio,
    get_portfolio_stock,
    add_to_portfolio,
    update_portfolio,
    remove_from_portfolio,
    get_latest_price
)
from backend.services.price_fetcher import PriceFetcher

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


# Watchlist endpoints
@router.get("/watchlist", response_model=List[WatchlistResponse])
async def list_watchlist(active_only: bool = True):
    """
    Get all stocks in watchlist

    Args:
        active_only: Only return active stocks

    Returns:
        List of watchlist stocks
    """
    try:
        watchlist = await get_watchlist(active_only)
        return watchlist

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch watchlist: {str(e)}")


@router.post("/watchlist", response_model=WatchlistResponse)
async def add_stock_to_watchlist(request: WatchlistCreate):
    """
    Add stock to watchlist

    Args:
        request: Watchlist creation data

    Returns:
        Created watchlist entry
    """
    try:
        # Fetch stock info to validate and get name
        if not request.name:
            info = PriceFetcher.fetch_current_info(request.symbol)
            if info and info.get("name"):
                request.name = info["name"]

        stock = await add_to_watchlist(request.symbol, request.name)
        return stock

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to watchlist: {str(e)}")


@router.delete("/watchlist/{symbol}")
async def remove_stock_from_watchlist(symbol: str):
    """
    Remove stock from watchlist

    Args:
        symbol: Stock ticker symbol

    Returns:
        Success message
    """
    try:
        await remove_from_watchlist(symbol)
        return {"message": f"{symbol} removed from watchlist"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from watchlist: {str(e)}")


@router.get("/watchlist/{symbol}", response_model=WatchlistResponse)
async def get_watchlist_item(symbol: str):
    """
    Get single watchlist stock

    Args:
        symbol: Stock ticker symbol

    Returns:
        Watchlist stock details
    """
    try:
        stock = await get_watchlist_stock(symbol)

        if not stock:
            raise HTTPException(status_code=404, detail=f"{symbol} not found in watchlist")

        return stock

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch watchlist stock: {str(e)}")


# Portfolio endpoints
@router.get("/holdings", response_model=List[PortfolioResponse])
async def list_holdings():
    """
    Get all portfolio holdings with current prices

    Returns:
        List of portfolio holdings
    """
    try:
        holdings = await get_portfolio()

        # Enrich with current prices and P&L
        enriched_holdings = []
        for holding in holdings:
            symbol = holding["symbol"]

            # Get latest price
            latest_price = await get_latest_price(symbol)

            if latest_price:
                current_price = Decimal(str(latest_price["close_price"]))
                shares = Decimal(str(holding["shares"]))
                avg_cost = Decimal(str(holding["avg_cost"]))

                current_value = shares * current_price
                cost_basis = shares * avg_cost
                unrealized_pnl = current_value - cost_basis
                unrealized_pnl_pct = (unrealized_pnl / cost_basis) if cost_basis > 0 else Decimal(0)

                holding["current_price"] = current_price
                holding["current_value"] = current_value
                holding["unrealized_pnl"] = unrealized_pnl
                holding["unrealized_pnl_pct"] = unrealized_pnl_pct

            enriched_holdings.append(holding)

        return enriched_holdings

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch holdings: {str(e)}")


@router.get("/holdings/{symbol}", response_model=PortfolioResponse)
async def get_holding(symbol: str):
    """
    Get single portfolio holding

    Args:
        symbol: Stock ticker symbol

    Returns:
        Portfolio holding details
    """
    try:
        holding = await get_portfolio_stock(symbol)

        if not holding:
            raise HTTPException(status_code=404, detail=f"{symbol} not found in portfolio")

        # Enrich with current price
        latest_price = await get_latest_price(symbol)

        if latest_price:
            current_price = Decimal(str(latest_price["close_price"]))
            shares = Decimal(str(holding["shares"]))
            avg_cost = Decimal(str(holding["avg_cost"]))

            current_value = shares * current_price
            cost_basis = shares * avg_cost
            unrealized_pnl = current_value - cost_basis
            unrealized_pnl_pct = (unrealized_pnl / cost_basis) if cost_basis > 0 else Decimal(0)

            holding["current_price"] = current_price
            holding["current_value"] = current_value
            holding["unrealized_pnl"] = unrealized_pnl
            holding["unrealized_pnl_pct"] = unrealized_pnl_pct

        return holding

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch holding: {str(e)}")


@router.post("/holdings", response_model=PortfolioResponse)
async def add_holding(request: PortfolioCreate):
    """
    Add stock to portfolio

    Args:
        request: Portfolio creation data

    Returns:
        Created portfolio entry
    """
    try:
        from datetime import date

        # Set first purchase date if not provided
        if not request.first_purchase:
            request.first_purchase = date.today()

        portfolio_data = {
            "symbol": request.symbol.upper(),
            "shares": float(request.shares),
            "avg_cost": float(request.avg_cost),
            "first_purchase": request.first_purchase
        }

        holding = await add_to_portfolio(portfolio_data)
        return holding

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to portfolio: {str(e)}")


@router.put("/holdings/{symbol}", response_model=PortfolioResponse)
async def update_holding(symbol: str, request: PortfolioUpdate):
    """
    Update portfolio holding

    Args:
        symbol: Stock ticker symbol
        request: Portfolio update data

    Returns:
        Updated portfolio entry
    """
    try:
        # Build updates dict
        updates = {}
        if request.shares is not None:
            updates["shares"] = float(request.shares)
        if request.avg_cost is not None:
            updates["avg_cost"] = float(request.avg_cost)

        if not updates:
            raise HTTPException(status_code=400, detail="No updates provided")

        holding = await update_portfolio(symbol, updates)
        return holding

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update portfolio: {str(e)}")


@router.delete("/holdings/{symbol}")
async def remove_holding(symbol: str):
    """
    Remove stock from portfolio

    Args:
        symbol: Stock ticker symbol

    Returns:
        Success message
    """
    try:
        await remove_from_portfolio(symbol)
        return {"message": f"{symbol} removed from portfolio"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from portfolio: {str(e)}")
