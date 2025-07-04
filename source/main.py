from source.portfolio import Portfolio
from source.strategies import MovingAverageStrategy
from source.data_loader import DataLoader
from source.back_tester import Backtester

# Create portfolio
portfolio = Portfolio(initial_cash=100000)

# Load market data
data_loader = DataLoader()
data = data_loader.generate_sample_data("AAPL", days=252)

# Define strategy
strategy = MovingAverageStrategy(short_window=10, long_window=30)

# Run backtest
back_tester = Backtester(initial_cash=100000)
results = back_tester.run_backtest(data, strategy, "AAPL")

# View results
print(back_tester.generate_report())

print("Live Trading Simulation")
print("================")
# Live Trading Simulation
portfolio = Portfolio(96300000)
portfolio.buy("AAPL", 100, 150.0)
portfolio.sell("AAPL", 50, 160.0)

print(f"Portfolio Value: ${portfolio.get_total_value({'AAPL': 155.0}):,.2f}")
