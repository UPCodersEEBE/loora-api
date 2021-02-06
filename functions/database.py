from google.cloud import datastore

client = datastore.Client()


def store_alive(ping):
    entity = datastore.Entity(key=client.key("visit"))
    entity.update(ping)
    client.put(entity)
    return


def get_us(dev_id):
    print("query")
    query = client.query(kind="visit")
    query.add_filter("dev_id", "=", dev_id)
    query.order = ["counter"]
    print(list(query.fetch())[0]["counter"])
    print(list(query.fetch())[0]["metadata"]["time"])
    return list(query.fetch())[0]["metadata"]["time"]


def get_users(dev_id):
    print("query")
    query = client.query(kind="visit")
    query.projection = ["dev_id"]
    query.keys_only()
    print(list(query.fetch()))
    return list(query.fetch())[0]["metadata"]["time"]
