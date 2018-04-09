import discord
import asyncio
import sys
import signal
import logintoken as token
import identity

import YoutubeModule as yt


running = True
timer = 0
client = discord.Client()
yutub = yt.YoutubeModule(client)

async def set_identity():
    print('timer is ', timer, ' running set_identity()')

    person = identity.get_peep()

    avatar_url = person['results'][0]['picture']['large']
    avatar_img = identity.get_avatar(avatar_url)

    for server in client.servers:
        naam = person['results'][0]['name']['first']
        naam += ' ' + person['results'][0]['name']['last']

        await client.change_nickname(server.me, naam.title())
        try:
            await asyncio.wait_for(client.edit_profile(avatar = avatar_img), 15)
            print('successfully changed avatar!')
        except discord.errors.HTTPException:
            print('Failed to set avatar :(')
        except asyncio.TimeoutError:
            print('Caught timeouterror!')
            
        break




# asyncio.ensure_future(self.finalize_item())
async def ticker():
    await asyncio.sleep(1)
    asyncio.ensure_future(ticker())
    
    global timer
    timer += 1
    print('\rtimer: ', timer, end='')


    await yutub.update()
    
    if timer % 900 == 0:
        await set_identity()

    if not running:
        return # of toch....


@client.event
async def on_ready():
    global timer

    print('Logged in as: ', client.user.name)
    print('id: ', client.user.id)

    signal.signal(signal.SIGINT, signal_handler)
    await set_identity()
    
    asyncio.ensure_future(ticker()) #starts the tickerloop FOREVA

@client.event
async def on_message(message):
    if(message.content.startswith('!ping')):
        await client.send_message(message.channel, 'Pong!')
    elif(message.content.startswith('!pong')):
        await client.send_message(message.channel, 'Niet zo flauw doen...')
    elif(message.content.startswith('!ticker')):
        await client.send_message(message.channel, 'Running for ' + str(timer) + ' seconds')


    elif(not message.channel.name == "botspam"): return

    elif(message.content.startswith('!yt')):
        rval = await yutub.handle_message(message)
        if(rval):
            await client.send_message(message.channel, rval)

    elif(message.content.startswith('!help')):
        msg = 'Albert the MagikMan bot v1.0\r\nrunning modules: Youtube player\r\n\r\n'
        msg += '!ping me, but I dont like to be pong-ed...\r\n\r\n'
        msg += yutub.help_message()
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!quit'):
        if (message.author.name.lower() == 'wavycolt' or message.author.name.lower() == 'boerenkool'):
            quitter()
        else:
            await client.send_message(message.channel, 'No =(')

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def quitter():
    running = False
    asyncio.ensure_future(client.close())


client.run(token.get_token())