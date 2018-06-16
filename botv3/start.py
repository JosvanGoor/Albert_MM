import asyncio
import discord
import signal
import sys

import logintoken as token
import core.module as module
import core.userdata as userdata
import core.worker as worker
import modules.BetModule as bm
import modules.GeneralModule as gm
import modules.IdentityModule as im
import modules.ServerInfoModule as sim
import modules.YoutubeModule as ym
import modules.StreamModule as sm

dc_client = discord.Client()
modules = {}
general_module = None

def shutdown(loop):
    for task in asyncio.Task.all_tasks():
        task.cancel()

def _ctrlc_handler(signal, frame):
    print("Caught ctrl+c signal...")
    worker.finalize()
    shutdown(None)
    

'''
    If connection succeeds, register modules
'''
def register_modules():
    global dc_client
    global general_module
    
    signal.signal(signal.SIGINT, _ctrlc_handler)

    module.dc_client = dc_client
    module.chat_default = module.channel_by_name('botspam')
    worker.initialize(3, asyncio.get_event_loop())
    userdata.initialize()

    #modules['!command'] = Module()
    modules['!yt'] = ym.YoutubeModule()
    modules['!info'] = sim.ServerInfoModule()
    modules['!name'] = im.IdentityModule()
    modules['!bet'] = bm.BetModule()
    modules["!stream"] = sm.StreamModule(module.channel_by_name('e-sports'))

    general_module = gm.GeneralModule(modules)

''' ticks 1'ce per second for modules that require time based updates '''
async def ticker():
    global modules

    while True:
        await asyncio.sleep(1)

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
