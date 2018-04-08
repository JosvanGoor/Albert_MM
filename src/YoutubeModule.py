import discord
import asyncio
import ModuleBase as mb

class YoutubeModule (mb.ModuleBase):

    def __init__(self, client):
        self.client = client
        self.queue = []
        self.player = None
        self.voice = None
        self.timer = 0

    # Generates this module's filter object and returns it.
    def get_filter(self):
        return '!yt'

    # This method gets called when a command arrives that passed this module's filter
    async def handle_message(self, message, client):
        

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
        if(self.player) return 'Ok! Playing song...'
        return 'Ok! idle...'

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        return 'Verbose status not implemented yet...'

    # This method gets called once every second for time based operations.
    def update(self):
        raise NotImplementedError()
    
    
    
    
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.player = None
        self.voice_client = None
        self.task = None

        asyncio.ensure_future(self.finalize_item())

        print('Initialized YoutubeModule...')

    def get_filter(self):
        return "!yt"

    async def handle_message(self, message):
        args = message.content.split(' ')
        if not args[0] == '!yt':
            print('YoutubeModule::handle_message - filter failed.')
            return 
        
        if len(args) < 2 or len(args) > 2: return

        if args[1] == 'stop':
            self.queue = []
            if(self.player):
                self.player.stop()
                self.player = None
                await self.voice_client.disconnect()
                self.voice_client = None

        elif self.player and self.player.is_playing():
            self.queue.append(args[1])
            return 'queued song!'

        elif not self.player:
            url = args[1]
            channel = message.author.voice_channel
            self.voice_client = await self.client.join_voice_channel(channel)
            self.player = await self.voice_client.create_ytdl_player(url)
            print('calling self.player.start()')
            self.player.start()
        
        return 'ok!'

    async def finalize_item(self):
        await asyncio.sleep(1)

        if(self.player and self.player.is_playing()):
            asyncio.ensure_future(self.finalize_item())

        elif len(self.queue) > 0:
            print('Running next song!...')
            song = queue.pop()
            self.player = await self.voice_client.create_ytdl_player(url, after = self.finalize_item)
            await finalize_item()
        
        elif(self.player):
            print('Kiling player!...')
            self.player.stop()
            self.player = None
            self.voice_client.disconnect()
            self.voice_client = None