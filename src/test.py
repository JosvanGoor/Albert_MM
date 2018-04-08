import discord
import asyncio
import signal
import sys
import tokenfile as token

import YoutubeModule as yt

client = discord.Client()
yutub = yt.YoutubeModule(client)

# asyncio.ensure_future(self.finalize_item())
async def ticker():
    await asyncio.sleep(1)
    await yutub.update()
    asyncio.ensure_future(ticker())



@client.event
async def on_ready():
    print('Logged in as: ', client.user.name)
    print('id: ', client.user.id)

    asyncio.ensure_future(ticker())
    #signal.signal(signal.SIGINT, ctrl_c_handler)

@client.event
async def on_message(message):
    if(not message.channel.name == "botspam"): return

    if(message.content.startswith('!ping')):
        await client.send_message(message.channel, 'Pong!')
    if(message.content.startswith('!pong')):
        await client.send_message(message.channel, 'Niet zo flauw doen...')
    if(message.content.startswith('!yt')):
        rval = await yutub.handle_message(message)
        await client.send_message(message.channel, rval)
        # url = message.content.split(' ')[1]
        # channel = message.author.voice_channel
        # await youtube(channel, url)

async def youtube(channel, url):
    cn = await client.join_voice_channel(channel)
    player = await cn.create_ytdl_player(url)
    player.start()

async def ctrl_c_handler(signal, frame):
    print('Caught ctrl+c, closing connection...')
    client.close()
    sys.exit()


client.run(token.get_token())