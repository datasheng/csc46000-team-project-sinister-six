from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data, yahoo_by_period, yahoo_get_additional_data, get_quote_table
from services.supabase_api import store_data_sb, get_data_all_sb
from services.utils import process_stock_data
import pandas as pd
import requests

app = Flask(__name__)
server_ip = 'http://localhost:5000'


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

@app.route('/get_full_stock_data', methods=['GET'])
def get_full_stock_data():
    """
    Combine historical data with additional metrics from Yahoo Finance.
    """
    stock_index = request.args.get('index')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if not (stock_index and start_date and end_date):
        return jsonify({"error": "REQUIRED parameters are missing from the API call"}), 400

    # Get historical stock data
    historical_data = yahoo_get_stock_data(stock_index, start_date, end_date)
    if historical_data is None or historical_data.empty:
        return jsonify({"error": "Historical data could not be retrieved"}), 404

    # Get additional stock metrics
    additional_data = yahoo_get_additional_data(stock_index)
    if additional_data is None:
        return jsonify({"error": "Additional data could not be retrieved"}), 404

    return jsonify({
        "historical_data": historical_data.to_dict(orient="records"),
        "additional_data": additional_data
    }), 200

@app.route('/get_quote_table', methods=['GET'])
def get_quote_table_data():
    """
    Fetch quote table data for a given stock symbol.
    """
    stock_index = request.args.get('index')

    if not stock_index:
        return jsonify({"error": "REQUIRED parameter 'index' is missing"}), 400

    quote_data = get_quote_table(stock_index)
    if quote_data is None:
        return jsonify({"error": "Quote table data could not be retrieved"}), 404

    return jsonify(quote_data), 200

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


if __name__ == "__main__":
    app.run(debug=True)

"""
options for 'period' parameter: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
"""