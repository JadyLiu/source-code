import pandas as pd
from typing import Dict, List, Any
from source.portfolio import Portfolio
from source.risk_manager import RiskManager


class Backtester:
    """Simple backtesting engine for trading strategies."""

    def __init__(self, initial_cash: float = 100000, commission: float = 1.0) -> None:
        self.initial_cash = initial_cash
        self.commission = commission
        self.results: Dict[str, Any] = {}

    def run_backtest(
        self, data: pd.DataFrame, strategy: Any, symbol: str
    ) -> Dict[str, Any]:
        """Run backtest for given strategy and data."""
        portfolio = Portfolio(self.initial_cash)
        risk_manager = RiskManager()

        portfolio_values = [self.initial_cash]
        trades = []
        position = 0  # Current position: 0=neutral, 1=long, -1=short

        prices = data["close"].tolist()

        for i in range(len(data)):
            current_price = data.iloc[i]["close"]

            # Get strategy signal
            if hasattr(strategy, "get_signal"):
                signal = strategy.get_signal(prices[: i + 1])
            else:
                # For pandas-based strategies
                signals = strategy.calculate_signals(data["close"][: i + 1])
                signal = signals.iloc[-1] if len(signals) > 0 else 0

            # Execute trades based on signal
            if signal == 1 and position <= 0:  # Buy signal
                if position == -1:
                    # Close short position first (not implemented in simple portfolio)
                    pass

                # Calculate position size
                stop_loss = current_price * 0.95  # 5% stop loss
                portfolio_value = portfolio.get_total_value({symbol: current_price})
                quantity = risk_manager.calculate_position_size(
                    portfolio_value, current_price, stop_loss
                )

                if quantity > 0 and portfolio.buy(symbol, quantity, current_price):
                    position = 1
                    trades.append(
                        {
                            "date": data.index[i],
                            "action": "BUY",
                            "price": current_price,
                            "quantity": quantity,
                        }
                    )

            elif signal == -1 and position >= 0:  # Sell signal
                current_quantity = portfolio.positions.get(symbol, 0)
                if current_quantity > 0 and portfolio.sell(
                    symbol, current_quantity, current_price
                ):
                    position = 0
                    trades.append(
                        {
                            "date": data.index[i],
                            "action": "SELL",
                            "price": current_price,
                            "quantity": current_quantity,
                        }
                    )

            # Track portfolio value
            portfolio_value = portfolio.get_total_value({symbol: current_price})
            portfolio_values.append(portfolio_value)

        # Calculate performance metrics
        returns = self._calculate_returns(portfolio_values)

        self.results = {
            "final_value": portfolio_values[-1],
            "total_return": (portfolio_values[-1] - self.initial_cash)
            / self.initial_cash,
            "total_trades": len(trades),
            "portfolio_values": portfolio_values,
            "trades": trades,
            "sharpe_ratio": risk_manager.calculate_sharpe_ratio(returns),
            "max_drawdown": risk_manager.calculate_max_drawdown(portfolio_values),
            "var_5": risk_manager.calculate_var(returns),
            "win_rate": self._calculate_win_rate(trades),
        }

        return self.results

    def _calculate_returns(self, portfolio_values: List[float]) -> List[float]:
        """Calculate daily returns from portfolio values."""
        returns = []
        for i in range(1, len(portfolio_values)):
            daily_return = (
                portfolio_values[i] - portfolio_values[i - 1]
            ) / portfolio_values[i - 1]
            returns.append(daily_return)
        return returns

    def _calculate_win_rate(self, trades: List[Dict]) -> float:
        """Calculate win rate from completed trades."""
        if len(trades) < 2:
            return 0.0

        profitable_trades = 0
        total_completed_trades = 0

        # Match buy and sell trades
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_trade = trades[i] if trades[i]["action"] == "BUY" else trades[i + 1]
                sell_trade = (
                    trades[i + 1] if trades[i + 1]["action"] == "SELL" else trades[i]
                )

                if buy_trade["action"] == "BUY" and sell_trade["action"] == "SELL":
                    profit = (sell_trade["price"] - buy_trade["price"]) * buy_trade[
                        "quantity"
                    ]
                    if profit > 0:
                        profitable_trades += 1
                    total_completed_trades += 1

        return (
            profitable_trades / total_completed_trades
            if total_completed_trades > 0
            else 0.0
        )

    def generate_report(self) -> str:
        """Generate a summary report of backtest results."""
        if not self.results:
            return "No backtest results available. Run backtest first."

        report = f"""
BACKTEST RESULTS
================
Initial Capital: ${self.initial_cash:,.2f}
Final Value: ${self.results["final_value"]:,.2f}
Total Return: {self.results["total_return"]:.2%}
Total Trades: {self.results["total_trades"]}

RISK METRICS
============
Sharpe Ratio: {self.results["sharpe_ratio"]:.3f}
Maximum Drawdown: {self.results["max_drawdown"]:.2%}
Value at Risk (5%): {self.results["var_5"]:.2%}
Win Rate: {self.results["win_rate"]:.2%}
        """

        return report.strip()
