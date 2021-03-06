from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import json

# custom functions
from functions.database import (
    store_db,
    retrieve_all_data,
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

# OCheck information from specific device
@app.route("/device", methods=["GET"])
def device():
    dev_id=request.args.get("dev_id")
    last_ping, last_alive, name, phone = retrieve_all_data(dev_id)
    return render_template("device.html", last_ping=last_ping, last_alive=last_alive, name=name, phone=phone)


# html page to add a user to the database. The user needs 3 parameters:
# devie id, name and phone number. It is added to an entity called
# users in google datastore
@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        name = request.form["name"]
        deviceid = request.form["deviceid"]
        phone = request.form["phone"]

        add_device(name, deviceid, phone)
        return redirect(request.url)

    return render_template("adduser.html")


def add_device(name, dev_id, phone):
    try:
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