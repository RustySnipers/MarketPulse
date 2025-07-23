import datetime
import os
import backtrader as bt
import joblib
from discord_webhook import send_discord_message
from settings import load_settings
from utils.ml_utils import load_data

def generate_report(cerebro, data, report_filename):
    """Generates a performance report from backtesting results."""
    portfolio = cerebro.broker.getvalue()
    returns = data["Close"].pct_change().dropna()
    sharpe = (returns.mean() / returns.std()) * (252 ** 0.5) if returns.std() != 0 else 0
    downside = returns[returns < 0]
    sortino = (returns.mean() / downside.std()) * (252 ** 0.5) if not downside.empty and downside.std() != 0 else 0
    running_max = data["Close"].cummax()
    drawdown = (data["Close"] - running_max) / running_max
    max_drawdown = drawdown.min()
    total_return = (portfolio / cerebro.broker.startingcash) - 1

    report_content = f"""# Backtesting Report

**Total Return:** {total_return:.2%}

| Metric        | Value      |
|---------------|------------|
| Sharpe Ratio  | {sharpe:.2f}   |
| Sortino Ratio | {sortino:.2f}  |
| Max Drawdown  | {max_drawdown:.2%} |
| Final Portfolio Value | ${portfolio:,.2f} |

"""
    os.makedirs("reports", exist_ok=True)
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Backtesting report generated at {report_filename}")

class MLStrategy(bt.Strategy):
    params = dict(
        model=None,
        features=None
    )

    def __init__(self):
        if not self.p.model or not self.p.features:
            raise ValueError("Model and features must be provided to the strategy.")
        self.dataclose = self.datas[0].close

    def next(self):
        # Create a DataFrame for the current row
        current_data = {
            'Open': self.datas[0].open[0],
            'High': self.datas[0].high[0],
            'Low': self.datas[0].low[0],
            'Close': self.datas[0].close[0],
            'Volume': self.datas[0].volume[0]
        }
        df = pd.DataFrame([current_data])
        df = add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume")
        df["hour"] = self.datas[0].datetime.datetime(0).hour

        if all(f in df.columns for f in self.p.features):
            prediction = self.p.model.predict(df[self.p.features])[0]
            if prediction == 1 and not self.position:
                self.buy()
            elif prediction == 0 and self.position:
                self.sell()

def run_backtest():
    settings = load_settings()
    file_path = settings.get("data_file", "data/SPY2324.csv")

    try:
        model = joblib.load("models/model.pkl")
    except FileNotFoundError:
        print("Model file not found. Please train the model first.")
        send_discord_message("Backtesting failed: Model not found.")
        return

    data = load_data(file_path)

    # Ensure data is in a backtrader-friendly format
    data_feed = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)

    features = ["trend_macd", "momentum_rsi", "volatility_bbm", "volatility_bbh", "volatility_bbl", "hour"]
    cerebro.addstrategy(MLStrategy, model=model, features=features)

    cerebro.broker.setcash(100000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    cerebro.broker.setcommission(commission=0.001)

    print("Starting backtest...")
    cerebro.run()
    print("Backtest finished.")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/backtesting_report_{timestamp}.md"
    generate_report(cerebro, data, report_filename)

    send_discord_message(f"Backtesting completed. Report generated.")
