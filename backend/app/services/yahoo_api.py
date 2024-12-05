import yfinance as yf


def yahoo_get_stock_data(symbol, start_date, end_date):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(start=start_date, end=end_date)
        data = history[['Open', 'Close', 'Volume']]
        return data
    except Exception as e:
        print(f"Error fetching data from yfinance API: {e}")
        return None
