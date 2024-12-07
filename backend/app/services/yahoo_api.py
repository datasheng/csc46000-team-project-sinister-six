import yfinance as yf


def yahoo_get_stock_data(symbol, start_date, end_date):
    # ALL stock data between start_date and end_date
    # returns just attributes Open price, Close price, and volume
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(start=start_date, end=end_date)
        data = history[['Open', 'Close', 'Volume']]
        return data
    except Exception as e:
        print(f"Error fetching data from yfinance API: {e}")
        return None

if __name__ == "__main__":
    print(yahoo_get_stock_data("SPY", "2018-01-01", "2018-12-31"))