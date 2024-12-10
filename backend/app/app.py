from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data, yahoo_past_year
import pandas as pd

app = Flask(__name__)


@app.route('/stocks', methods=['GET'])
# basically retrieve stocks data between two specified dates!
# make sure to specify in the docs, format must be in YYYY-MM-DD format
def get_stocks_info():
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

@app.route('/stocks_past_year', methods=['GET'])
def get_stocks_past_year():
    stock_index = request.args.get('index')
    if not stock_index:
        return jsonify({"error": "REQUIRED parameters are missing from the API call"}), 400
    response = yahoo_past_year(stock_index)
    if response is None or len(response) == 0:
        return jsonify({"error": "Data could not be retrieved"}), 404
    response = pd.DataFrame(response)
    return response.to_json(orient="records"), 200