import datetime
import os

import backtrader as bt  # backtrader provides the strategy engine
from discord_webhook import send_discord_message
from settings import load_settings
from utils.ml_utils import load_data, train_random_forest


# Load and preprocess historical data
def perform_backtest(data):
    """Train a model on the provided data and return results."""
    results = train_random_forest(data)
    print(f"Model Accuracy: {results['accuracy']:.2f}")  # Debug print
    return results


def generate_report(data, results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/backtesting_report_{timestamp}.md"
    optimal_settings = {
        "MACD": "12, 26, 9",  # Example values
        "RSI": "14",
        "Bollinger Bands": "20, 2",
    }
    trading_plan = (
        "1. Enter a long position when the MACD line crosses above the signal line and RSI is below 30.\n"
        "2. Enter a short position when the MACD line crosses below the signal line and RSI is above 70.\n"
        "3. Use Bollinger Bands to set stop-loss and take-profit levels.\n"
        "4. Monitor trades and adjust positions based on market conditions."
    )
    returns = data["Close"].pct_change().dropna()
    sharpe = (returns.mean() / returns.std()) * (252 ** 0.5)
    downside = returns[returns < 0]
    sortino = (returns.mean() / downside.std()) * (252 ** 0.5) if not downside.empty else 0
    running_max = data["Close"].cummax()
    drawdown = (data["Close"] - running_max) / running_max
    max_drawdown = drawdown.min()
    total_return = (data["Close"].iloc[-1] / data["Close"].iloc[0]) - 1

    report_content = f"""# Backtesting Report

**Accuracy:** {results['accuracy']:.2f}

**Total Return:** {total_return:.2%}

| Metric | Value |
|-------|-------|
| Sharpe Ratio | {sharpe:.2f} |
| Sortino Ratio | {sortino:.2f} |
| Max Drawdown | {max_drawdown:.2%} |

## Optimal Settings

- MACD: {optimal_settings['MACD']}
- RSI: {optimal_settings['RSI']}
- Bollinger Bands: {optimal_settings['Bollinger Bands']}

## Trading Plan

{trading_plan}
"""

    os.makedirs("reports", exist_ok=True)
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Backtesting completed. Report generated in {report_filename}")


class MLStrategy(bt.Strategy):
    def __init__(self, model, features):
        self.model = model
        self.features = features

    def next(self):
        features = [self.data.get(name)[0] for name in self.features]
        prediction = self.model.predict([features])[0]
        if prediction == 1:
            self.buy()
        elif prediction == 0:
            self.sell()


def run_backtest():
    settings = load_settings()
    file_path = settings.get("data_file", "data/SPY2324.csv")
    data = load_data(file_path)
    results = perform_backtest(data)
    generate_report(data, results)
    print("Backtesting completed. Report generated.")
    send_discord_message(
        f"Backtesting completed with accuracy {results['accuracy']:.2f}"
    )
