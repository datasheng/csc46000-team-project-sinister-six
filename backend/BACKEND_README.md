### Documentation for all Flask routes
#### Endpoints:
- /get_stocks
- /get_stocks_db
- /get_stocks_past_period
- /store_past_period
- /query_llm
- /query_llm_news

## get_stocks (GET)
Parameters:
- index
- start
- end </br>

Example: 
`/get_stocks?index=VOO&start=2021-01-01&end=2021-12-31` </br>

Returns: Stock data of given stock index. Includes columns Date, Open, Close/Last, Volume, High, Low


## get_stocks_db (GET)
Parameters:
- index
- start (optional)
- end (optional)

Example:
`/get_stocks_db?index=RSP&start=2024-11-01&end=2024-11-05`

Returns: Stock data from Supabase's DB, time constraints are optional and can be used when needed.
Otherwise, returns the entire table.

## get_stocks_past_year (GET)
Parameters:
- index
- period

Example:
`/get_stocks_past_year?index=VOO&period=6mo`
Note: Allowed periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

Returns: Stock data directly from yfinance API for the past period since current date

## store_past_period (POST)
Parameters:
- index
- period

Example:
`/store_past_period?index=SPY&period=3mo`

Returns: Success or failure response. Stores specific period of data into postgres DB, retrieved from yfinance API

## query_llm (GET)
Parameters:
- query
- index

Example:
`/query_llm?query=Tell me about Voo stock prices&index=voo`

Returns: LLM (OpenAI) response based on postgresql data on the stock

## query_llm_news (GET)
Parameters: 
- query
- index

Example: 
`/query_llm_news?query=What's the latest news on the stock Voo?&index=voo`

Returns: LLM (OpenAI) response based on Finnhub Stock News API
