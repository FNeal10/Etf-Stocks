import os
from dotenv import load_dotenv
from flask import Flask
from api.routes.routes import api_routes


if os.path.exists('.env'):
    load_dotenv()


app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == "__main__": 
    app.run(debug=True)