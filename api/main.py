from flask import Flask, request, jsonify
from src.data.blob_storage_utils import get_market_urls
import os

app = Flask(__name__)

service_client = os.getenv("AZURE_CONNECTION_STRING")
container_client = os.getenv("CONTAINER_NAME")

@app.route("/market_urls", methods=["GET"])
def market_urls():
    try:
        data = get_market_urls(service_client, container_client)
        data = data.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}, 500)
    
#@app.route("/")
    
    

if __name__ == "__main__":
    app.run(debug=True)