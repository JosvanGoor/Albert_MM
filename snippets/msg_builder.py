import json

# op = opcode (mandatory)
# d = event message (mandatory)
# s = sequence number (mandatory if available)
# t = event name (optional)
def payload(op, d, s=None, t=None):
    msg = {}
    msg["op"] = op
    msg["d"] = d
    msg["s"] = s
    msg["t"] = t
    return msg

def strip_payload(response):
    msg = response["d"]
    response["d"] = None
    payload = response
    return payload, msg

def heartbeat(seq_num):
    msg = {}
    msg["op"] = 1
    msg["d"] = str(seq_num)
    return json.dumps(msg)
    
def identify(token):
    msg = {
        'token': str(token),
        'properties' : {
            '$os' : 'Win32',
            '$browser': 'Alberto',
            '$device' : 'Alberto'
        },
        'compress' : False
    }
    print(json.dumps(payload(2, msg), indent=4))
    return json.dumps(payload(2, msg))