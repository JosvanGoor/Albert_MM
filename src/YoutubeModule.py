import discord
import asyncio
import youtube_dl
import ModuleBase as mb

class YoutubeModule (mb.ModuleBase):
    # asyncio.ensure_future(self.finalize_item())

    def __init__(self, client):
        self.client = client
        self.queue = []
        self.player = None
        self.voice = None
        self.channel = None
        self.timer = 0

        self.working = False

        print('Youtube module initialized...')

    # Generates this module's filter object and returns it.
    def get_filter(self):
        return '!yt'

    # This method gets called when a command arrives that passed this module's filter
    async def handle_message(self, message):
        args = message.content.split(' ')
        if(not args[0] == '!yt'):
            return 'YoutubeModule filter is misconfigured.'
        
        if(len(args) != 2): return 'YT: Needs exactely 1 argument...'

        if(args[1] == 'stop'):
            self.queue = []
            self.timer = 1
            return 'Stopping yt player'
        
        if(args[1] == 'next'):
            await self.play_next()
            return 'Playing next song...'

        if(self.channel == None):
            self.channel = message.author.voice_channel
            self.queue.append(args[1])
            
            try:
                self.voice = await self.client.join_voice_channel(self.channel)
                self.timer = 30
                return 'Playing song!'
            except discord.ClientException: 
                self.timer = 1
                return 'You are not in a voicechannel.'
            except discord.errors.InvalidArgument:
                self.channel = None
                self.queue = []
                return 'YT: Invalid url or request.'
        else:
            self.queue.append(args[1])
            return 'Added song to queue'

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        rval = 'Youtube player module version 1.0\r\n'
        rval += '    "!yt [link]" to play or queue a song.\r\n'
        rval += '    "!yt stop" to stop the player and empty the queue.\r\n'
        rval += '    "!yt next" to skip the current song.\r\n'

        return rval

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        if(self.player): return 'Ok! Playing song...'
        return 'Ok! idle...'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        return 'Verbose status not implemented yet...'

    # This method gets called once every second for time based operations.
    async def update(self):
        if(self.timer > -1):
            self.timer -= 1

        if self.timer == 0:
            await self.play_next()
            print('self.timer == 0')

    # Plays next song (if any)
    async def play_next(self):
        if self.working: return
        self.working = True

        # not connected, perform cleanup and return
        if(self.channel == None):
            self.queue = []
            if(self.player):
                self.player.stop()
                self.player = None
            if(self.voice):
                await self.voice.disconnect()
                self.voice = None
            return
        
        #if we are still playing stop the current player
        if(self.player):
            self.player.stop()

        # While there are still songs in the queue
        if len(self.queue) > 0:
            url = self.queue.pop()
            
            # Handles incorrect url's
            try:
                self.player = await self.voice.create_ytdl_player(url)
                if self.player.duration == 0:
                    self.timer = -2
                else:
                    self.timer = self.player.duration + 2
                    print('Set timer to ', timer)
                self.player.start()
            except discord.ClientException: 
                self.timer = 1
            except youtube_dl.utils.DownloadError:
                self.timer = 1
            
            self.working = False
            return
        
        else:
            self.channel = None
            self.timer = 1
            self.working = False
