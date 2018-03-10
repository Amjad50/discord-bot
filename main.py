import discord
from firebase_admin.db import TransactionError
from Database import database
from credentials import cred

client = discord.Client()
db = database.Database(cred['cert'],
                       cred['database_url'],
                       app_name="bot-test"
                       )


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
        await client.add_reaction(tmp, emoji="🍋")
        respond = await client.wait_for_reaction(message=tmp, check=lambda r, u: u != client.user)
        try:
            db.get_reference(
                "reactions/users/{}/number".format(respond.user.name + respond.user.id)) \
                .transaction(lambda value: value + 1 if value else 1)
        except TransactionError:
            print("transaction failed!")

        await db.write("reactions/users/{0}".format(respond.user.name + respond.user.id),
                       {'emoji': respond.reaction.emoji}, update=True)
        await client.send_message(message.channel,
                                  "{0.user} reacted with {0.reaction.emoji}".format(respond))
    elif message.content.startswith('!sleep'):
        await client.send_message(message.channel, 'Done sleeping')


client.run(cred['bot_token'])
