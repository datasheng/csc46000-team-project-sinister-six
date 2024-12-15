import yfinance as yf


def yahoo_get_stock_data(symbol, start_date, end_date):
    """
    input: stock symbol/index, start_date, end_date (in YYYY-MM-DD format)
    output: Open Price, Close Price & Volume for that index
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(start=start_date, end=end_date)
        data = history[['Open', 'Close', 'Volume']]
        return data
    except Exception as e:
        print(f"Error fetching data from yfinance API: {e}")
        return None

def yahoo_get_additional_data(symbol):
    """
    Retrieve more comprehensive data for a stock symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "priceToEarningsRatio": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "earningsPerShare": info.get("trailingEps"),
            "beta": info.get("beta"),
            "dividendYield": info.get("dividendYield"),
            "targetMeanPrice": info.get("targetMeanPrice"),
            "bookValue": info.get("bookValue"),
            "priceToBook": info.get("priceToBook"),
            "revenue": info.get("totalRevenue"),
            "grossProfit": info.get("grossProfits"),
            "operatingIncome": info.get("operatingIncome"),
            "totalDebt": info.get("totalDebt"),
            "freeCashFlow": info.get("freeCashflow")
        }
    except Exception as e:
        print(f"Error fetching additional data from yfinance: {e}")
        return None
        
def get_quote_table(symbol):
    """
    Fetch quote table data for a given stock symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        # The `info` attribute contains the quote table and more
        info = ticker.info

        # Extract commonly used quote table fields
        quote_data = {
            "symbol": symbol,
            "ask": info.get("ask"),
            "bid": info.get("bid"),
            "dayHigh": info.get("dayHigh"),
            "dayLow": info.get("dayLow"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "previousClose": info.get("previousClose"),
            "currentPrice": info.get("regularMarketPrice"),
            "open": info.get("open"),
            "volume": info.get("volume"),
            "marketCap": info.get("marketCap"),
            "beta": info.get("beta"),
        }
        return quote_data
    except Exception as e:
        print(f"Error fetching quote table data: {e}")
        return None

def yahoo_by_period(symbol, period):
    """
    input: stock symbol, period
    output: Open Price, Close Price, Volume in the past period or interval (from current date)
    example func call: yahoo_by_period('SPY', '1y')
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval='1d')
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
