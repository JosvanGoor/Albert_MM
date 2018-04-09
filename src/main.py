import discord
import asyncio
import logintoken as token

client = discord.Client()
modules = {}
general_module = None

async def ticker():
    await asyncio.sleep(1)
    asyncio.ensure_future(ticker())

    # update modules here
    for module in modules.values():
        module.update()

# setup
async def on_ready():
    print('Logged in as: ', client.user.name, '(', client.user.id, ')')

    for module in modules.values():
        module.on_ready()

    asyncio.ensure_future(ticker())

async def on_message(message):
    for key, value in modules.items():
        if(message.content.startswith(key)):
            value.handle_message(message)
            return
    
    if(general_module):
        general_module.handle_message(message)
