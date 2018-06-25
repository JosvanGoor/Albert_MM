import core.module as module
import re
import random

starting_gold = 100
cooldown_time = 5

def is_int(s):
    return re.match(r"[-+]?\d+$", s) is not None

class BetModule(module.Module):
    STATE_IDLE = 'idle'
    STATE_GAME = 'running game'
    STATE_FINSHED = 'finishing game'
    STATE_COOLDOWN = 'cooling down'

    def __init__(self, cashmoney):
        self.score = 0
        self.state = self.STATE_IDLE
        self.timer = -1
        self.players = []
        self.cashmoney = cashmoney

        print('BetModule initiated...')

    '''
        This method gets called when a command arrives that passed this module's filter
        This function can return a string which will be the bot's response.
    '''
    async def handle_message(self, message):
        if not message.channel.name == module.chat_default.name:
            return

        args = message.content.split(' ')

        if len(args) == 1:
            if self.state == self.STATE_IDLE or self.state == self.STATE_COOLDOWN:
                await module.dc_client.send_message(message.channel, 'There is currently no game to join.')
                return
            
            if message.author in self.players:
                await module.dc_client.send_message(message.channel, 'Hey! {} you can ony participate once!'.format(message.author.name))
            else:
                self.players.append(message.author)
                await module.dc_client.send_message(message.channel, 'welcome to the game {}!'.format(message.author.name))
            
        if len(args) == 2:
            if args[1] == 'help':
                await module.dc_client.send_message(message.channel, self.help_message())
                return True
            if args[1] == 'status':
                await module.dc_client.send_message(message.channel, self.status())
                return True
            
            if self.state == self.STATE_GAME:
                await module.dc_client.send_message(message.channel, 'There is already a game running silly')
                return
            
            if self.state == self.STATE_COOLDOWN or self.state == self.STATE_FINSHED:
                await module.dc_client.send_message(message.channel, 'Give me a few seconds to relax!')
                return

            if is_int(args[1]):
                msg = '{} has started a game for {}, type "!bet"  within 15 seconds to join!'
                value = int(args[1])
                
                if value > 100000000000000000000:
                    await module.dc_client.send_message(message.channel, 'eem nomoal...')
                    return

                if value < 1:
                    await module.dc_client.send_message(message.channel, 'noooooooope!')
                    return

                
                await module.dc_client.send_message(message.channel, msg.format(message.author.name, value))

                self.timer = 15
                self.score = value
                self.players = [message.author]
                self.state = self.STATE_GAME
                return

            


    '''
        This method gets called when help is called on this module.
        It should return a string explaining the usage of this module
    '''
    def help_message(self):
        msg = 'BetModule help:\r\n'
        msg += 'This module allows you to bet for gold!! with other players.\r\n\r\n'
        msg += 'Commands:\r\n'
        msg += '    "!bet <number>" starts a new bet people can join.'
        msg += '    "!bet" Join a bet, make sure you have enough gold!'
        return msg

    ''' Gets called once, when the client is connected. '''
    async def on_ready(self):
        pass

    ''' gets called when an update happens in any voice channel '''
    async def on_voice_change(self):
        pass

    ''' Status in 1 line (running! or error etc..) '''
    def short_status(self):
        return self.name() + ': ' + self.state

    '''
        This method gets called when status is called on this module. 
        It should return a string explaining the runtime status of this module.
    '''
    def status(self):
        msg = 'BetModule status:'
        if self.state == self.STATE_GAME:
            msg += ' A game is running, join now!\r\n\r\n'
            msg += 'Players:\r\n'
            for member in self.players:
                msg += '    ' + member.name + '\r\n'
        else:
            msg += self.state
        return msg

    ''' This method gets called once every second for time based operations. '''
    async def update(self):
        if self.state == self.STATE_IDLE:
            return
        
        print('self.state: {}'.format(self.state))
        print('self.timer: {}'.format(self.timer))
        
        if self.timer == 0:
            if self.state == self.STATE_GAME:
                self.state = self.STATE_FINSHED
                return
            
            if self.state == self.STATE_COOLDOWN:
                self.state = self.STATE_IDLE
                return

        if self.state == self.STATE_GAME:
            self.timer -= 1
            return
        
        if self.state == self.STATE_FINSHED:
            # Laat de scores binnenlopen met een seconde ertussen steeds.

            print('GAME SHOULD FINISH HERE')
            scores = []
            if len(self.players) == 1:
                await module.dc_client.send_message(module.chat_default, 'Nobody joined, what a shame =(')
                self.state = self.STATE_COOLDOWN
                self.timer = 5
                return
            
            for p in self.players:
                scores.append(random.randint(0, self.score))

            min = self.score + 12
            playermin = None
            max = 0
            playermax = None
            for i in range(0, len(self.players)):
                if scores[i] > max:
                    max = scores[i]
                    playermax = self.players[i]
                if scores[i] < min:
                    min = scores[i]
                    playermin = self.players[i]

            if playermax == playermin or playermax == None or playermin == None:
                await module.dc_client.send_message(module.chat_default, 'Nobody won, how rude =(')
                self.state = self.STATE_COOLDOWN
            
            msg = 'Round played for {}'.format(self.score)
            msg += '\r\n\r\nScores:\r\n'
            for i in range(0, len(self.players)):
                msg += '    {}: {}\r\n'.format(self.players[i].name, scores[i])
            
            if not playermin or not playermax:
                print("PLAYERMIN / PLAYERMAX NOT SET")
                msg += "An internal error occured..."
            else:
                msg += '\r\nLoser {} has lost {} gold to winner {}'.format(playermin.name, max - min, playermax.name)
                self.state = self.STATE_COOLDOWN
                self.timer = 5
            await module.dc_client.send_message(module.chat_default, msg)

            return

        if self.state == self.STATE_COOLDOWN:
            self.timer -= 1
            return
