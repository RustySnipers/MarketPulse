from ib_insync import IB, Stock
import pandas as pd
import joblib

from discord_webhook import send_discord_message

# Initialize IB instance
ib = IB()

def start_trading_bot(ticker):
    ib.connect('127.0.0.1', 7497, clientId=1)
    stock = Stock(ticker, 'SMART', 'USD')
    # Implement trading logic here
    send_discord_message(f"Trading started for {ticker}")

def stop_trading_bot():
    ib.disconnect()
    send_discord_message("Trading stopped")

def self_improve_model(new_data):
    features = ['trend_macd', 'momentum_rsi', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'hour']
    model = joblib.load('models/model.pkl')
    
    data = pd.read_csv('data/historical_data.csv', parse_dates=True, index_col='date')
    data = data.append(new_data)
    data.to_csv('data/historical_data.csv')
    
    X = data[features]
    y = data['target']
    model.fit(X, y)
    joblib.dump(model, 'models/model.pkl')
    send_discord_message("Model updated with new data")
