"""
Pydantic models for request/response validation
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class ActionType(str, Enum):
    """Trading action types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class PeriodType(str, Enum):
    """Performance tracking periods"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# Watchlist schemas
class WatchlistCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10)
    name: Optional[str] = Field(None, max_length=255)

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class WatchlistResponse(BaseModel):
    id: str
    symbol: str
    name: Optional[str]
    added_at: datetime
    is_active: bool


# Decision schemas
class DecisionCreate(BaseModel):
    symbol: str
    decision_date: date
    action: ActionType
    confidence: Decimal = Field(..., ge=0, le=1)
    risk_score: Decimal = Field(..., ge=0, le=1)
    reasoning: str
    raw_response: Dict[str, Any]


class DecisionResponse(BaseModel):
    id: str
    symbol: str
    decision_date: date
    action: ActionType
    confidence: Decimal
    risk_score: Decimal
    reasoning: str
    raw_response: Dict[str, Any]
    created_at: datetime


# Price schemas
class PriceCreate(BaseModel):
    symbol: str
    price_date: date
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: int


class PriceResponse(BaseModel):
    id: str
    symbol: str
    price_date: date
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: int


# Portfolio schemas
class PortfolioCreate(BaseModel):
    symbol: str
    shares: Decimal = Field(..., gt=0)
    avg_cost: Decimal = Field(..., gt=0)
    first_purchase: Optional[date] = None


class PortfolioUpdate(BaseModel):
    shares: Optional[Decimal] = Field(None, gt=0)
    avg_cost: Optional[Decimal] = Field(None, gt=0)


class PortfolioResponse(BaseModel):
    id: str
    symbol: str
    shares: Decimal
    avg_cost: Decimal
    first_purchase: Optional[date]
    last_updated: datetime
    current_price: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    unrealized_pnl: Optional[Decimal] = None
    unrealized_pnl_pct: Optional[Decimal] = None


# Performance schemas
class PerformanceCreate(BaseModel):
    symbol: str
    period: PeriodType
    start_date: date
    end_date: date
    ai_recommendation: Optional[ActionType]
    actual_return: Decimal
    hit_rate: Decimal = Field(..., ge=0, le=1)


class PerformanceResponse(BaseModel):
    id: str
    symbol: str
    period: PeriodType
    start_date: date
    end_date: date
    ai_recommendation: Optional[ActionType]
    actual_return: Decimal
    hit_rate: Decimal
    created_at: datetime


# Analysis schemas
class AnalysisRequest(BaseModel):
    symbol: str
    analysis_date: Optional[date] = None

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()


class AnalysisResponse(BaseModel):
    symbol: str
    date: date
    action: ActionType
    confidence: Decimal
    risk_score: Decimal
    reasoning: str
    raw_decision: Dict[str, Any]


class BatchAnalysisRequest(BaseModel):
    symbols: Optional[List[str]] = None  # If None, analyze all active watchlist
    analysis_date: Optional[date] = None


class BatchAnalysisResponse(BaseModel):
    total: int
    successful: int
    failed: int
    results: List[AnalysisResponse]
    errors: List[Dict[str, str]]


# Dashboard schemas
class DashboardSummary(BaseModel):
    portfolio_value: Decimal
    portfolio_change_pct: Decimal
    total_holdings: int
    total_watchlist: int
    recommendations_today: int
    ai_accuracy_7d: Optional[Decimal]
    ai_accuracy_30d: Optional[Decimal]


class RecentActivity(BaseModel):
    timestamp: datetime
    activity_type: str
    symbol: str
    description: str


# Scheduler schemas
class ScheduleConfig(BaseModel):
    enabled: bool = True
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    timezone: str = "America/New_York"
    days_of_week: Optional[List[int]] = None  # 0=Monday, 6=Sunday


class ScheduleStatus(BaseModel):
    enabled: bool
    next_run: Optional[datetime]
    last_run: Optional[datetime]
    status: str
