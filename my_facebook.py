import requests
import json
from urllib.parse import quote

base_url = "https://graph.facebook.com/v9.0/me"
fields = quote("id,name,likes.limit(10){about}")
# fields = quote("id,name")

with open('facebook_api.json') as fb_config_file:
    _fb_config = json.load(fb_config_file)
    ACCESS_TOKEN = _fb_config['ACCESS_TOKEN']
print(ACCESS_TOKEN)

url = "{0}?fields={1}&access_token={2}".format(base_url, fields, ACCESS_TOKEN)
print(url)

content = requests.get(url).json()
print(json.dumps(content, indent=1))
