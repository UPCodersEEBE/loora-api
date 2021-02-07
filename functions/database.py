from google.cloud import datastore
from .time_functions import time_check, arduino_new_time
from .twipy import send_whatsapp

client = datastore.Client()

# adds a device, userId and telephone to users entity
def add_device_db(device, dev_id):
    entity = datastore.Entity(key=client.key("users", dev_id))
    entity.update(device)
    client.put(entity)
    return


# stores data sent by the device. If the device detects movement of
# the owner, it will also count as a ping
def store_db(data, action):
    entity = datastore.Entity(key=client.key(action, data["dev_id"]))
    data_dict = {"time": data["metadata"]["time"]}
    entity.update(data_dict)
    client.put(entity)
    if action == "alive":
        store_db(data, "ping")
    return


# Checks if the last interaction (ultrasound detection or device ping)
# happened a long time ago. If the device looks inactive or the person
# has not moved in a while, the device id's are stored in an array that
# will be compared with the user datastore entitiy
def get_last_action(action):
    query = client.query(kind=action)
    users_to_call = []
    for user in list(query.fetch()):
        if time_check(user["time"], action):
            users_to_call.append(user.key.id_or_name)
    return users_to_call


# Compares the devices that need notifications with the users datastore
# entity. A whatsapp message is sent to each of them.
def call_users(users_to_call, action):
    query = client.query(kind="users")
    for user in list(query.fetch()):
        if (user.key.id_or_name) in users_to_call:
            send_whatsapp(user["phone"], user["name"], action)
            update_after_call(user.key.id_or_name,action)
    return

# modifies database to prevent sending messages every user check, which
# happens once every 5 minutes
def update_after_call(userId,action):
    entity = datastore.Entity(key=client.key(action, userId))
    entity.update({"time":str(arduino_new_time(action)) })
    client.put(entity)
    return


def retrieve_all_data(dev_id):
    key = client.key("ping", dev_id)
    data = client.get(key)
    last_ping=data["time"]
    key = client.key("alive", dev_id)
    data = client.get(key)
    last_alive=data["time"]
    key = client.key("users", dev_id)
    data = client.get(key)
    name=data["name"]
    phone=data["phone"]
    return last_ping, last_alive, name, phone