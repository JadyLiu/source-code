import pandas as pd
from typing import List


class MovingAverageStrategy:
    """Simple moving average crossover strategy."""

    def __init__(self, short_window: int = 10, long_window: int = 30) -> None:
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, prices: pd.Series) -> pd.Series:
        """Generate buy/sell signals based on moving average crossover."""
        short_ma = prices.rolling(window=self.short_window).mean()
        long_ma = prices.rolling(window=self.long_window).mean()

        signals = pd.Series(0, index=prices.index)
        signals[short_ma > long_ma] = 1  # Buy signal
        signals[short_ma < long_ma] = -1  # Sell signal

        return signals

    def get_signal(self, prices: List[float]) -> int:
        """Get current signal for latest prices."""
        if len(prices) < self.long_window:
            return 0

        short_ma = sum(prices[-self.short_window :]) / self.short_window
        long_ma = sum(prices[-self.long_window :]) / self.long_window

        if short_ma > long_ma:
            return 1  # Buy
        elif short_ma < long_ma:
            return -1  # Sell
        return 0  # Hold


class MomentumStrategy:
    """Simple momentum-based strategy."""

    def __init__(self, lookback_period: int = 14, threshold: float = 0.02) -> None:
        self.lookback_period = lookback_period
        self.threshold = threshold

    def calculate_momentum(self, prices: pd.Series) -> pd.Series:
        """Calculate momentum as percentage change over lookback period."""
        return prices.pct_change(self.lookback_period)

    def get_signal(self, prices: List[float]) -> int:
        """Get momentum signal for latest prices."""
        if len(prices) < self.lookback_period + 1:
            return 0

        momentum = (prices[-1] - prices[-self.lookback_period - 1]) / prices[
            -self.lookback_period - 1
        ]

        if momentum > self.threshold:
            return 1  # Strong upward momentum - Buy
        elif momentum < -self.threshold:
            return -1  # Strong downward momentum - Sell
        return 0  # Hold


class RSIStrategy:
    """Relative Strength Index strategy."""

    def __init__(
        self, period: int = 14, oversold: float = 30, overbought: float = 70
    ) -> None:
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def calculate_rsi(self, prices: List[float]) -> float:
        """Calculate RSI for given prices."""
        if len(prices) < self.period + 1:
            return 50  # Neutral RSI

        deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        gains = [max(0, delta) for delta in deltas[-self.period :]]
        losses = [max(0, -delta) for delta in deltas[-self.period :]]

        avg_gain = sum(gains) / self.period
        avg_loss = sum(losses) / self.period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def get_signal(self, prices: List[float]) -> int:
        """Get RSI-based signal."""
        rsi = self.calculate_rsi(prices)

        if rsi < self.oversold:
            return 1  # Oversold - Buy
        elif rsi > self.overbought:
            return -1  # Overbought - Sell
        return 0  # Hold
