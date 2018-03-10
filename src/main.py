import discord
from credentials import cred
from games.game_2048 import Game2048

client = discord.Client()
games = {}


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        await client.add_reaction(tmp, emoji="➡")
        respond = await client.wait_for_reaction(message=tmp, check=lambda r, u: u != client.user)

        await client.send_message(message.channel,
                                  "{0.user} reacted with {0.reaction.emoji}".format(respond))
    elif message.content.startswith('!game'):
        games[message.author] = Game2048(client, message.author, message.channel)
        await games[message.author].run()
    elif message.content.startswith('!stop'):
        if games[message.author] is not None:
            await games[message.author].stop()
            games[message.author] = None


client.run(cred['bot_token'])
