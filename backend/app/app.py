from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data, yahoo_by_period
from services.supabase_api import store_data_sb
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
    return response.to_json(orient="records"), 200


@app.route('/store_past_period', methods=['POST'])
def store_past_year():
    """
    retrieves the past year data from yfinance API then stores it into supabase
    input: stock symbol, period from current date
    output: response or status
    """
    index = request.args.get('index')
    period = request.args.get('period')
    url = f"{server_ip}/get_stocks_past_period?index={index}&period={period}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # returned as a json
        df = pd.read_json(data)
        response = store_data_sb(df, index)
        return jsonify(response), 200
    else:
        return jsonify({"error": f"Failed getting stock data from past period {period}"})

