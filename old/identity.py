import json
import requests

def get_peep():
    person = requests.get('https://randomuser.me/api/',timeout=3)
    person.raise_for_status()
    return json.loads(person.text)
    
def get_avatar(url):
    print('avatar url: ', url, ', downloading...', end='')
    avatar = requests.get(url, stream=True, timeout=3)
    avatar.raise_for_status()
    print('done!')
    return avatar.raw.data