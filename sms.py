import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC0097621915f6378da39162bb2b78e263'
auth_token = '97ffeae960d2f5d712cee8fa33620026'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+16074007517',
                     to='+9779860999660'
                 )

print(message.sid)