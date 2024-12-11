from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data, yahoo_by_period
from services.supabase_api import store_data_sb
from services.utils import process_stock_data
import pandas as pd
import requests

app = Flask(__name__)
server_ip = 'http://localhost:5000'


@app.route('/get_stocks', methods=['GET'])
def get_stocks_info():
    """
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


@app.route('/get_stocks_past_period', methods=['GET'])
def get_stocks_past_year():
    """
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
    retrieves the past year data from yfinance API then stores it into supabase
    input: stock symbol, period from current date
    output: response or status
    """
    index = request.args.get('index')
    period = request.args.get('period')
    # Use index as table name if not provided
    table_name = request.args.get('table', index)

    if not (index and period):
        return jsonify({"error": "Missing required parameters: index and period"}), 400

    # Fetch data using yahoo_by_period
    stock_data = yahoo_by_period(index, period)
    if stock_data is None or stock_data.empty:
        return jsonify({"error": f"No data found for index: {index} and period: {period}"}), 404

    # Process stock data using utility function
    try:
        processed_data = process_stock_data(stock_data)
    except Exception as e:
        return jsonify({"error": f"Failed to process stock data: {str(e)}"}), 500

    # # Store processed data in Supabase
    try:
        response = store_data_sb(processed_data, table_name)
        if "error" in response:
            return jsonify(response), 500
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Failed to store data in Supabase: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
