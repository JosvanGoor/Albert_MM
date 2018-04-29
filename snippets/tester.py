import json
import logintoken as tokens
import requests
import select
import signal
import sys
import time
import websocket

import msg_builder

def get_weblink(token):
    headers = {"Authorization" : f"Bot {token}"}
    response = requests.get("https://discordapp.com/api/gateway/bot", headers=headers)
    return json.loads(response.text)

#print(get_weblink(tokens.get_token()).text)
#sys.exit(0)

print('hb: {}'.format(msg_builder.heartbeat('null')))

def signal_handler(signal, frame):
    print('CTRL+C caught')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

socket = websocket.WebSocket()
socket.settimeout(7200) # 2 uur should do it?

url = get_weblink(tokens.get_token())["url"]
print('Connection: ' + url)
socket.connect(f'{url}/?v=6&encoding=json')

response = json.loads(socket.recv())
print(response)
socket.send(msg_builder.identify(tokens.get_token()))

sequence_number = 'null'
heartbeat = response['d']['heartbeat_interval']

ticks_since_hb = 0
tickspeed = 0.1 #10x per sec
start = time.time()

while True:
    r, w, e = select.select([socket.sock], [], [], 0)
    if r:
        response = socket.recv()
        
        with open('output.txt', 'a+') as file:
            response = json.loads(response)
            print(response)
            json.dump(response, file, indent=4)

        print()
        print('received something: ')
        print(response)

    #manage heartbeat code
    ticks_since_hb += 1
    if (ticks_since_hb * 100) >= heartbeat:
        ticks_since_hb = 0
        socket.send(msg_builder.heartbeat(sequence_number))

    end = time.time()
    #print(f'ticker start: {start}, end: {end}')
    worktime = end - start
    start += tickspeed
    if worktime > tickspeed:
        print('Warning! ticker not keeping up')
        print(f'    worktime: {worktime}')
        continue
    time.sleep(tickspeed - worktime) #ensure "purest form of 0.1ticks"