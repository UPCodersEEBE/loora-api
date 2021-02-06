from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import json
from functions.database import store_db, get_last_action, call_users, add_device_db
from functions.twipy import send_whatsapp


app = Flask(__name__)
CORS(app)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add_device", methods=["POST"])
def add_device():
    json_data = request.get_json(force=True)
    try:
        name = json_data["name"]
        dev_id = json_data["dev_id"]
        phone = json_data["phone"]
        data = {"name": name, "dev_id": dev_id, "phone": phone}
        add_device_db(data)
        return "User added"
    except:
        return "At least one parameter is missing"


@app.route("/alive", methods=["POST"])
def alive():
    json_data = request.get_json(force=True)
    try:
        if json_data["payload_fields"]["aka"] == "o":
            action = "ping"
        elif json_data["payload_fields"]["aka"] == "x":
            action = "alive"
        time = json_data["metadata"]["time"]
        store_db(json_data, action)
        return "Added correctly"
    except:
        return "At least one parameter is missing"


@app.route("/check_users", methods=["GET"])
def check_users():
    actions = ["alive", "ping"]
    for action in actions:
        users_to_call = get_last_action(action)
        call_users(users_to_call, action)
    return "check completed"


if __name__ == "__main__":
    app.run()