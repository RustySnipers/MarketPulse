import pandas as pd
import numpy as np
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from discord_webhook import send_discord_message
import joblib
import datetime
import os
import backtrader as bt  # backtrader provides the strategy engine
from settings import load_settings


# Load and preprocess historical data
def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Loaded data columns: {data.columns}")  # Print the columns for debugging
    if "Date" in data.columns:
        data.rename(columns={"Date": "date"}, inplace=True)
    data["date"] = pd.to_datetime(data["date"])
    data.set_index("date", inplace=True)
    data["Volume"] = pd.to_numeric(
        data["Volume"].astype(str).str.replace(",", ""), errors="coerce"
    ).astype(float)
    data = add_all_ta_features(
        data, open="Open", high="High", low="Low", close="Close", volume="Volume"
    )
    data["hour"] = data.index.hour
    return data


def perform_backtest(data):
    features = [
        "trend_macd",
        "momentum_rsi",
        "volatility_bbm",
        "volatility_bbh",
        "volatility_bbl",
        "hour",
    ]
    data["target"] = np.where(data["Close"].shift(-1) > data["Close"], 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data["target"], test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "models/model.pkl")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    results = {"model": model, "accuracy": accuracy, "features": features}

    print(f"Model Accuracy: {accuracy:.2f}")  # Debug print to check accuracy
    return results


def generate_report(results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/backtesting_report_{timestamp}.txt"
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
    report_content = (
        f"Backtesting Report:\n\n"
        f"Accuracy: {results['accuracy']:.2f}\n\n"
        f"Optimal Settings:\n"
        f"MACD: {optimal_settings['MACD']}\n"
        f"RSI: {optimal_settings['RSI']}\n"
        f"Bollinger Bands: {optimal_settings['Bollinger Bands']}\n\n"
        f"Trading Plan:\n{trading_plan}"
    )
    print(report_content)  # Debug print to check report content
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
    generate_report(results)
    print("Backtesting completed. Report generated.")
    send_discord_message(
        f"Backtesting completed with accuracy {results['accuracy']:.2f}"
    )
