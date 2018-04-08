# Module.py defines a module baseclass used to register with the python core.

class ModuleBase:

    # Generates this module's filter object and returns it.
    def get_filter(self):
        raise NotImplementedError()

    # This method gets called when a command arrives that passed this module's filter
    async def handle_message(self, message, client):
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
    def update(self):
        raise NotImplementedError()
