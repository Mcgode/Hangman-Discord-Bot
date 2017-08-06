import logging
import discord
from HangmanLogic import HangmanLogic


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()
mail_address = "dummy@domain.com"  # Your Discord account mail address
password = "password"  # Your account password
master_account_name = "M_cgode"  # The name of your "admin" account
hangman_bot_account_name = "happiebot2"  # The name of Nadeko bot (the one with which you play hangman)
default_allowed_games = 5  # The amount of attempts this bot is allowed to make on startup
# You'll still have to launch a hangman game in the channel you want your bot to 'play', after it booted


global logic, allowed_servers


@client.event
async def on_ready():
    global logic, allowed_servers
    logic = HangmanLogic(default_allowed_games)
    allowed_servers = ['dummy_server']  # The servers your bot is allowed
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print('Available servers: ', [server.name for server in client.servers])
    print('------')


@client.event
async def on_message(message):

    await client.wait_until_ready()

    global logic, allowed_servers

    if message.channel.server and message.channel.server.name not in allowed_servers:
        return None

    if message.author.name == master_account_name:

        if message.content.startswith('!ping'):
            await client.send_message(message.channel, 'Pong!')

        elif message.content.startswith('!bye'):
            await client.send_message(message.channel, 'Bye!')
            print('Will logout')
            await client.logout()

        elif message.content.startswith('!servers'):
            await client.send_message(message.channel, [server.name for server in client.servers])

        elif message.content.startswith('!addsolve'):
            logic.number_of_remaining_games += int(message.content.split(' ')[1])
            if logic.current_status == "Idle":
                await client.send_message(message.channel, '.hangman Countries')

        elif message.content.startswith('!addserver'):
            allowed_servers.append(message.content.lstrip('!addserver '))
            await client.send_message(
                message.channel,
                'Just added the "**{0}**" server'.format(message.content.lstrip('!addserver '))
            )

    if message.author.display_name == hangman_bot_account_name:
        if len(message.embeds) > 0:
            if 'title' in message.embeds[0] and "hangman" in message.embeds[0]['title'].lower():
                await logic.call(client, message)


client.run(mail_address, password)


