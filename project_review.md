# Project Review: Market Pulse

This document outlines identified bugs, unfinished features, and areas for improvement in the Market Pulse application. Issues are categorized by severity to guide development efforts.

## Critical Issues

### 1. **Fatal Error in Live Trading Due to Mismatched ML Model Features**
- **Severity:** Critical
- **File:** `trading.py`, line 35
- **Description:** The live trading `on_tick` function creates a pandas DataFrame with features `["Open", "High", "Low", "Close", "Volume", "hour"]`. However, the machine learning model (`models/model.pkl`) was trained on a different set of features (e.g., `trend_macd`, `momentum_rsi`). This mismatch will cause the application to crash with a `ValueError` as soon as the model attempts to make a prediction.
- **Suggested Solution:** The `on_tick` function needs to be updated to calculate the same features that the model was trained on. This will likely involve using a library like `ta` to calculate technical indicators from the incoming tick data.

## High-Severity Issues

### 1. **Backtesting Module Not Implemented**
- **Severity:** High
- **File:** `backtesting.py`
- **Description:** The `run_backtest` function does not perform a proper backtest. It trains a new model on the entire historical dataset and then calculates performance metrics on that same data, which is a form of data leakage. The `MLStrategy` class, which appears intended for use with the `backtrader` library, is never actually used.
- **Suggested Solution:** Refactor `run_backtest` to use `backtrader` with the `MLStrategy`. The function should take a pre-trained model and a dataset for backtesting (ideally, a hold-out set not used during training).

### 2. **Inefficient Per-Tick DataFrame Creation**
- **Severity:** High
- **File:** `trading.py`, line 28
- **Description:** The `on_tick` function in the live trading module creates a new pandas DataFrame for every single market tick. This is extremely inefficient and will lead to high memory usage and poor performance, especially in active markets.
- **Suggested Solution:** Instead of creating a new DataFrame on each tick, append the new tick data to an existing DataFrame and keep a rolling window of data. This will be much more performant.

### 3. **Unsafe Credential Storage**
- **Severity:** High
- **File:** `gui.py`, line 192
- **Description:** Usernames for Webull and TradingView are stored in the main settings file in plain text. While passwords are saved to the system keychain, storing usernames in an unencrypted file is a security risk.
- **Suggested Solution:** Store usernames in the system keychain along with the passwords.

## Medium-Severity Issues

### 1. **No Error Handling for IB TWS Connection**
- **Severity:** Medium
- **File:** `trading.py`, line 19
- **Description:** The `start_trading_bot` function attempts to connect to Interactive Brokers TWS without any error handling. If TWS is not running or the connection fails for any other reason, the application will crash.
- **Suggested Solution:** Wrap the `ib.connect()` call in a `try...except` block to gracefully handle connection errors and provide feedback to the user.

### 2. **Multiple Trading Threads Can Be Started**
- **Severity:** Medium
- **File:** `gui.py`, line 133
- **Description:** The "Start Trading" button can be clicked multiple times, which will start multiple trading threads for the same ticker. This can lead to unexpected behavior and conflicting orders.
- **Suggested Solution:** Disable the "Start Trading" button after it has been clicked and re-enable it only after trading has stopped.

### 3. **Unused `self_improve_model` Function**
- **Severity:** Medium
- **File:** `trading.py`, line 51
- **Description:** The `self_improve_model` function is defined but is never called anywhere in the application. This represents unfinished or dead code.
- **Suggested Solution:** Either implement a feature that uses this function (e.g., a button in the GUI to trigger model retraining) or remove the function if it is not intended to be used.

## Low-Severity Issues

### 1. **Blocking GUI Calls**
- **Severity:** Low
- **File:** `gui.py`
- **Description:** The use of `simpledialog` and `messagebox` can block the main GUI thread. For a simple application, this is acceptable, but it can lead to a non-responsive UI during these operations.
- **Suggested Solution:** For a more advanced implementation, custom non-blocking dialogs could be created. For now, this is a low-priority issue.

### 2. **Monolithic GUI Class**
- **Severity:** Low
- **File:** `gui.py`
- **Description:** The `TradingBotApp` class is very large and handles all aspects of the GUI. This makes the code harder to read and maintain.
- **Suggested Solution:** Refactor the `TradingBotApp` class by breaking it down into smaller, more focused components. For example, the Webull, TradingView, and backtesting sections could each be their own classes.
