from flask import Flask, request, render_template
from flask_cors import CORS
import json

# custom functions
from functions.database import (
    store_db,
    get_last_action,
    call_users,
    add_device_db,
)
from functions.twipy import send_whatsapp


app = Flask(__name__)
CORS(app)

# Our static website lays on the base url
@app.route("/")
def about():
    return render_template("about.html")


# website to add a user to the database
@app.route("/create_user_form")
def create_user_form():
    return render_template("adduser.html")


# endpoint to add a user to the database. The user needs 3 parameters:
# devie id, name and phone number. It is added to an entity called
# users in google datastore
@app.route("/add_device", methods=["POST"])
def add_device():
    json_data = request.get_json(force=True)
    try:
        name = json_data["name"]
        dev_id = json_data["dev_id"]
        phone = json_data["phone"]
        data = {"name": name, "phone": phone}
        add_device_db(data, dev_id)
        return "User added"
    except:
        return "At least one parameter is missing"


# endpoint to add an interaction to the database. The hardware devices can
# send two types of actions:
#  - Alive: the user has passed in front of a ultrasound sensor
#  - Ping: periodig signal to indicate the hardware is still online
# they are added in the "alive" and "ping" entities respectively
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


# endpoint to check issues in the user database. If the last ping was made
# more than 10 minutes ago, a whatsapp message is sent to the stored phone
# number saying the device may be disconnected. If the ultrasound detector
# hasen't seen activity in the last 12 hours, a message is sent prompting
# to check on the device owner
@app.route("/check_users", methods=["GET"])
def check_users():
    actions = ["alive", "ping"]
    for action in actions:
        users_to_call = get_last_action(action)
        call_users(users_to_call, action)
    return "check completed"


if __name__ == "__main__":
    app.run()