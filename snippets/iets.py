import json

string1 = json.dumps({'test' : 5})
string2 = json.dumps({'document2' : {'test' : 5}})

print(json.loads(string1 + string2))