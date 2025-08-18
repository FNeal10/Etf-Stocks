import os
from dotenv import load_dotenv
from flask import Flask
from routes.routes import api_routes


if os.path.exists('.env'):
    load_dotenv()


app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)