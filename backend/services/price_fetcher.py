"""
Stock price fetching service using yfinance
"""
import yfinance as yf
from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal
import pandas as pd


class PriceFetcher:
    """Fetch stock prices from yfinance"""

    @staticmethod
    def fetch_latest_price(symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch the latest price for a symbol

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with price data or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")

            if hist.empty:
                return None

            latest = hist.iloc[-1]
            price_date = hist.index[-1].date()

            return {
                "symbol": symbol.upper(),
                "price_date": price_date,
                "open_price": Decimal(str(latest['Open'])),
                "high_price": Decimal(str(latest['High'])),
                "low_price": Decimal(str(latest['Low'])),
                "close_price": Decimal(str(latest['Close'])),
                "volume": int(latest['Volume'])
            }
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    @staticmethod
    def fetch_price_history(
        symbol: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        period: str = "1mo"
    ) -> List[Dict[str, Any]]:
        """
        Fetch historical prices for a symbol

        Args:
            symbol: Stock ticker symbol
            start_date: Start date for history
            end_date: End date for history
            period: Period string (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            List of price dictionaries
        """
        try:
            ticker = yf.Ticker(symbol)

            if start_date and end_date:
                hist = ticker.history(start=start_date, end=end_date)
            else:
                hist = ticker.history(period=period)

            if hist.empty:
                return []

            prices = []
            for idx, row in hist.iterrows():
                prices.append({
                    "symbol": symbol.upper(),
                    "price_date": idx.date(),
                    "open_price": Decimal(str(row['Open'])),
                    "high_price": Decimal(str(row['High'])),
                    "low_price": Decimal(str(row['Low'])),
                    "close_price": Decimal(str(row['Close'])),
                    "volume": int(row['Volume'])
                })

            return prices
        except Exception as e:
            print(f"Error fetching price history for {symbol}: {e}")
            return []

    @staticmethod
    def fetch_current_info(symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current stock info (name, market cap, etc.)

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with stock info or None if failed
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol.upper(),
                "name": info.get("longName") or info.get("shortName"),
                "market_cap": info.get("marketCap"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "current_price": Decimal(str(info.get("currentPrice", 0))) if info.get("currentPrice") else None,
            }
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return None

    @staticmethod
    def calculate_return(
        start_price: Decimal,
        end_price: Decimal
    ) -> Decimal:
        """
        Calculate percentage return between two prices

        Args:
            start_price: Starting price
            end_price: Ending price

        Returns:
            Percentage return as decimal (e.g., 0.05 for 5%)
        """
        if start_price == 0:
            return Decimal(0)

        return ((end_price - start_price) / start_price)

    @staticmethod
    def batch_fetch_latest_prices(symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch latest prices for multiple symbols

        Args:
            symbols: List of stock ticker symbols

        Returns:
            List of price dictionaries
        """
        prices = []
        for symbol in symbols:
            price = PriceFetcher.fetch_latest_price(symbol)
            if price:
                prices.append(price)

        return prices
