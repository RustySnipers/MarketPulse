import pandas as pd
import numpy as np
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import datetime
import os

def load_data(file_path):
    data = pd.read_csv(file_path)
    print(f"Loaded data columns: {data.columns}")
    if 'Date' in data.columns:
        data.rename(columns={'Date': 'date'}, inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data['Volume'] = data['Volume'].str.replace(',', '').astype(float)
    data = add_all_ta_features(data, open="Open", high="High", low="Low", close="Close", volume="Volume")
    data['hour'] = data.index.hour
    return data

def prepare_ml_training(data):
    features = ['trend_macd', 'momentum_rsi', 'volatility_bbm', 'volatility_bbh', 'volatility_bbl', 'hour']
    target = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)
    X = data[features]
    y = target
    return X, y

def train_local_llm(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, 'models/llm_model.pkl')
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)
    return model, accuracy, conf_matrix, class_report

def generate_training_report(accuracy, conf_matrix, class_report):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f'reports/training_report_{timestamp}.txt'
    with open(report_filename, 'w') as f:
        f.write(f"Training Report:\n\nAccuracy: {accuracy:.2f}\n\n")
        f.write(f"Confusion Matrix:\n{conf_matrix}\n\n")
        f.write(f"Classification Report:\n{class_report}\n")
    print(f"Training completed. Report generated in {report_filename}")

if __name__ == "__main__":
    file_path = 'data/SPY2324.csv'
    data = load_data(file_path)
    X, y = prepare_ml_training(data)
    model, accuracy, conf_matrix, class_report = train_local_llm(X, y)
    generate_training_report(accuracy, conf_matrix, class_report)
