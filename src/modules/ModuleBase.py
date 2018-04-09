# Module.py defines a module baseclass used to register with the python core.

class ModuleBase:

    # initializer, binds client handle
    def __init__(self, client):
        self.client = client

    # Gets called once, when the client is connected.
    async def on_ready(self):
        pass

    # Generates this module's filter object and returns it.
    def get_filter(self):
        raise NotImplementedError()

    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        args = message.content.split(' ')
        if len(args) == 1:
            await self.client.send_message(message.channel, self.help_message())
            return
            
        if len(args) == 2:
            if args[1] == 'help':
                await self.client.send_message(message.channel, self.help_message())
                return
            if args[1] == 'status':
                await self.client.send_message(message.channel, self.status())
                return

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        raise NotImplementedError()

    # Returns the name of the module.
    def name(self):
        return 'Bad programming'

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        raise NotImplementedError()

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        raise NotImplementedError()

    # This method gets called once every second for time based operations.
    async def update(self):
        pass
