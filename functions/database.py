from google.cloud import datastore
from .time_functions import time_check
from .twipy import send_whatsapp

client = datastore.Client()

# adds a device, userId and telephone to users DB
def add_device_db(device, dev_id):
    entity = datastore.Entity(key=client.key("users", device))
    entity.update(device)
    client.put(entity)
    return


# stores data sent by the LORA
def store_db(data, action):
    entity = datastore.Entity(key=client.key(action, data["dev_id"]))
    data_dict = {"time": data["metadata"]["time"]}
    entity.update(data_dict)
    client.put(entity)
    if action == "alive":
        store_db(data, "ping")
    return


# gets last time the user has activated the us sensor
def get_last_action(action):
    query = client.query(kind=action)
    users_to_call = []
    for user in list(query.fetch()):
        if time_check(user["time"], action):
            users_to_call.append(user.key.id_or_name)
    return users_to_call


# Gets a list of all unique dev_id
def call_users(users_to_call, action):
    query = client.query(kind="users")
    for user in list(query.fetch()):
        if (user.key.id_or_name) in users_to_call:
            send_whatsapp(user["phone"], user["name"])
    return
