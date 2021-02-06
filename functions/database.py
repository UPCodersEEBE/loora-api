from google.cloud import datastore

client = datastore.Client()

# adds a device, userId and telephone to users DB
def add_device(device):
    entity = datastore.Entity(key=client.key("users"))
    entity.update(device)
    client.put(entity)
    return


# stores data sent by the LORA
def store_db(data, action):
    entity = datastore.Entity(key=client.key(action, data["dev_id"]))
    data_dict = {"time": data["metadata"]["time"]}
    entity.update(data_dict)
    client.put(entity)
    return


# gets last time the user has activated the us sensor
def get_last_us(dev_id):
    query = client.query(kind="visit")
    query.add_filter("dev_id", "=", dev_id)
    query.order = ["-counter"]
    return {
        "time": list(query.fetch())[0]["metadata"]["time"],
        "phone": list(query.fetch())[0]["hardware_serial"],
    }


# Gets a list of all unique dev_id
def get_users(action):
    query = client.query(kind=action)
    query.order = ["time"]
    users = []
    for user in list(query.fetch()):
        print(user.key)
    return users