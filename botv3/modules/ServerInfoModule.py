import core.module as module
import core.worker as worker
import mcstatus as mc

class ServerInfoModule(module.Module):
    
    def __init__(self):
        print('ServerInfoModule initialized...')

    '''
        This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response.
    '''
    async def handle_message(self, message):
        if not message.channel.name == module.chat_default.name:
            return

        args = message.content.split(' ')

        if len(args) == 2:
            if args[1] == 'minecraft':
                worker.queue_function(self.minecraft_status)
                return

        if await super().handle_message(message):
            return

    '''
        This method gets called when help is called on this module.
        It should return a string explaining the usage of this module
    '''
    def help_message(self):
        msg = 'ServerInfoModule help:\r\n'
        msg += 'This module allows you to get info on the status of the l3am server, note that it is still a work in progress at this time.\r\n\r\n'
        msg += 'Commands:\r\n'
        msg += '    "!info minecraft": Shows the online status of the minecraft server\r\n'
        return msg

    ''' Status in 1 line (running! or error etc..) '''
    def short_status(self):
        return self.name() + ': ready...'

    '''
        This method gets called when status is called on this module. 
        It should return a string explaining the runtime status of this module.
    '''
    def status(self):
        msg = 'ServerInfoModule status: ok!\r\n'
        msg += self.minecraft_status()
        return msg

    ''' This method gets called once every second for time based operations. '''
    async def update(self):
        pass

    def minecraft_status(self):
        msg = ''
        
        try:
            server_1 = mc.MinecraftServer('minecraft.wavycolt.com')
            status = server_1.status()

            msg = 'Server 1: "{}" has {} players online and replied in {} ms'.format(status.description['text'], status.players.online, status.latency)
            if status.players.online > 0:
                msg += ', online players:\r\n'
                for x in status.players.sample:
                    msg += ' - {}\r\n'.format(x.name)
            else:
                msg += '.'
        except Exception as e:
            print(e)
            msg = 'server_1: offline...'

        module.send_message_nowait(module.chat_default, msg)
