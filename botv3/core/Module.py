import discord

'''
    This class is the baseclass for any module used by the bot.
    It contains default implementations and utility functions for communication with the server
'''
class Module:
    ''' Static ref to the client, usable by all modules after it being set once '''
    dc_client = None

    ######################
    ## Static functions ##
    ######################

    ''' Returns a member object by nickname on the server. '''
    def member_by_name(self, name):
        return None

    ''' Returns a channel object by name on the server '''
    def channel_by_name(self, name):
        return None

    #############
    ## Methods ##
    #############

    ''' 
        returns filter object
        !! Currently unused
    '''
    def get_filter(self):
        raise NotImplementedError()

    '''
        This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response.
    '''
    async def handle_message(self, message):
        args = message.content.split(' ')
        if len(args) == 1:
            await self.client.send_message(message.channel, self.help_message())
            return True
            
        if len(args) == 2:
            if args[1] == 'help':
                await self.client.send_message(message.channel, self.help_message())
                return True
            if args[1] == 'status':
                await self.client.send_message(message.channel, self.status())
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
        type(self).__name__

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