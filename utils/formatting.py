def format_symbol_for_tradingview(symbol: str) -> str:
    """
    Formats a ticker symbol for use in a TradingView URL.
    - Adds exchange prefixes for common exchanges.
    - Converts to uppercase.
    """
    symbol = symbol.upper()
    # This is a simplified example. A more robust solution would involve
    # a more comprehensive mapping of symbols to exchanges.
    if symbol in ["AAPL", "GOOG", "MSFT", "AMZN", "META"]:
        return f"NASDAQ:{symbol}"
    elif symbol in ["SPY", "QQQ", "DIA"]:
        return f"AMEX:{symbol}"
    else:
        return symbol
