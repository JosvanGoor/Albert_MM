import json
import requests

import logintoken

header = { "Client-ID" : logintoken.get_twitch_id() }
url = "https://api.twitch.tv/helix/users?login={}"
stream_ids = ["dreamhackcs", "eikelxl"]

url = url.format("waasdasdvycolt")

req = requests.get(url, headers=header)
data = json.loads(req.text)
print(json.dumps(data, indent = 4))

#record = {}

#for stream in data["data"]:
#    record[stream["id"]] = stream

#print(json.dumps(record, indent = 4))