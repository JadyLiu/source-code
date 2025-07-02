# Financial Trading Demo

A concise Python-based financial trading system designed to demonstrate AI coding capabilities for investment management and algorithmic trading.

## 🎯 Purpose

This codebase serves as a demonstration platform for showcasing AI-powered development tools in the financial sector. It provides a complete yet simple trading system that investment firms can easily understand and extend.

## 🏗️ Architecture

```
financial-demo/
├── portfolio.py          # Portfolio management and position tracking
├── strategies.py         # Trading strategies (MA, RSI, Momentum)
├── risk_manager.py       # Risk calculations and position sizing
├── back_tester.py         # Strategy backtesting engine
├── data_loader.py        # Market data generation and loading
└── README.md            # This file
```

## 🚀 Quick Start

### Basic Usage

```python
from portfolio import Portfolio
from strategies import MovingAverageStrategy
from data_loader import DataLoader
from backtester import Backtester

# Create portfolio
portfolio = Portfolio(initial_cash=100000)

# Load market data
data_loader = DataLoader()
data = data_loader.generate_sample_data('AAPL', days=252)

# Define strategy
strategy = MovingAverageStrategy(short_window=10, long_window=30)

# Run backtest
backtester = Backtester(initial_cash=100000)
results = backtester.run_backtest(data, strategy, 'AAPL')

# View results
print(backtester.generate_report())
```

### Live Trading Simulation

```python
# Manual trading
portfolio = Portfolio(50000)
portfolio.buy('AAPL', 100, 150.0)
portfolio.sell('AAPL', 50, 160.0)

print(f"Portfolio Value: ${portfolio.get_total_value({'AAPL': 155.0}):,.2f}")
```

## 📊 Features

### Portfolio Management
- **Position Tracking**: Real-time portfolio positions and cash balance
- **Trade Execution**: Buy/sell orders with automatic validation
- **Performance Metrics**: Portfolio value calculation and trade history

### Trading Strategies
- **Moving Average Crossover**: Classic technical analysis strategy
- **RSI Strategy**: Relative Strength Index overbought/oversold signals
- **Momentum Strategy**: Price momentum-based trading decisions

### Risk Management
- **Position Sizing**: Automatic calculation based on risk parameters
- **Portfolio Limits**: Maximum position size and risk per trade
- **Risk Metrics**: VaR, Sharpe ratio, maximum drawdown calculations

### Backtesting Engine
- **Historical Analysis**: Test strategies against historical data
- **Performance Reports**: Comprehensive trading statistics
- **Risk Analytics**: Drawdown analysis and win rate calculations

## 📈 Example Output

```
BACKTEST RESULTS
================
Initial Capital: $100,000.00
Final Value: $112,450.00
Total Return: 12.45%
Total Trades: 28

RISK METRICS
============
Sharpe Ratio: 1.234
Maximum Drawdown: 8.50%
Value at Risk (5%): -2.10%
Win Rate: 64.29%
```

## 🛠️ AI Development Opportunities

This codebase is designed to showcase AI coding capabilities in several areas:

### Code Understanding
- **Strategy Analysis**: AI can analyze existing trading logic and explain strategy mechanics
- **Risk Assessment**: Understanding risk management rules and portfolio constraints
- **Performance Evaluation**: Interpreting backtest results and identifying improvement opportunities

### Code Generation
- **New Strategies**: Generate additional trading algorithms (MACD, Bollinger Bands, etc.)
- **Risk Enhancements**: Create advanced risk management features
- **Data Integration**: Add real-time market data connections
- **Optimization**: Generate parameter optimization routines

### Testing & Validation
- **Unit Tests**: Expand test coverage for edge cases
- **Integration Tests**: Create comprehensive strategy validation
- **Performance Tests**: Generate stress testing scenarios

### Operations & Deployment
- **Monitoring**: Add logging and alerting systems
- **Configuration**: Create parameter management systems
- **Reporting**: Generate automated performance reports

## 🎛️ Configuration

Key parameters can be adjusted for different risk profiles:

```python
# Conservative setup
portfolio = Portfolio(initial_cash=100000)
risk_manager = RiskManager(
    max_position_size=0.05,    # 5% max position
    max_portfolio_risk=0.01    # 1% max risk per trade
)

# Aggressive setup
risk_manager = RiskManager(
    max_position_size=0.20,    # 20% max position
    max_portfolio_risk=0.05    # 5% max risk per trade
)
```

No external API keys or market data subscriptions required - includes synthetic data generation for testing.

## 🧪 Testing

Run the test suite:

```bash
python -m unittest test_portfolio.py
```
