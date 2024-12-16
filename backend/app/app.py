from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data, yahoo_by_period
from services.supabase_api import store_data_sb, get_data_all_sb, query_llm_data
from services.utils import process_stock_data
from services.stocks_news_api import get_company_news, get_general_news
from services.chroma_langchain_api import handle_llm_news
import pandas as pd
import requests
from flask_cors import CORS


app = Flask(__name__)
server_ip = 'http://localhost:5000'
CORS(app, origins=["http://localhost:3000","http://127.0.0.1:3000"])


@app.route('/get_stocks', methods=['GET'])
def get_stocks_info():
    """
    USES: yahoo_get_stocks_data()
    inputs: index, start, end (stock symbol/index, start date, end date)
    output: returns json of stock data, previously converted to dataframe format also
    example of api call:
    http://localhost:5000/stocks?index=SPY&start=2021-01-01&end=2021-12-31
    note, sometimes people have different ports. take the one from your terminal/console log
    """
    stock_index = request.args.get('index')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not (stock_index, start_date, end_date):
        return jsonify({"error": "REQUIRED parameters are missing from the API call"}), 400
    response = yahoo_get_stock_data(stock_index, start_date, end_date)
    if response is None or len(response) == 0:
        return jsonify({"error": "Data could not be retrieved"}), 404

    response = pd.DataFrame(response)
    return response.to_json(orient="records"), 200


@app.route('/get_stocks_db', methods=['GET'])
def get_stocks_db():
    """
    USES: get_data_all_sb()
    gets stock data from postgres/supabase backend.
    currently only supports retrieving entire table data. will add option to set a range
    input: stock symbol
           (optional): start date
           (optional): end date
    output:
    """
    stock_index = request.args.get('index')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not stock_index:
        return jsonify({"error": "REQUIRED parameters are missing from the API call"}), 400
    if not start_date and not end_date:  # retrieve all from DB, no time range
        response = get_data_all_sb(stock_index.lower())
        return jsonify(response), 200
    elif start_date and not end_date:
        response = get_data_all_sb(stock_index.lower(), start_date)
        return jsonify(response), 200
    else:  # retrieve based on time range
        response = get_data_all_sb(stock_index.lower(), start_date, end_date)
        return jsonify(response), 200


@app.route('/get_stocks_past_period', methods=['GET'])
def get_stocks_past_year():
    """
    USES: yahoo_by_period()
    input: stock symbol, period from current date
    output: json format of stock symbol's data in the past year
    """
    stock_index = request.args.get('index')
    period = request.args.get('period')
    if not stock_index:
        return jsonify({"error": "REQUIRED parameters are missing from the API call"}), 400
    response = yahoo_by_period(stock_index, period)
    if response is None or len(response) == 0:
        return jsonify({"error": "Data could not be retrieved"}), 404
    response = pd.DataFrame(response)
    response.reset_index(inplace=True)
    return response.to_json(orient="records"), 200


@app.route('/store_past_period', methods=['POST'])
def store_past_period():
    """
    USES: yahoo_by_period(), process_stock_data(), store_data_sb()
    retrieves the past year data from yfinance API then stores it into supabase
    input: stock symbol, period from current date
    output: response or status
    """
    index = request.args.get('index')
    period = request.args.get('period')
    if not (index and period):
        return jsonify({"error": "Missing required parameters: index and period"}), 400

    stock_data = yahoo_by_period(index, period)
    if stock_data is None or stock_data.empty:
        return jsonify({"error": f"No data found for index: {index} and period: {period}"}), 404

    try:
        processed_data = process_stock_data(stock_data)
    except Exception as e:
        return jsonify({"error": f"Failed to process stock data: {str(e)}"}), 500

    try:
        response = store_data_sb(processed_data, index)
        if "error" in response:
            return jsonify(response), 500
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to store data in Supabase: {str(e)}"}), 500


@app.route('/query_llm', methods=['GET'])
def query_llm():
    """
    input: query, stock index
    note, you need to provide a stock symbol somehow (maybe from user input), for efficiency
    output: LLM response
    """
    query = request.args.get('query')
    stock_index = request.args.get('index')
    try:
        response = query_llm_data(query, stock_index)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"failed querying llm": str(e)}), 500


@app.route('/query_llm_news', methods=['GET'])
def query_llm_news():
    """
    input: query, stock index
    output: LLM response
    key difference is simply that the LLM will specifically look for news in vector DB
    """
    query = request.args.get('query')
    stock_index = request.args.get('index')
    try:
        response = handle_llm_news(query, stock_index)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"failed querying llm for stock news": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

"""
options for 'period' parameter: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
"""