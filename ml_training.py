import pandas as pd
import numpy as np
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import datetime
import os

def load_data(file_path):
    data = pd.read_csv(file_path)
    if 'Date' in data.columns:
        data.rename(columns={'Date': 'date'}, inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data['Volume'] = data['Volume'].str.replace(',', '').astype(float)
    data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
    data['hour'] = data.index.hour
    return data

def perform_ml_training(data):
    features = ['trend_macd', 'momentum_rsi', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'hour']
    data['target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(data[features], data['target'], test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'models/ml_model.pkl')
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    results = {
        'model': model,
        'accuracy': accuracy,
        'features': features
    }
    
    return results

def generate_ml_report(results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = 'reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = os.path.join(report_dir, f'ml_training_report_{timestamp}.txt')
    optimal_settings = {
        'MACD': '12, 26, 9',  # Example values
        'RSI': '14',
        'Bollinger Bands': '20, 2'
    }
    trading_plan = (
        "1. Enter a long position when the MACD line crosses above the signal line and RSI is below 30.\n"
        "2. Enter a short position when the MACD line crosses below the signal line and RSI is above 70.\n"
        "3. Use Bollinger Bands to set stop-loss and take-profit levels.\n"
        "4. Monitor trades and adjust positions based on market conditions."
    )
    report_content = (
        f"ML Training Report:\n\n"
        f"Accuracy: {results['accuracy']:.2f}\n\n"
        f"Optimal Settings:\n"
        f"MACD: {optimal_settings['MACD']}\n"
        f"RSI: {optimal_settings['RSI']}\n"
        f"Bollinger Bands: {optimal_settings['Bollinger Bands']}\n\n"
        f"Trading Plan:\n{trading_plan}"
    )
    with open(report_filename, 'w') as f:
        f.write(report_content)
    print(f"ML Training completed. Report generated in {report_filename}")

def run_ml_training():
    file_path = 'data/SPY2324.csv'
    data = load_data(file_path)
    results = perform_ml_training(data)
    generate_ml_report(results)
    print("ML Training completed. Report generated.")
