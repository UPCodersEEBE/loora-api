import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     from_='whatsapp:+14155238886',
                     body='Your appointment is coming up on July 21 at 3PM',
                     to='whatsapp:+34695848183'
                 )

print(message.sid)
