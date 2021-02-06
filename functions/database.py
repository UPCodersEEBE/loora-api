from google.cloud import datastore

datastore_client = datastore.Client()


def store_alive(ping):
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update(ping)
    datastore_client.put(entity)


def get_us(dev_id):
    # print("helldo", dev_id)
    # query = client.query(kind="visit")
    # query.add_filter("dev_id", "=", dev_id)
    # print("r")
    return "2021-02-05T15:20:20Z"