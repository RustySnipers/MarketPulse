from ib_insync import IB, Stock, MarketOrder
import pandas as pd
import joblib
import os
from ta import add_all_ta_features

# Initialize IB instance
ib = IB()
ticks_df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
ticks_df.index.name = "date"


def start_trading_bot(ticker: str):
    """Basic live trading loop using a pre-trained model."""
    global ticks_df
    ticks_df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    ticks_df.index.name = "date"

    contract = Stock(ticker, "SMART", "USD")
    try:
        ib.connect("127.0.0.1", 7497, clientId=1)
    except Exception as e:
        print(f"Failed to connect to IB TWS: {e}")
        return

    model = joblib.load("models/model.pkl")

    def on_tick(tick):
        global ticks_df
        try:
            new_tick = pd.DataFrame([{
                "Open": tick.price,
                "High": tick.price,
                "Low": tick.price,
                "Close": tick.price,
                "Volume": tick.size,
            }], index=[pd.Timestamp.now()])

            ticks_df = pd.concat([ticks_df, new_tick])

            # Keep the last 100 ticks to avoid memory issues
            if len(ticks_df) > 100:
                ticks_df = ticks_df.iloc[-100:]

            # Need at least some data to calculate indicators
            if len(ticks_df) > 20:
                # Calculate technical analysis features
                df_ta = add_all_ta_features(
                    ticks_df, open="Open", high="High", low="Low", close="Close", volume="Volume"
                )
                df_ta["hour"] = df_ta.index.hour

                features = ["trend_macd", "momentum_rsi", "volatility_bbm", "volatility_bbh", "volatility_bbl", "hour"]

                # Ensure all features are present
                if all(feature in df_ta.columns for feature in features):
                    last_row = df_ta.iloc[[-1]]
                    pred = model.predict(last_row[features])[0]
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
    if ib.isConnected():
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
