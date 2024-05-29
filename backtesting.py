import pandas as pd
import numpy as np
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import backtrader as bt

# Load and preprocess historical data
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=True, index_col='date')
    data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")

    # Convert 'Volume' column to numeric, coercing errors to NaN
    data['Volume'] = pd.to_numeric(data['Volume'].str.replace(',', ''), errors='coerce')

    # Fill NaN values with zero
    data['Volume'].fillna(0, inplace=True)

    data['hour'] = data.index.hour
    return data

def perform_backtest(data):
    features = ['trend_macd', 'momentum_rsi', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'hour']
    data['target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(data[features], data['target'], test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'models/model.pkl')
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    results = {
        'model': model,
        'accuracy': accuracy,
        'features': features
    }
    
    return results

def generate_report(results):
    report = f"Backtesting Report:\n\nAccuracy: {results['accuracy']:.2f}\n\nOptimal Settings: ...\nTrading Plan: ..."
    with open('reports/backtesting_report.txt', 'w') as f:
        f.write(report)

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
    file_path = 'data/SPY2324.csv'
    data = load_data(file_path)
    results = perform_backtest(data)
    generate_report(results)
    print("Backtesting completed. Report generated in reports/backtesting_report.txt")
