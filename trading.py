from ib_insync import IB, Stock, MarketOrder
import pandas as pd
import joblib
import os

# Initialize IB instance
ib = IB()


def start_trading_bot(ticker: str):
    """Basic live trading loop using a pre-trained model."""
    contract = Stock(ticker, "SMART", "USD")
    ib.connect("127.0.0.1", 7497, clientId=1)
    model = joblib.load("models/model.pkl")

    def on_tick(tick):
        try:
            df = pd.DataFrame([{
                "Open": tick.price,
                "High": tick.price,
                "Low": tick.price,
                "Close": tick.price,
                "Volume": tick.size,
                "date": pd.Timestamp.now()
            }]).set_index("date")
            df = df.assign(hour=df.index.hour)
            features = ["Open", "High", "Low", "Close", "Volume", "hour"]
            pred = model.predict(df[features])[0]
            if pred == 1:
                ib.placeOrder(contract, MarketOrder("BUY", 1))
            elif pred == 0:
                ib.placeOrder(contract, MarketOrder("SELL", 1))
        except Exception as exc:
            print(f"Trading error: {exc}")

    ib.reqMktData(contract, "", False, False, None)
    ib.pendingTickersEvent += on_tick
    ib.run()


def stop_trading_bot():
    ib.disconnect()


def self_improve_model(new_data):
    features = [
        "trend_macd",
        "momentum_rsi",
        "volatility_bbm",
        "volatility_bbh",
        "volatility_bbl",
        "hour",
    ]
    model = joblib.load("models/model.pkl")

    if os.path.exists("data/historical_data.csv"):
        data = pd.read_csv(
            "data/historical_data.csv", parse_dates=True, index_col="date"
        )
    else:
        data = pd.DataFrame(columns=new_data.columns)
    data = pd.concat([data, new_data])
    data.to_csv("data/historical_data.csv")

    X = data[features]
    y = data["target"]
    model.fit(X, y)
    joblib.dump(model, "models/model.pkl")
