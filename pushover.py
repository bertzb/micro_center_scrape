import requests
from os import environ


if 'PO_APP_TOKEN' in environ:
  PO_APP_TOKEN = environ.get('PO_APP_TOKEN')
else:
  raise OSError("No Pushover app token found in env vars")

if 'PO_USER_TOKEN' in environ:
  PO_USER_TOKEN = environ.get('PO_USER_TOKEN')
else:
  raise OSError("No Pushover user token found in env vars")


pushover = requests.post(
    "https://api.pushover.net/1/messages.json",
    data = {
      "token": PO_APP_TOKEN,
      "user": PO_USER_TOKEN,
      "message": "hello world"
    }
    #},
    #files = {"attachment": ("image.jpg", open("your_image.jpg", "rb"), "image/jpeg")}
  )

print(pushover.text)
