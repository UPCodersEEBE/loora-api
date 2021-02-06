from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import json
from functions.time_functions import time_check
from functions.database import store_db, get_last_us, get_users
from functions.twipy import send_whatsapp


app = Flask(__name__)
CORS(app)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/add_device", methods=["POST"])
def add_device():
    json_data = request.get_json(force=True)
    try:
        user_id = json_data["user_id"]
        device_id = json_data["device_id"]
        phone_number = json_data["phone_number"]
        return "test"
    except:
        return "At least one parameter is missing"


@app.route("/alive", methods=["POST"])
def alive():
    json_data = request.get_json(force=True)
    try:
        time = json_data["metadata"]["time"]
        store_db(json_data, "alive")
        return "test"
    except:
        return "Time parameter is missing"


@app.route("/ping", methods=["POST"])
def ping():
    json_data = request.get_json(force=True)
    try:
        time = json_data["metadata"]["time"]
        store_db(json_data, "ping")
        return "test"
    except:
        return "Time parameter is missing"


@app.route("/check_users", methods=["GET"])
def check_users():
    users = get_users("ping")
    count = 0
    for user in users:
        last_us = get_last_us(user)
        if time_check(last_us["time"]):
            count += 1
            print("s'ha trucat a {} al telefon {}".format(user, str(last_us["phone"])))
            # send_whatsapp(str(last_us["phone"]), user)
        else:
            print(
                "no cal trucar a {} al telefon {}".format(user, str(last_us["phone"]))
            )
    return "Check complete, only {} of {} users are dead".format(
        str(count), str(len(users))
    )



if __name__ == "__main__":
    app.run()