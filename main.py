from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from functions.time_functions import time_check
from functions.database import store_alive, get_us
from functions.twipy import send_whatsapp


app = Flask(__name__)
CORS(app)


@app.route("/alive", methods=["POST"])
def alive():
    json_data = request.get_json(force=True)
    try:
        time = json_data["metadata"]["time"]
        dev_id = json_data["dev_id"]
        last_us(dev_id)
        store_alive(json_data)
        return response
    except:
        return "We need time parameter"


# Calls DB and if the last recorded ultrasound ping was more than 6h ago, calls the user
def last_us(dev_id):
    if time_check(get_us(dev_id)):
        print("ha trucat a la Clara")
        # send_whatsapp("695848183", "Clara")
    return None


if __name__ == "__main__":
    app.run()