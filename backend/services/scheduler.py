"""
Background job scheduler using APScheduler
"""
import asyncio
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError
import os

from backend.db.supabase import get_watchlist, save_decision
from backend.services.trading_agents import get_trading_agents_service
from backend.services.price_fetcher import PriceFetcher
from backend.services.performance import calculate_performance_metrics


class AnalysisScheduler:
    """Scheduler for automated stock analysis"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.enabled = False
        self.last_run: Optional[datetime] = None

    def start(
        self,
        hour: int = 18,
        minute: int = 30,
        timezone: str = "America/New_York"
    ):
        """
        Start the scheduler

        Args:
            hour: Hour to run analysis (0-23)
            minute: Minute to run analysis (0-59)
            timezone: Timezone string (e.g., 'America/New_York')
        """
        # Remove existing job if any
        try:
            self.scheduler.remove_job('daily_analysis')
        except JobLookupError:
            pass

        # Add daily analysis job
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            timezone=timezone
        )

        self.scheduler.add_job(
            self._run_daily_analysis,
            trigger=trigger,
            id='daily_analysis',
            name='Daily Stock Analysis',
            replace_existing=True
        )

        # Start scheduler if not running
        if not self.scheduler.running:
            self.scheduler.start()

        self.enabled = True
        print(f"Scheduler started: Daily analysis at {hour:02d}:{minute:02d} {timezone}")

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
        self.enabled = False
        print("Scheduler stopped")

    async def run_now(self) -> dict:
        """
        Manually trigger analysis immediately

        Returns:
            Dictionary with results
        """
        return await self._run_daily_analysis()

    async def _run_daily_analysis(self) -> dict:
        """
        Run analysis for all stocks in watchlist

        This is the main scheduled job that:
        1. Fetches latest prices for all stocks
        2. Runs AI analysis for each stock
        3. Saves decisions to database
        4. Calculates performance metrics
        """
        print(f"Starting daily analysis at {datetime.now()}")
        self.last_run = datetime.now()

        try:
            # Get active watchlist
            watchlist = await get_watchlist(active_only=True)
            total = len(watchlist)
            successful = 0
            failed = 0
            errors = []

            print(f"Analyzing {total} stocks...")

            # Step 1: Fetch latest prices for all stocks
            print("Fetching latest prices...")
            symbols = [stock["symbol"] for stock in watchlist]
            prices = PriceFetcher.batch_fetch_latest_prices(symbols)

            # Save prices to database
            from backend.db.supabase import save_prices
            if prices:
                await save_prices(prices)
                print(f"Saved {len(prices)} price updates")

            # Step 2: Run AI analysis for each stock
            trading_service = get_trading_agents_service()

            for stock in watchlist:
                symbol = stock["symbol"]
                try:
                    print(f"Analyzing {symbol}...")

                    # Run TradingAgents analysis
                    result = await trading_service.analyze_stock(symbol)

                    # Prepare decision data for database
                    decision_data = {
                        "symbol": result["symbol"],
                        "decision_date": result["date"],
                        "action": result["action"],
                        "confidence": float(result["confidence"]),
                        "risk_score": float(result["risk_score"]),
                        "reasoning": result["reasoning"],
                        "raw_response": result["raw_decision"]
                    }

                    # Save to database
                    await save_decision(decision_data)

                    successful += 1
                    print(f"✓ {symbol}: {result['action']} (confidence: {result['confidence']:.2f})")

                except Exception as e:
                    failed += 1
                    error_msg = f"Error analyzing {symbol}: {str(e)}"
                    errors.append({"symbol": symbol, "error": str(e)})
                    print(f"✗ {error_msg}")

            # Step 3: Calculate performance metrics
            print("Calculating performance metrics...")
            try:
                await calculate_performance_metrics()
                print("✓ Performance metrics updated")
            except Exception as e:
                print(f"✗ Error calculating performance: {e}")

            result = {
                "timestamp": self.last_run.isoformat(),
                "total": total,
                "successful": successful,
                "failed": failed,
                "errors": errors
            }

            print(f"Daily analysis complete: {successful}/{total} successful")
            return result

        except Exception as e:
            error_msg = f"Error in daily analysis: {str(e)}"
            print(error_msg)
            return {
                "timestamp": datetime.now().isoformat(),
                "error": error_msg
            }

    def get_status(self) -> dict:
        """
        Get scheduler status

        Returns:
            Dictionary with status information
        """
        next_run = None

        if self.enabled and self.scheduler.running:
            job = self.scheduler.get_job('daily_analysis')
            if job:
                next_run = job.next_run_time

        return {
            "enabled": self.enabled,
            "running": self.scheduler.running,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": next_run.isoformat() if next_run else None,
            "status": "active" if self.enabled else "stopped"
        }


# Singleton instance
_scheduler = None


def get_scheduler() -> AnalysisScheduler:
    """Get or create scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = AnalysisScheduler()
    return _scheduler
