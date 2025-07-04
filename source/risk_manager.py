import math
from typing import Dict, List


class RiskManager:
    """Risk management utilities for portfolio and position sizing."""

    def __init__(
        self, max_position_size: float = 0.1, max_portfolio_risk: float = 0.02
    ) -> None:
        self.max_position_size = max_position_size  # Max 10% of portfolio per position
        self.max_portfolio_risk = max_portfolio_risk  # Max 2% portfolio risk per trade

    def calculate_position_size(
        self, portfolio_value: float, entry_price: float, stop_loss: float
    ) -> int:
        """Calculate position size based on risk management rules."""
        # Risk per share
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share == 0:
            return 0

        # Maximum position based on portfolio risk
        max_risk_amount = portfolio_value * self.max_portfolio_risk
        max_shares_by_risk = int(max_risk_amount / risk_per_share)

        # Maximum position based on position size limit
        max_position_value = portfolio_value * self.max_position_size
        max_shares_by_size = int(max_position_value / entry_price)

        # Take the smaller of the two limits
        return min(max_shares_by_risk, max_shares_by_size)

    def calculate_var(
        self, returns: List[float], confidence_level: float = 0.05
    ) -> float:
        """Calculate Value at Risk (VaR) at given confidence level."""
        if not returns:
            return 0.0

        sorted_returns = sorted(returns)
        index = int(len(sorted_returns) * confidence_level)
        return (
            sorted_returns[index] if index < len(sorted_returns) else sorted_returns[-1]
        )

    def calculate_sharpe_ratio(
        self, returns: List[float], risk_free_rate: float = 0.02
    ) -> float:
        """Calculate Sharpe ratio for given returns."""
        if not returns or len(returns) < 2:
            return 0.0

        excess_returns = [
            r - risk_free_rate / 252 for r in returns
        ]  # Daily risk-free rate
        avg_excess_return = sum(excess_returns) / len(excess_returns)

        # Calculate standard deviation
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)

        return avg_excess_return / std_dev if std_dev > 0 else 0.0

    def calculate_max_drawdown(self, portfolio_values: List[float]) -> float:
        """Calculate maximum drawdown from portfolio values."""
        if len(portfolio_values) < 2:
            return 0.0

        peak = portfolio_values[0]
        max_drawdown = 0.0

        for value in portfolio_values[1:]:
            if value > peak:
                peak = value
            else:
                drawdown = (peak - value) / peak
                max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    def check_position_limits(
        self,
        portfolio_value: float,
        positions: Dict[str, int],
        prices: Dict[str, float],
    ) -> Dict[str, bool]:
        """Check if current positions exceed risk limits."""
        violations = {}

        for symbol, quantity in positions.items():
            if symbol not in prices:
                continue

            position_value = quantity * prices[symbol]
            position_weight = position_value / portfolio_value

            violations[symbol] = position_weight > self.max_position_size

        return violations

    def suggest_rebalancing(
        self,
        portfolio_value: float,
        positions: Dict[str, int],
        prices: Dict[str, float],
    ) -> Dict[str, int]:
        """Suggest position adjustments to meet risk limits."""
        suggestions = {}

        for symbol, quantity in positions.items():
            if symbol not in prices:
                continue

            current_value = quantity * prices[symbol]
            current_weight = current_value / portfolio_value

            if current_weight > self.max_position_size:
                target_value = portfolio_value * self.max_position_size
                target_quantity = int(target_value / prices[symbol])
                suggestions[symbol] = target_quantity - quantity  # Negative means sell

        return suggestions
