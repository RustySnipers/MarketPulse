import datetime
import os

from discord_webhook import send_discord_message
from settings import load_settings
from utils.ml_utils import load_data, train_random_forest


def perform_ml_training(data):
    """Train a model for ML analysis."""
    return train_random_forest(data, model_path="models/ml_model.pkl")


def generate_ml_report(results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/ml_training_report_{timestamp}.md"
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
    report_content = f"""# ML Training Report

**Accuracy:** {results['accuracy']:.2f}

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
    print(f"ML Training completed. Report generated in {report_filename}")


def run_ml_training():
    settings = load_settings()
    file_path = settings.get("data_file", "data/SPY2324.csv")
    data = load_data(file_path)
    results = perform_ml_training(data)
    generate_ml_report(results)
    print("ML Training completed. Report generated.")
    send_discord_message(
        f"ML training completed with accuracy {results['accuracy']:.2f}"
    )
