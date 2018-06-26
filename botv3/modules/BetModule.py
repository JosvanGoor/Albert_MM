import re
import random
from operator import itemgetter

import core.module as module
import modules.CashmoneyModule as cash

def is_int(input):
    return re.match(r"[-+]?\d+$", input) is not None

STATE_IDLE = "idle"
STATE_INGAME = "running game"
STATE_FINISHED = "finishing game"
STATE_COOLDOWN = "cooling down"

class GameContainer:

    def __init__(self):
        self.players = []

        self.timer = -1
        self.limit = -1

    def has_ties(self):
        if len(self.players) >= 2:
            if self.players[0][1] == self.players[1][1]:
                return True
            if self.players[-1][1] == self.players[-2][1]:
                return True
            return False
        return False

    def add_player(self, player, cashmoney):
        for mem, val in self.players:
            if mem.id == player.id:
                return False

        if not cashmoney.can_afford(player.id, self.limit):
            msg = "{}... you cant afford that man!".format(module.strip_name(player))
            module.send_message_nowait(module.chat_default, msg)
            return False

        if not cashmoney.lock_member(player.id):
            msg = "{}! You are already in a transaction!".format(module.strip_name(player))
            module.send_message_nowait(module.chat_default, msg)
            return False

        score = random.randint(0, self.limit)
        self.players.append((player, score))
        msg = "Welcome to the game {}!".format(module.strip_name(player))
        module.send_message_nowait(module.chat_default, msg)
        return True

    def randomize(self):
        for it in range(0, len(self.players)):
            print("Rerolling bets")
            self.players[0] = (self.players[0][0], random.randint(0, self.limit))

    def sort(self):
        self.players = sorted(self.players, key=itemgetter(1), reverse = True)

    def finalize(self, cashmoney):
        self.timer = -1
        self.sort()

        # attempt to break tie's max 3 times.
        for it in range(0, 3):
            if not self.has_ties():
                break
            self.randomize()
            self.sort()

        if self.has_ties():
            module.send_message_nowait(module.chat_default, "Match ended in a tie.. nothing happend.")
            for it in range(0, len(self.players)):
                cashmoney.unlock_member(self.players[it][0].id)
            return

        difference = self.players[0][1] - self.players[-1][1]

        msg = "Round played for {} gold!\r\n\r\n".format(self.limit)
        msg += "Scores:\r\n"
        for player, score in self.players:
            msg += "    - {}: {}\r\n".format(module.strip_name(player), score)

        msg += "\r\n{} lost {} gold to {}!".format(
            module.strip_name(self.players[0][0]),
            difference,
            module.strip_name(self.players[-1][0]))

        cashmoney.transfer(difference, self.players[0][0].id, self.players[-1][0].id, False)
        cashmoney.update_after_bet(self.players[0][0].id, difference, self.limit, cash.BET_WON)
        cashmoney.update_after_bet(self.players[-1][0].id, difference, self.limit, cash.BET_LOST)

        for it in range(1, len(self.players) - 1):
            cashmoney.update_after_bet(self.players[it][0].id, self.limit, difference)
        
        cashmoney._save_data()
        module.send_message_nowait(module.chat_default, msg)
        
        self.players = []
        self.limit = -1


#
#   MODULE PART
#

class BetModule(module.Module):

    def __init__(self, cashmoney):
        self.cashmoney = cashmoney
        self.game = GameContainer()

        print("BetModule initialized...")

    async def handle_message(self, message):
        if not message.channel.name == module.chat_default.name:
            return

        args = message.content.split(" ")

        if len(args) == 1 and not self.game.timer == -1:
            self.game.add_player(message.author, self.cashmoney)
            return

        if len(args) == 2:
            if args[1] == "help":
                await module.dc_client.send_message(message.channel, self.help_message())
                return
            
            if args[1] == "status":
                await module.dc_client.send_message(message.channel, self.status())
                return

            if not self.game.timer == -1:
                await module.dc_client.send_message(message.channel, 'There is already a game running silly')
                return

            if is_int(args[1]):
                value = int(args[1])

                if value <= -1:
                    await module.dc_client.send_message(message.channel, 'Yeah... No!')
                    return

                if not self.cashmoney.can_afford(message.author.id, value):
                    await module.dc_client.send_message(message.channel, 'You cannot afford that LOL!')
                    return

                if self.cashmoney.is_locked(message.author.id):
                    await module.dc_client.send_message(message.channel, 'Cant start a game when in a transaction.')
                    return

                await module.dc_client.send_message(message.channel, 'A game has started worth {} gold! Join within 15 seconds by typing !bet.'.format(value))
                self.game.players = []
                self.game.timer = 15
                self.game.limit = value
                self.game.add_player(message.author, self.cashmoney)



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

    ''' Status in 1 line (running! or error etc..) '''
    def short_status(self):
        msg = "{}: {}"
        if self.game.timer == -1:
            return msg.format(self.name(), "Idle...")
        else:
            return msg.format(self.name(), "Running a game!")

    '''
        This method gets called when status is called on this module. 
        It should return a string explaining the runtime status of this module.
    '''
    def status(self):
        msg = 'BetModule status:'
        if not self.game.timer == -1:
            msg += "A game is running, join now!\r\n\r\n"
            return msg
        else:
            return self.short_status()

    async def update(self):
        if not self.game.timer == -1:
            self.game.timer -= 1

        if self.game.timer == 0:
            
            if len(self.game.players) <= 1:
                await module.dc_client.send_message(module.chat_default, 'Nobody joined =( what a shame...')
                self.game.timer = -1
                for it in range(0, len(self.game.players)):
                    self.cashmoney.unlock_member(self.game.players[it][0])

                return

            self.game.finalize(self.cashmoney)
