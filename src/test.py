import discord
import asyncio
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

    asyncio.ensure_future(ticker()) #starts the tickerloop FOREVA

@client.event
async def on_message(message):
    if(message.content.startswith('!ping')):
        await client.send_message(message.channel, 'Pong!')
    if(message.content.startswith('!pong')):
        await client.send_message(message.channel, 'Niet zo flauw doen...')

    if(not message.channel.name == "botspam"): return

    if(message.content.startswith('!yt')):
        rval = await yutub.handle_message(message)
        if(rval):
            await client.send_message(message.channel, rval)

client.run(token.get_token())