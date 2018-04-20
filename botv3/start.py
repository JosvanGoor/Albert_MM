import discord
import asyncio
import logintoken as token

import core.module as module
import core.worker as worker
import modules.GeneralModule as gm
import modules.IdentityModule as im
import modules.ServerInfoModule as sim
import modules.YoutubeModule as ym

dc_client = discord.Client()
modules = {}
general_module = None

'''
    If connection succeeds, register modules
'''
def register_modules():
    global dc_client
    global general_module

    module.dc_client = dc_client
    worker.initialize(3)

    #modules['!command'] = Module()
    modules['!yt'] = ym.YoutubeModule()
    modules['!info'] = sim.ServerInfoModule()
    modules['!name'] = im.IdentityModule()

    general_module = gm.GeneralModule(modules)

''' ticks 1'ce per second for modules that require time based updates '''
async def ticker():
    global modules

    await asyncio.sleep(1)
    asyncio.ensure_future(ticker())

    for mod in modules.values():
        await mod.update()

''' setup-on-connect '''
@dc_client.event
async def on_ready():
    global modules
    global general_module
    
    print('Logged in as: ', dc_client.user.name, '(', dc_client.user.id, ')')

    register_modules()

    for module in modules.values():
        await module.on_ready()
    await general_module.on_ready()

    asyncio.ensure_future(ticker())

''' 
    dispatch messages to relevant modules 
    No relevant module found -> send it to the general module
'''
@dc_client.event
async def on_message(message):
    for key, value in modules.items():
        if(message.content.startswith(key)):
            await value.handle_message(message)
            return
    
    await general_module.handle_message(message)

'''
    Update joins/leaves of voice channels to modules.
'''
@dc_client.event
async def on_voice_state_update(before, after):
    for value in modules.values():
        await value.on_voice_change()

    await general_module.on_voice_change()

# run the thing
dc_client.run(token.get_token())