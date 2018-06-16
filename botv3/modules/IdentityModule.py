import asyncio
import core.module as module
import discord
import json
import requests

class IdentityModule(module.Module):

    def __init__(self):
        self.tricker_count = 0
        self.first = 'Albert'
        self.last = 'Bakker'
        self.picture = None
        self.make_identity()
        self.server = None
        print('IdentityModule initialized...')

    # Gets called once, when the client is connected.
    async def on_ready(self):
        #await self.set_identity()
        pass

    # Generates this module's filter object and returns it.
    def get_filter(self):
        return '!name'

    async def handle_message(self, message):
        if not message.channel.name == module.chat_default.name:
            return
       
        await super().handle_message(message)

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        msg = 'IdentityModule help:\r\n'
        msg += '    Creates and sets the identity of this bot\r\n'
        msg += '    Has no user interactions.'
        #msg += 'Commands:\r\n'
        #msg += '    "!name me" to let me pick a new name for you'
        
        return msg

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        return 'IdentityModule: running'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        return self.short_status()

    # This method gets called once every second for time based operations.
    async def update(self):
        #self.tricker_count +=1

        if not self.server:
            self.server = self.find_my_server()

        if self.tricker_count % 3600 == 0:
            self.tricker_count = 0
            await self.set_identity()
            self.make_identity()

        self.tricker_count += 1
    
    def find_my_server(self):
        for server in module.dc_client.servers:
            return server

    def make_identity(self):
        person = requests.get('https://randomuser.me/api/?inc=name,picture')
        person.raise_for_status()
        person = json.loads(person.text)

        self.first = person['results'][0]['name']['first'].title()
        self.last = person['results'][0]['name']['last'].title()

        avatar = requests.get(person['results'][0]['picture']['large'], stream=True, timeout=3)
        avatar.raise_for_status()
        self.picture = avatar.raw.data

    async def set_identity(self):
        name = '{first} {last}'.format(first=self.first, last=self.last)
        module.naam = name
        await module.dc_client.change_nickname(self.server.me, name)
        try:
            await asyncio.wait_for(module.dc_client.edit_profile(avatar = self.picture), 15)
        except discord.errors.HTTPException:
            print('Failed to set avatar :(')
        except asyncio.TimeoutError:
            print('Caught timeouterror!')

