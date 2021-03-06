import asyncio
import discord
import re
import youtube_dl
import modules.ModuleBase as base
import modules.YoutubeListWorker as ytlw
from threading import Thread

class YoutubeModule(base.ModuleBase):
    STATE_IDLE = "idle"          # not playing anything
    STATE_PLAYING = "Playing"    # playing a song
    STATE_STARTING = "Starting"  # starting up a song
    STATE_STOPPING = "Stopping"  # cleaning up


    def __init__(self, client):
        super().__init__(client)
        self.queue = []
        self.player = None
        self.voice = None
        self.channel = None
        self.chat = None
        self.song = ""
        self.state = self.STATE_IDLE
        self.timer = -1

        print('YoutubeModule initialized...')

    # Gets called once, when the client is connected.
    async def on_ready(self):
        pass

    async def on_voice_change(self):
        if not self.voice:
            return
        
        if len(self.voice.channel.voice_members) == 1:
            self.state = self.STATE_STOPPING


    # This method gets called when a command arrives that passed this module's filter
    # This function can return a string which will be the bot's response.
    async def handle_message(self, message):
        if not message.channel.name == 'botspam': return

        self.channel = message.author.voice_channel
        self.chat = message.channel
        args = message.content.split(' ')

        if len(args) == 2:
            if args[1] == 'stop':
                self.state = self.STATE_STOPPING
                return

            if args[1] == 'next':
                self.state = self.STATE_STARTING
                return

            if args[1] == 'play':
                if not self.state == self.STATE_IDLE:
                    await self.client.send_message(message.channel, 'Already working :)')
                elif len(self.queue) == 0:
                    await self.client.send_message(message.channel, 'Playqueue is empty...')
                else:
                    self.state = self.STATE_STARTING
                return
                
            if args[1] == 'reset':
                self.state = self.STATE_STOPPING
                self.queue = []
                return
        
        if await super().handle_message(message):
            return

        # it must be a link then, start playin bojj
        # check input
        if re.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', args[1]):
            if '&list=' in args[1]:
                await self.client.send_message(message.channel, 'This seems to be a playlist, this might take some time :)')
                
                t1 = ytlw.ytl_worker(args[1], self)
                t1.start()
                return
            
            self.queue.append(args[1])
            self.channel = message.author.voice_channel

            if self.state == self.STATE_IDLE: # not if were busy tho
                self.state = self.STATE_STARTING
        else:
            await self.client.send_message(message.channel, 'That is not a youtube url you cheeky bastard :)')
       

    # This method gets called when help is called on this module. This should return a string explaining the usage
    # of this module
    def help_message(self):
        msg = 'YoutubeModule help:\r\n'
        msg += 'This module allows you to play the sound of youtube videos in your current voice channel.\r\n\r\n'
        msg += 'Commands:\r\n'
        msg += '    "!yt <url>": Plays the url, or adds the url to the playqueue.\r\n'
        msg += '    "!yt next": Skips to the next song in the queue\r\n'
        msg += '    "!yt play": Starts playback if there are songs in the queue\r\n'
        msg += '    "!yt stop": Stops playback\r\n'
        msg += '    "!yt reset: Stops playback and clears the queue\r\n'
        return msg

    # Status in 1 line (running! or error etc..)
    def short_status(self):
        rval = ''
        if self.state == self.STATE_PLAYING:
            rval += 'YoutubeModule: playing "' + self.song + '"'
        else:
            rval += 'YoutubeModule: ' + self.state

        rval += ' (' + str(len(self.queue)) + ' in queue)'
        return rval

    # This method gets called when status is called on this module. This should return a string explaining the
    # runtime status of this module.
    def status(self):
        if not self.state == self.STATE_PLAYING:
            return self.short_status()
        
        msg = 'YoutubeModule - Playing audio\r\n'
        msg += '    Song: ' + self.song + '\r\n'
        msg += '    queue: ' + str(len(self.queue)) + '\r\n'
        return msg

    # This method gets called once every second for time based operations.
    async def update(self):
        # not doing anything, return
        if self.state == self.STATE_IDLE:
            return

        # update timer and go to starting if song ended
        if self.state == self.STATE_PLAYING:
            self.timer -= 1
            if self.timer == 0:
                self.state = self.STATE_STARTING
            return
        
        # clean resources.
        if self.state == self.STATE_STOPPING:
            print('State = stopping')
            self.song = ""
            self.state = self.STATE_IDLE

            if(self.player):
                self.player.stop()
                self.player = None
            if(self.voice):
                await self.voice.disconnect()
                self.voice = None
            
            return

        # somebody said music?
        if self.state == self.STATE_STARTING:
            self.state = self.STATE_PLAYING
            # No! =(
            if len(self.queue) == 0:
                self.state = self.STATE_STOPPING
                return
            
            # clean this old shit up
            if self.player:
                self.player.stop()
                self.player = None

            song = self.queue.pop(0)
            try:
                if not self.voice:
                    self.voice = await self.client.join_voice_channel(self.channel)
                
                self.player = await self.voice.create_ytdl_player(song)
                if(self.player.is_live): 
                    self.state = self.STATE_STARTING
                    #self.timer = -1
                    return
                else: self.timer = self.player.duration + 2

                self.song = self.player.title
                self.player.start()
            except discord.ClientException as e:
                print(e)
                self.state = self.STATE_STARTING
            except youtube_dl.utils.DownloadError as e:
                print(e)
                self.state = self.STATE_STARTING
                self.timer = -1



