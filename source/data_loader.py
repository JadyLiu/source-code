import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List


class DataLoader:
    """Simple market data loader and generator for backtesting."""

    def __init__(self) -> None:
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def generate_sample_data(
        self,
        symbol: str,
        days: int = 252,
        start_price: float = 100.0,
        volatility: float = 0.02,
    ) -> pd.DataFrame:
        """Generate sample stock price data for testing."""
        np.random.seed(42)  # For reproducible results

        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")[:days]

        # Generate price data using geometric Brownian motion
        returns = np.random.normal(0.0005, volatility, days)  # Small positive drift

        prices = [start_price]
        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))

        # Create OHLCV data
        data = pd.DataFrame(
            {
                "open": prices,
                "high": [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
                "low": [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
                "close": prices,
                "volume": np.random.randint(100000, 1000000, days),
            },
            index=dates,
        )

        # Ensure high >= close >= low and high >= open >= low
        data["high"] = data[["open", "close", "high"]].max(axis=1)
        data["low"] = data[["open", "close", "low"]].min(axis=1)

        self.data_cache[symbol] = data
        return data

    def load_csv_data(self, file_path: str, symbol: str) -> pd.DataFrame:
        """Load data from CSV file."""
        try:
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)

            # Ensure required columns exist
            required_columns = ["open", "high", "low", "close", "volume"]
            for col in required_columns:
                if col not in data.columns:
                    raise ValueError(f"Missing required column: {col}")

            self.data_cache[symbol] = data
            return data

        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return self.generate_sample_data(symbol)

    def get_price_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get price data for symbol within date range."""
        if symbol not in self.data_cache:
            self.generate_sample_data(symbol)

        data = self.data_cache[symbol].copy()

        if start_date:
            data = data[data.index >= start_date]
        if end_date:
            data = data[data.index <= end_date]

        return data

    def get_latest_price(self, symbol: str) -> float:
        """Get the latest price for a symbol."""
        if symbol not in self.data_cache:
            self.generate_sample_data(symbol)

        return self.data_cache[symbol]["close"].iloc[-1]

    def get_price_history(self, symbol: str, days: int = 30) -> List[float]:
        """Get recent price history for a symbol."""
        if symbol not in self.data_cache:
            self.generate_sample_data(symbol)

        return self.data_cache[symbol]["close"].tail(days).tolist()

    def add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add common technical indicators to price data."""
        df = data.copy()

        # Simple Moving Averages
        df["sma_10"] = df["close"].rolling(window=10).mean()
        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()

        # Exponential Moving Averages
        df["ema_12"] = df["close"].ewm(span=12).mean()
        df["ema_26"] = df["close"].ewm(span=26).mean()

        # MACD
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        df["macd_histogram"] = df["macd"] - df["macd_signal"]

        # Bollinger Bands
        df["bb_middle"] = df["close"].rolling(window=20).mean()
        bb_std = df["close"].rolling(window=20).std()
        df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
        df["bb_lower"] = df["bb_middle"] - (bb_std * 2)

        # RSI
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        return df

    def get_multiple_symbols(
        self, symbols: List[str], days: int = 252
    ) -> Dict[str, pd.DataFrame]:
        """Get data for multiple symbols."""
        data = {}
        for symbol in symbols:
            if symbol not in self.data_cache:
                self.generate_sample_data(symbol, days)
            data[symbol] = self.data_cache[symbol]
        return data
