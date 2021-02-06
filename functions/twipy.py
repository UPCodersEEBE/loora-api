import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_whatsapp(recievernum, name):
    print("called {} at {}".format(name, recievernum))
    message = f"Hey! It seems like {name} is moving around"
    message = client.messages.create(
        from_="whatsapp:+14155238886", body=message, to="whatsapp:+34" + recievernum
    )
    return
