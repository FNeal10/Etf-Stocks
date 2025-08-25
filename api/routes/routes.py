from flask import Blueprint, request, jsonify, Response, render_template
from utils.blob_storage import *


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/')
def index():
    return render_template('about.html')


@api_routes.route('/market-urls', methods=['GET'])
def market_urls():
    try:
        df = get_market_urls()
        return jsonify(df.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_routes.route('/append-ohclv', methods=['POST'])
def append_ohclv():
    try:
        params = request.get_json()
        ticker_name = params.get("ticker_name")
        market_data = params.get("market_data")

        append_latest_ohclv(ticker_name, market_data)

        return jsonify({"message": "OHLCV data appended successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@api_routes.route('/get-bronze', methods=['POST'])
def get_bronze():
    try:
        bronze_files = get_bronze_files()
        return jsonify(bronze_files), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@api_routes.route('/get-file', methods=['POST'])
def get_file():
    try:
        params = request.get_json()
        file = params.get("file")

        file_data = get_file_data(file)
        if file_data is None:
            return jsonify({"error": "File not found"}), 404
        
        return Response(file_data, mimetype="text/csv"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/create-silver', methods=['POST'])
def create_silver():
    try:
       silver_file = request.get_data()
       result = create_silver_file(silver_file)
       return jsonify(result), 201 if result.get("is_success") else 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500