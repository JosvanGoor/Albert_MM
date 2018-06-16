import atexit
import os
import requests
import json

import logintoken as token
import core.module as module

class StreamModule(module.Module):

    def __init__(self, channel):
        self._channel = channel
        self._streams = {} # "stream_id" : online_bool
        self._datafile = "data/StreamModule.json"
        self._initialize_state()
        self._ticker = 0

        data = self._load_state()
        for key, value in self._streams.items():
            if key in data:
                value["online"] = True

    #####
    #   MODULE OVERWRITES
    #####
    def get_filter(self):
        return "sm"

    '''
        This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response.
    '''
    async def handle_message(self, message):
        if not message.channel.name == self._channel.name: return
        args = message.content.split(' ')

        if len(args) == 3:
            if args[1] == "add":
                self._add_url(args[2])

            if args[1] == "remove":
                self._remove_url(args[2])

        if len(args) == 2:
            if args[1] == "list":
                lst = "\r\n    - ".join(self._streams.keys())
                msg = "Tracking the following streams:\r\n    {}".format(lst)
                await module.dc_client.send_message(self._channel, msg)

        await super().handle_message(message)

    '''
        This method gets called when help is called on this module.
        It should return a string explaining the usage of this module
    '''
    def help_message(self):
        return "StreamModule help:\r\nWIP"

    ''' Status in 1 line (running! or error etc..) '''
    def short_status(self):
        return "StreamModule: Running"

    '''
        This method gets called when status is called on this module. 
        It should return a string explaining the runtime status of this module.
    '''
    def status(self):
        return "StreamModule: Running"

    ''' This method gets called once every second for time based operations. '''
    async def update(self):
        self._ticker += 1

        if(self._ticker == 60):
            self._ticker = 0

            print("Checking online status!")

            data = self._load_state()
            #print("DATA:\r\n{}".format(json.dumps(data, indent = 4)))
            #print("STREAMS:\r\n{}".format(json.dumps(self._streams, indent = 4)))

            for key, value in self._streams.items():
                if value["id"] in data:
                    if value["online"]:
                        continue
                    value["online"] = True
                    msg = "{} has just started streaming on twitch!\r\n    Title: {}\r\n    Url: {}"
                    msg = msg.format(key, data[value["id"]]["title"], "https://twitch.tv/{}".format(key))
                    await module.dc_client.send_message(self._channel, msg)
                else:
                    value["online"] = False
                    

    #####
    #   INTERNALS
    #####
    def _load_state(self):
        if(len(self._streams) == 0): return

        url = "https://api.twitch.tv/helix/streams?user_login={}"
        url = url.format("&user_login=".join(self._streams.keys()))

        #print("STREAM UPDATE URL: {}".format(url))

        req = requests.get(url, headers = {"Client-ID" : token.get_twitch_id()})
        data = json.loads(req.text)
        #print("STREAM RESPONSE: {}".format(req.text))

        record = {}
        for stream in data["data"]:
            record[stream["user_id"]] = stream
        return record

    def _get_user_id(self, name):
        url = "https://api.twitch.tv/helix/users?login={}".format(name)
        req = requests.get(url, headers = {"Client-ID" : token.get_twitch_id()})
        data = json.loads(req.text)
        #print(json.dumps(data))

        if len(data["data"]) == 0:
            module.send_message_nowait(self._channel, "No twitch user found for name {}".format(name))
            return
        return data["data"][0]["id"]

    def _new_stream(self, id, name):
        return {
            "id" : id,
            "name" : name,
            "title" : "<unknown>",
            "online" : False }

    def _add_url(self, url):
        if url.startswith("https://www.twitch.tv/"):
            url = url[22:]
        elif url.startswith("https://twitch.tv/"):
            url = url[18:]
        else:
            return
        if len(url) >= 1:
            self._streams[url] = self._new_stream(self._get_user_id(url), url)
            self._store_state()

    def _remove_url(self, url):
        if url.startswith("https://www.twitch.tv/"):
            url = url[22:]
        elif url.startswith("https://twitch.tv/"):
            url = url[18:]
        else: return

        if url in self._streams:
            del self._streams[url]
            self._store_state()

    def _initialize_state(self):
        if os.path.isfile(self._datafile):
            with open(self._datafile, "r") as file:
                self._streams = json.load(file)

    def _store_state(self):
        with open(self._datafile, "w+") as file:
            json.dump(self._streams, file, indent=4)

        
        
