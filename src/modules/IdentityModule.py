import json

import discord
import modules.ModuleBase as base
import requests

class Identity(base.ModuleBase):

    def __init__(self, client):
        self.client = client
        self.tricker_count = 0
        self.first = 'Albert'
        self.last = 'Bakker'
        self.picture = None
        self.make_identity()
        self.server = None
        print('Identity module initialized')

    # Gets called once, when the client is connected.
    async def on_ready(self):
        #await self.set_identity()
        pass

    # Generates this module's filter object and returns it.
    def get_filter(self):
        return '!name'

    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        # dit kan worden:
        # await super().handle_message(message)
        
        args = message.content.split(' ')
        if len(args) == 1:
            await client.send_message(message.channel, self.help_message())
            return
            
        if len(args) == 2:
            if args[1] == 'help':
                await client.send_message(message.channel, self.help_message())
                return
            if args[1] == 'status':
                await client.send_message(message.channel, self.status())
                return

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        return 'IdentityModule help'

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        return 'IdentityModule help'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        return 'IdentityModule: Idle'

    def name(self):
        return 'IdentityModule'

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
        for server in self.client.servers:
            self.server = server
            return

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
        await self.client.change_nickname(self.server.me, name)
        try:
            await asyncio.wait_for(self.client.edit_profile(avatar = self.picture), 15)
            print('successfully changed avatar!')
        except discord.errors.HTTPException:
            print('Failed to set avatar :(')
        except asyncio.TimeoutError:
            print('Caught timeouterror!')

