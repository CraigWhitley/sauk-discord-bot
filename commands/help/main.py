import discord

multiline_message = """
Test help response!
Example of a *multiline* response
using discord **markup**
"""


# This is the entry point to the command.
async def send_default_help(message: discord.Message,
                            *command_args):
    if len(command_args) > 1:
        for x in command_args:
            print(x)

    await message.channel.send(multiline_message)
