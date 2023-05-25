import os
from twilio.rest import Client
account_sid = "AC1cbf4470d5cf7463c873e77d3d8684a0"
auth_token = "ce76ba0924583166a8829248adc8972f"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body="Hello Paithankar",
  from_="+13158182340",
  to="+919930147179"
)
print(message.sid)