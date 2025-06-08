import pandas as pd
from functools import lru_cache
from ta import add_all_ta_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

@lru_cache(maxsize=4)
def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data and compute TA features. Cached for efficiency."""
    data = pd.read_csv(file_path)
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


def train_random_forest(data: pd.DataFrame, model_path: str = "models/model.pkl"):
    """Train RandomForest on common features and save model."""
    features = [
        "trend_macd",
        "momentum_rsi",
        "volatility_bbm",
        "volatility_bbh",
        "volatility_bbl",
        "hour",
    ]
    data["target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        data[features], data["target"], test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    if model_path:
        joblib.dump(model, model_path)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    return {"model": model, "accuracy": accuracy, "features": features}
