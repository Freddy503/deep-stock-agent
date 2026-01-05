"""
Analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import date
from typing import List

from backend.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    DecisionResponse
)
from backend.services.trading_agents import get_trading_agents_service
from backend.db.supabase import (
    save_decision,
    get_decisions,
    get_latest_decision,
    get_all_latest_decisions,
    get_watchlist
)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/{symbol}", response_model=AnalysisResponse)
async def analyze_stock(
    symbol: str,
    request: AnalysisRequest = None
):
    """
    Run AI analysis for a single stock

    Args:
        symbol: Stock ticker symbol
        request: Optional analysis parameters

    Returns:
        Analysis results with recommendation
    """
    try:
        trading_service = get_trading_agents_service()

        analysis_date = request.analysis_date if request else None

        # Run analysis
        result = await trading_service.analyze_stock(symbol, analysis_date)

        # Save decision to database
        decision_data = {
            "symbol": result["symbol"],
            "decision_date": result["date"],
            "action": result["action"],
            "confidence": float(result["confidence"]),
            "risk_score": float(result["risk_score"]),
            "reasoning": result["reasoning"],
            "raw_response": result["raw_decision"]
        }

        await save_decision(decision_data)

        return AnalysisResponse(
            symbol=result["symbol"],
            date=result["date"],
            action=result["action"],
            confidence=result["confidence"],
            risk_score=result["risk_score"],
            reasoning=result["reasoning"],
            raw_decision=result["raw_decision"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/batch", response_model=BatchAnalysisResponse)
async def batch_analyze(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Run AI analysis for multiple stocks

    Args:
        request: Batch analysis request with symbols list

    Returns:
        Batch analysis results
    """
    try:
        # Get symbols to analyze
        if request.symbols:
            symbols = request.symbols
        else:
            # Analyze all active watchlist stocks
            watchlist = await get_watchlist(active_only=True)
            symbols = [stock["symbol"] for stock in watchlist]

        trading_service = get_trading_agents_service()
        results = []
        errors = []

        for symbol in symbols:
            try:
                result = await trading_service.analyze_stock(
                    symbol,
                    request.analysis_date
                )

                # Save decision
                decision_data = {
                    "symbol": result["symbol"],
                    "decision_date": result["date"],
                    "action": result["action"],
                    "confidence": float(result["confidence"]),
                    "risk_score": float(result["risk_score"]),
                    "reasoning": result["reasoning"],
                    "raw_response": result["raw_decision"]
                }

                await save_decision(decision_data)

                results.append(AnalysisResponse(
                    symbol=result["symbol"],
                    date=result["date"],
                    action=result["action"],
                    confidence=result["confidence"],
                    risk_score=result["risk_score"],
                    reasoning=result["reasoning"],
                    raw_decision=result["raw_decision"]
                ))

            except Exception as e:
                errors.append({
                    "symbol": symbol,
                    "error": str(e)
                })

        return BatchAnalysisResponse(
            total=len(symbols),
            successful=len(results),
            failed=len(errors),
            results=results,
            errors=errors
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@router.get("/decisions/{symbol}", response_model=List[DecisionResponse])
async def get_stock_decisions(
    symbol: str,
    start_date: date = None,
    end_date: date = None,
    limit: int = 100
):
    """
    Get decision history for a stock

    Args:
        symbol: Stock ticker symbol
        start_date: Optional start date filter
        end_date: Optional end date filter
        limit: Maximum number of decisions to return

    Returns:
        List of historical decisions
    """
    try:
        decisions = await get_decisions(symbol, start_date, end_date, limit)
        return decisions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch decisions: {str(e)}")


@router.get("/decisions/{symbol}/latest", response_model=DecisionResponse)
async def get_stock_latest_decision(symbol: str):
    """
    Get the most recent decision for a stock

    Args:
        symbol: Stock ticker symbol

    Returns:
        Latest decision
    """
    try:
        decision = await get_latest_decision(symbol)

        if not decision:
            raise HTTPException(status_code=404, detail=f"No decisions found for {symbol}")

        return decision

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch decision: {str(e)}")


@router.get("/decisions", response_model=List[DecisionResponse])
async def get_all_decisions():
    """
    Get latest decisions for all stocks

    Returns:
        List of latest decisions for each stock
    """
    try:
        decisions = await get_all_latest_decisions()
        return decisions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch decisions: {str(e)}")
