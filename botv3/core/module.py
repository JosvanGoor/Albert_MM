import asyncio
import discord

############
## Global ##
############

''' Static ref to the client, usable by all modules after it being set once '''
dc_client = None
''' Static reference to the default output chat channel '''
chat_default = None
''' TEMPORARY WORKAROUND '''
naam = "Albert"

''' Returns a member object by nickname on the server. '''
def member_by_name(name):
    for mem in get_server().members:
        if name == mem.nick or name == mem.name or name == (mem.name + '#' + mem.discriminator):
            print('found member by name {}: {}#{} / {}'.format(name, mem.name, mem.discriminator, mem.nick))
            return mem

''' Returns a channel object by name on the server '''
def channel_by_name(name):
    for chan in get_server().channels:
        if chan.name == name:
            print('found channel by name {}'.format(name))
            return chan

''' Convenience function to retrieve the connected server (bot only supports being connected to one server) '''
def get_server():
    for s in dc_client.servers:
        return s

def send_message_nowait(channel, message):
    asyncio.ensure_future(dc_client.send_message(channel, message))

def strip_name(member):
    if isinstance(member, discord.Member):
        if hasattr(member, "nick") and member.nick:
            return member.nick
        return member.name

################
## Base class ##
################

'''
    This class is the baseclass for any module used by the bot.
    It contains default implementations and utility functions for communication with the server
'''
class Module:
    ''' 
        returns filter object
        !! Currently unused
    '''
    def get_filter(self):
        return ""

    '''
        This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response.
    '''
    async def handle_message(self, message):
        args = message.content.split(' ')
        if len(args) == 1:
            await dc_client.send_message(message.channel, self.help_message())
            return True
            
        if len(args) == 2:
            if args[1] == 'help':
                await dc_client.send_message(message.channel, self.help_message())
                return True
            if args[1] == 'status':
                await dc_client.send_message(message.channel, self.status())
                return True

        return False

    '''
        This method gets called when help is called on this module.
        It should return a string explaining the usage of this module
    '''
    def help_message(self):
        raise NotImplementedError()

    ''' Returns the name of the module. '''
    def name(self):
        return type(self).__name__

    ''' Gets called once, when the client is connected. '''
    async def on_ready(self):
        pass

    ''' gets called when an update happens in any voice channel '''
    async def on_voice_change(self):
        pass

    ''' Status in 1 line (running! or error etc..) '''
    def short_status(self):
        raise NotImplementedError()

    '''
        This method gets called when status is called on this module. 
        It should return a string explaining the runtime status of this module.
    '''
    def status(self):
        raise NotImplementedError()

    ''' This method gets called once every second for time based operations. '''
    async def update(self):
        pass