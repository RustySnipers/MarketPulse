import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
import pytest
import backtesting

# Dummy function to avoid heavy computations in tests

def _dummy_add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume"):
    return df


def test_load_data(monkeypatch, tmp_path):
    # Prepare a small CSV file
    df = pd.DataFrame({
        'Date': ['2024-05-21 10:00:00', '2024-05-21 11:00:00', '2024-05-21 12:00:00'],
        'Open': [1, 2, 3],
        'High': [1, 2, 3],
        'Low': [1, 2, 3],
        'Close': [1, 2, 3],
        'Volume': ['1,000', '2,000', '3,000']
    })
    csv_file = tmp_path / "sample.csv"
    df.to_csv(csv_file, index=False)

    # Patch technical indicator generation
    monkeypatch.setattr(backtesting, "add_all_ta_features", _dummy_add_all_ta_features)

    result = backtesting.load_data(csv_file)

    # Volume column should be numeric
    assert pd.api.types.is_numeric_dtype(result['Volume'])

    # Hour column should exist and match expected hours
    assert 'hour' in result.columns
    assert result['hour'].tolist() == [10, 11, 12]
