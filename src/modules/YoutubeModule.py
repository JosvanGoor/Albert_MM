import discord
import asyncio
import youtube_dl
import module.ModuleBase as base

class YoutubeModule(base.ModuleBase):

    def __init__(self, client):
        super().__init__(client)
        self.queue = []
        self.player = None
        self.voice = None
        self.channel = None
        self.timer = 0

    # Gets called once, when the client is connected.
    async def on_ready(self):
        pass

    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        

        await super().handle_message(message)

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        msg = '!yt: YoutubeModule\r\n'
        msg += 'This module allows you to play the sound of youtube videos in your current voice channel.\r\n\r\n'
        msg += 'Commands:\r\n'
        msg += '    "!yt <url>": Plays the url, or adds the url to the playqueue.\r\n'
        msg += '    "!yt next": Skips to the next song in the queue\r\n'
        msg += '    "!yt stop": Stops playback and clears the queue\r\n'
        return msg

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        if(self.player): return 'YoutubeModule: Playing'
        return 'YoutubeModule: Idle'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        if(self.player): return 'YoutubeModule: Playing'
        return 'YoutubeModule: Idle'

    # This method gets called once every second for time based operations.
    async def update(self):
        pass
