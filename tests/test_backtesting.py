import pandas as pd
import sys
from pathlib import Path

# Ensure the repository root is in sys.path so we can import backtesting.py
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import backtesting


def test_load_data_volume_and_hour(tmp_path):
    # create sample DataFrame with at least 10 rows for ta features
    start = pd.Timestamp("2023-01-01 09:30")
    rows = []
    for i in range(30):
        ts = start + pd.Timedelta(hours=i)
        rows.append({
            "Date": ts.strftime("%Y-%m-%d %H:%M"),
            "Open": 100 + i,
            "High": 110 + i,
            "Low": 90 + i,
            "Close": 105 + i,
            "Volume": f"{1000 * (i+1):,}"
        })
    df_in = pd.DataFrame(rows)

    file_path = tmp_path / "sample.csv"
    df_in.to_csv(file_path, index=False)

    df = backtesting.load_data(Path(file_path))

    assert pd.api.types.is_float_dtype(df["Volume"])
    expected_hours = [(start + pd.Timedelta(hours=i)).hour for i in range(30)]
    assert list(df.index.hour)[:30] == expected_hours
