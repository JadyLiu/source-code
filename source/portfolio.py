from datetime import datetime
from typing import Dict, List


class Portfolio:
    """Simple portfolio management system for tracking stock positions."""

    def __init__(self, initial_cash: float = 100000.0) -> None:
        self.cash = initial_cash
        self.positions: Dict[str, int] = {}  # symbol -> quantity
        self.trades: List[Dict] = []

    def buy(self, symbol: str, quantity: int, price: float) -> bool:
        """Buy shares if sufficient cash available."""
        cost = quantity * price
        if cost > self.cash:
            return False

        self.cash -= cost
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        self.trades.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "action": "BUY",
                "timestamp": datetime.now(),
            }
        )
        return True

    def sell(self, symbol: str, quantity: int, price: float) -> bool:
        """Sell shares if sufficient position available."""
        if self.positions.get(symbol, 0) < quantity:
            return False

        self.cash += quantity * price
        self.positions[symbol] -= quantity
        if self.positions[symbol] == 0:
            del self.positions[symbol]

        self.trades.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "price": price,
                "action": "SELL",
                "timestamp": datetime.now(),
            }
        )
        return True

    def get_position_value(self, symbol: str, current_price: float) -> float:
        """Calculate current value of position."""
        return self.positions.get(symbol, 0) * current_price

    def get_total_value(self, prices: Dict[str, float]) -> float:
        """Calculate total portfolio value."""
        total = self.cash
        for symbol, quantity in self.positions.items():
            total += quantity * prices.get(symbol, 0)
        return total

    def get_summary(self) -> Dict:
        """Get portfolio summary."""
        return {
            "cash": self.cash,
            "positions": self.positions.copy(),
            "total_trades": len(self.trades),
        }
