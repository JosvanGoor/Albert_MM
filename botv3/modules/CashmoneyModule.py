import os
import json

import core.module as module

'''
    This module contains information and managing functions on the gold(tm) factors
    on the server.
'''

# some constants
STARTING_GOLD = 10000 #10K

BET_WON = "winning!"
BET_LOST = "losing!"
BET_TIED = "ehh who cares"

class CashmoneyModule(module.Module):
    
    def __init__(self):
        self._data = {}
        self._datafile = "data/CashmoneyModule.json"
        self._initialize()

        print("CashmoneyModule initialized...")

    #
    #   Maintenance
    #

    ' This function ensures that the member has relevant data setup '
    def validate_member(self, id):
        if not id in self._data:
            self._data[id] = \
            {
                "gold" : STARTING_GOLD,
                "transaction_lock" : False, # Used to prevent players from performing more then 1 transaction at the same time.
                "total_winnings" : 0,
                "total_losses" : 0,
                "bet_games_played" : 0,
                "bet_games_won" : 0,
                "bet_games_lost" : 0,
                "biggest_win" : 0,
                "biggest_loss" : 0,
                "biggest_game" : 0,
                "activity" : self._fresh_activity()
            }
            self._save_data() #not required

    def lock_member(self, id, validate = True):
        if validate:
            self.validate_member(id)

        if self._data[id]["transaction_lock"]:
            return False
        
        self._data[id]["transaction_lock"] = True
        return True

    def is_locked(self, id, validate = True):
        if validate:
            self.validate_member(id)
        return self._data[id]["transaction_lock"]

    def unlock_member(self, id):
        self._data[id]["transaction_lock"] = False

    def _fresh_activity(self):
        return \
        {
            "chats" : 0,
            "reactions" : 0,
            "voice" : False,
            "played" : False,
        }

    def _initialize(self):
        if os.path.isfile(self._datafile):
            with open(self._datafile, "r") as file:
                self._data = json.load(file)
        
        # reset any remaining locks
        for value in self._data.values():
            value["transaction_lock"] = False

    def _save_data(self):
        with open(self._datafile, "w+") as file:
            json.dump(self._data, file, indent = 4)
    #
    #   Meme-conomy
    #

    def update_after_bet(self, id, amount, limit, result = BET_TIED):
        
        self._data[id]["biggest_game"] = max(self._data[id]["biggest_game"])
        data["bet_games_played"] = 1 + data["bet_games_played"]

        if result == BET_WON:
            data["bet_games_won"] = 1 + data["bet_games_won"]
            data["total_winnings"] = amount + data["total_winnings"]
            if amount > data["biggest_win"]:
                data["biggest_win"] = amount

        elif result == BET_LOST:
            data["bet_games_lost"] = 1 + data["bet_games_lost"]
            data["total_losses"] = amount + data["total_losses"]
            if amount > data["biggest_loss"]:
                data["biggest_loss"] = amount

        self.unlock_member(id)

    def can_afford(self, id, amount, validate = True):
        if validate:
            self.validate_member(id)
        
        return self._data[id]["gold"] >= amount

    def balance_message(self, id, name):
        data = self._data[id]

        msg = "Hey {}!\r\n\r\n".format(name)
        msg += "You have {} gold!\r\n".format(data["gold"])
        return msg

    # does not lock since this is a single thread class, and this op is instant.
    def transfer(self, amount, from_id, to_id):
        self.validate_member(from_id) #validations shouldn't be required here
        self.validate_member(to_id)

        self._data[from_id]["gold"] -= amount
        self._data[to_id]["gold"] += amount

        #store changes
        self._save_data()

    #
    #   Activity updates
    #

    def on_chat(self, id):
        if id in self._data:
            self._data[id]["activity"]["chats"] += 1

    def on_reaction(self, id):
        if id in self._data:
            self._data[id]["activity"]["reactions"] += 1

    ' Voice is future work '

    #
    #   Module overwrites
    #

    async def handle_message(self, message):
        if not message.content.startswith("!wallet"):
            return

        if not message.channel.is_private and not message.channel.name == module.chat_default.name:
            return

        args = message.content.split(" ")
        if len(args) < 2:
            return

        if args[1] == "balance":
            self.validate_member(message.author.id)
            msg = self.balance_message(message.author.id, module.strip_name(message.author))
            await module.dc_client.send_message(message.channel, msg)

    def help_message(self):
        return "CashmoneyModule help: WIP"

    def short_status(self):
        return "CashmoneyModule: Ya'll broke!"

    def status(self):
        return short_status()
