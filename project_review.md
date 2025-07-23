# Project Review: Market Pulse

This document outlines identified bugs, unfinished features, and areas for improvement in the Market Pulse application. Issues are categorized by severity to guide development efforts.

## Completed Issues

### 1. **Fatal Error in Live Trading Due to Mismatched ML Model Features**
- **Severity:** Critical
- **Status:** **Fixed**
- **File:** `trading.py`
- **Description:** The live trading `on_tick` function was creating a pandas DataFrame with features that did not match what the machine learning model was trained on.
- **Resolution:** The `on_tick` function was updated to calculate the correct technical analysis features before making predictions.

### 2. **Backtesting Module Not Implemented**
- **Severity:** High
- **Status:** **Fixed**
- **File:** `backtesting.py`
- **Description:** The backtesting module was not performing a proper backtest and was instead retraining the model on the test data.
- **Resolution:** The `run_backtest` function was refactored to use the `backtrader` library with a pre-trained model to simulate a realistic backtest.

### 3. **Unsafe Credential Storage**
- **Severity:** High
- **Status:** **Fixed**
- **File:** `gui.py`, `webull_integration.py`, `tradingview_integration.py`
- **Description:** Usernames were being stored in plain text in the settings file.
- **Resolution:** The application now stores usernames in the system keychain, alongside passwords, for improved security.

### 4. **Inefficient Per-Tick DataFrame Creation**
- **Severity:** High
- **Status:** **Fixed**
- **File:** `trading.py`
- **Description:** The live trading module was creating a new pandas DataFrame for every market tick, leading to high memory usage.
- **Resolution:** The trading module now maintains a rolling window of tick data, which is much more memory-efficient.

## High-Severity Issues

### 1. **No Error Handling for IB TWS Connection**
- **Severity:** Medium
- **File:** `trading.py`, line 19
- **Description:** The `start_trading_bot` function attempts to connect to Interactive Brokers TWS without any error handling. If TWS is not running or the connection fails for any other reason, the application will crash.
- **Suggested Solution:** Wrap the `ib.connect()` call in a `try...except` block to gracefully handle connection errors and provide feedback to the user.

## Medium-Severity Issues

### 1. **Multiple Trading Threads Can Be Started**
- **Severity:** Medium
- **File:** `gui.py`, line 133
- **Description:** The "Start Trading" button can be clicked multiple times, which will start multiple trading threads for the same ticker. This can lead to unexpected behavior and conflicting orders.
- **Suggested Solution:** Disable the "Start Trading" button after it has been clicked and re-enable it only after trading has stopped.

### 2. **Unused `self_improve_model` Function**
- **Severity:** Medium
- **File:** `trading.py`, line 51
- **Description:** The `self_improve_model` function is defined but is never called anywhere in the application. This represents unfinished or dead code.
- **Suggested Solution:** Either implement a feature that uses this function (e.g., a button in the GUI to trigger model retraining) or remove the function if it is not intended to be used.

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
