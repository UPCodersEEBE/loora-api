import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_whatsapp(recievernum, name, action):
    if action == "ping":
        message = f"It seems like {name}'s node disconnected! It may be out of battery."
    elif action == "alive":
        message = f"Hey! It seems like {name} is moving around"
    print("called {} at {} saying: {}".format(name, recievernum, message))
    send_message(recievernum, message)
    return


def send_message(recievernum, message):
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=message,
        to="whatsapp:+34" + str(recievernum),
    )
    return
