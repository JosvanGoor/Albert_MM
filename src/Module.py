# Module.py defines a module baseclass used to register with the python core.

class Module:

    # Generates this module's filter object and returns it.
    def get_filter(self):
        raise NotImplementedError()

    # This method gets called when a command arrives that passed this module's filter
    async def handle_message(self, message, client):
        raise NotImplementedError()

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    async def help_string(self):
        raise NotImplementedError()

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    async def status_string(self):
        raise NotImplementedError()