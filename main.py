from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from functions.time_functions import check_time
from functions.database import store_ping


app = Flask(__name__)
CORS(app)


@app.route("/ping", methods=["POST"])
def ping():
    json_data = request.get_json(force=True)
    try:
        time = json_data["time"]
        response = check_time(time)
        store_ping(json_data)
        return response
    except:
        return "We need time parameter"


if __name__ == "__main__":
    app.run()