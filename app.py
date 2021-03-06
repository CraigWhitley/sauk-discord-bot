# Jake!#4988
import discord
from typing import List
import datetime as dt
from bot_settings import BotSettings
from commands.register_commands import commands
import dotenv
import os


dotenv.load_dotenv()


client = discord.Client()
text_channels = []
prefix = "!"


def get_user_from_id(username: str, message) -> discord.Member:
    member = discord.utils.get(message.guild.members, name=username)

    return member


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    BotSettings.client = client

    channels: List[discord.abc.GuildChannel] = client.get_all_channels()

    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            BotSettings.text_channels.append(channel)
            print(channel.name)


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix) is False:
        return

    split_message: [] = message.content.split(" ")

    command: str = split_message[0].replace("!", "", 1)

    result: bool = any(x == command for x in commands)

    if result is False:
        # Send the default --help
        return

    command_args = []

    if len(split_message) > 1:
        command_args = split_message[1:]

    # We store the function inside the commands dictionary.
    # commands["help"](*args)
    # executes the default help command with *args.
    await commands[command](message, *command_args)

client.run(os.getenv("DISCORD"))
