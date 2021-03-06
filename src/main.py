import discord
import asyncio
import logintoken as token

import modules.GeneralModule as gm
import modules.YoutubeModule as yt
import modules.IdentityModule as im

client = discord.Client()
modules = {}
general_module = None

def register_modules():
    global client
    global modules

    #modules['!command'] = Module()
    modules['!yt'] = yt.YoutubeModule(client)
    modules['!name'] = im.Identity(client)

    pass

# ticks 1'ce per second for modules
# that require time based updates
async def ticker():
    global modules

    await asyncio.sleep(1)
    asyncio.ensure_future(ticker())

    for module in modules.values():
        await module.update()

# setup-on-connect
@client.event
async def on_ready():
    global modules
    global general_module

    print('Logged in as: ', client.user.name, '(', client.user.id, ')')

    general_module = gm.GeneralModule(client, modules)
    register_modules()

    for module in modules.values():
        await module.on_ready()
    await general_module.on_ready()

    asyncio.ensure_future(ticker())

# dispatch messages to relevant modules
# No relevant module found -> send it to the general module
@client.event
async def on_message(message):
    for key, value in modules.items():
        if(message.content.startswith(key)):
            print('DEBUG: sending message to: ', key)
            await value.handle_message(message)
            return
    
    await general_module.handle_message(message)

@client.event
async def on_voice_state_update(before, after):
    for value in modules.values():
        await value.on_voice_change()

    await general_module.on_voice_change()

# run the thing
client.run(token.get_token())
