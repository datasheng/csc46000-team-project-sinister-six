from flask import Flask, request, jsonify
from services.yahoo_api import yahoo_get_stock_data

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
    if not response:
        return jsonify({"error": "Data could not be retrieved"}), 404

    return jsonify(response), 200
