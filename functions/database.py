from google.cloud import datastore

datastore_client = datastore.Client()


def store_ping(ping):
    entity = datastore.Entity(key=datastore_client.key("visit"))
    entity.update(ping)

    datastore_client.put(entity)
