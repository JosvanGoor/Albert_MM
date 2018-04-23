import discord
import core.module as module
import core.userdata as userdata
import core.worker as worker
import sys
import time
import datetime

class GeneralModule(module.Module):
    
    # Constructor
    def __init__(self, modules):
        self.modules = modules
        self.startup_time = None
        self.last_backup = 0

        print('GeneralModule initialized...')

    # Gets called once, when the client is connected.
    async def on_ready(self):
        self.startup_time = int(time.time())
        self.last_backup = self.startup_time

    # Generates this module's filter object and returns it.
    def get_filter(self):
        pass

    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        if not message.channel.name == module.chat_default.name:
            return

        if message.content.startswith('!ping'):
            await module.dc_client.send_message(message.channel, 'Pong!')
            return
        
        if message.content.startswith('!pong'):
            await module.dc_client.send_message(message.channel, 'Toe even...')
            return

        if message.content.startswith('!help'):
            await module.dc_client.send_message(message.channel, self.help_message())
            return

        if message.content.startswith('!status'):
            await module.dc_client.send_message(message.channel, self.status())
            return

        if message.content.startswith('!penis'):
            await module.dc_client.send_message(message.channel, ':eggplant:')

        if message.content.startswith('!quit'):
            sender = message.author.name + '#' + message.author.discriminator
            print('DEBUG: quit message from {}'.format(sender))

            if sender == 'Wavycolt#7327' or sender == 'Boerenkool#8539':
                await module.dc_client.send_message(message.channel, ':wave::wave:')
                worker.finalize()
                sys.exit(0)
            else:
                await module.dc_client.send_message(message.channel, 'No! =(')

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        msg = 'MagikMan bot v3.0 help.\r\n\r\n'
        msg += 'I am the l3am discord bot try me and say !ping\r\n'
        msg += 'To get help on any sub modules use the module command followed by "help"\r\n\r\n'
        msg += 'List of module commands:\r\n'
        for key, value in self.modules.items():
            msg += '    "' + key + '" - ' + value.name()  + '\r\n'
        
        return msg

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        return 'GeneralModule: status ok!'

    def timestring(self, sec):
        return str(datetime.timedelta(seconds=sec))
        
    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        msg = 'Magikman bot v3.0 status report:\r\n'
        msg += 'runtime: ' + self.timestring(int(time.time()) - self.startup_time) + '\r\n\r\n'
        msg += 'Modules:\r\n'
        for value in self.modules.values():
            msg += '    ' + value.short_status() + '\r\n'
        
        return msg
        
    # This method gets called once every second for time based operations.
    async def update(self):
        backup_delay = time.time() - self.last_backup
        if backup_delay > (60 * 60 * 24): #24 hour
            userdata.schedule_backup()
            backup_delay = time.time()