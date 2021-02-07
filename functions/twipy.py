import os
from twilio.rest import Client


# credential variables from twilio
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# this function prepares a message to send to whatsapp. It takes a user name and number and
# an action that can be "alive" or "ping", and creates a message depending on it's value
def send_whatsapp(recievernum, name, action):
    if action == "ping":
        message = f"It seems like {name}'s node disconnected! It may be out of battery."
    elif action == "alive":
        message = f"Hey! It seems like {name} hasn't moved in a while. You should check on them."
    print("called {} at {} saying: {}".format(name, recievernum, message))
    send_message(recievernum, message)
    return


# the message is sent to whatsapp (only Spain is supported now)
def send_message(recievernum, message):
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=message,
        to="whatsapp:+{}".format(recievernum),
    )
    return
