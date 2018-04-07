import discord
import asyncio
import tokencontainer

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as: ', client.user.name)
    print('id: ', client.user.id)

@client.event
async def on_message(message):
    if(message.content.startswith('!ping')):
        await client.send_message(message.channel, 'Pong!')
    if(message.content.startswith('!pong')):
        await client.send_message(message.channel, 'Niet zo flauw doen...')

client.run(id_token.get_token())