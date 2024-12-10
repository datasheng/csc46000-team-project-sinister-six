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

def yahoo_past_year(symbol):
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period='1y', interval='1d')
        data = history[['Open', 'Close', 'Volume']]
        return data
    except Exception as e:
        print(f"Error fetching data from yfinance API: {e}")
        return None


if __name__ == "__main__":
    print(yahoo_get_stock_data("SPY", "2018-01-01", "2018-12-31"))

# may be useful:
# valid intervals you can use are:
# 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo