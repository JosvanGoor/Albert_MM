import discord
import ModuleBase as base
import time

class GeneralModule (base.ModuleBase):
    
    # Constructor
    def __init__(self, client, modules):
        self.client = client
        self.modules = modules
        self.startup_time = None

        print('GeneralModule initialized...')

    # Gets called once, when the client is connected.
    async def on_ready(self):
        self.startup_time = int(time.time())

    # Generates this module's filter object and returns it.
    def get_filter(self):
        pass

    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        if not message.channel.name == 'botspam': return

        if message.content.startswith('!ping'):
            await client.send_message(message.channel, 'Pong!')
            return
        
        if message.content.startswith('!pong'):
            await client.send_message(message.channel, 'Toe even...')
            return

        await super.handle_message(message) # handles 'help' and 'status'

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        msg = 'MagikMan bot v1.0 help.\r\n\r\n'
        msg += 'I am the l3am discord bot try me and say !ping\r\n'
        msg += 'To get help on any sub modules use the module command followed by "help"\r\n\r\n'
        msg += 'List of module commands:\r\n'
        for key in self.modules.keys():
            msg += '    ' + key + '\r\n'
        
        return msg

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        return 'GeneralModule: status ok!'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        msg = 'Magikman bot status report:\r\n'
        msg = 'runtime: ' + str(self.startup_time - int(time.time())) + 's\r\n\r\n'
        msg = 'Modules:\r\n'
        for value in self.modules.values():
            msg = '    ' + value.short_status() + '\r\n'
        
        return msg
        
    # This method gets called once every second for time based operations.
    async def update(self):
        pass