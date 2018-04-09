# Module.py defines a module baseclass used to register with the python core.

class ModuleBase:

    # Gets called when the connection is completed
    async def on_ready(self):
        pass

    def get_filter(self):
        ''' Generates this module's filter object and returns it. '''
        raise NotImplementedError()

    async def handle_message(self, message):
    ''' This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response. '''
        raise NotImplementedError()

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        raise NotImplementedError()

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        raise NotImplementedError()

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        raise NotImplementedError()

    # This method gets called once every second for time based operations.
    async def update(self):
        raise NotImplementedError()
