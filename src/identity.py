import json
import requests

def get_peep():
    person = requests.get('https://randomuser.me/api/')
    person.raise_for_status()
    return json.loads(person.text)
    
def get_avatar(url):
    print('avatar url: ', url)
    avatar = requests.get(url, stream=True)
    avatar.raise_for_status()
    return avatar.raw.data