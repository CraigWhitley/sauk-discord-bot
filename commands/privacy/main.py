# Credits to Schmoo for the idea!
import discord
from bot_settings import BotSettings
import datetime
import time
from discord.errors import Forbidden, HTTPException, NotFound


help_message: str = """
**!privacy** *<amount_of_days_to_purge_before> <channel | all>*

**Example #1:**
**!privacy** *7 general*
This will delete all of your messages prior to 7 days ago in the **#general** channel.
--------
**Example #2:**
**!privacy** *14 all*
This will delete all of your messages prior to 14 days ago in *every* channel!
"""


async def delete_users_message_history(message: discord.Message,
                                       *args):

    # Initialize our locals:
    user = message.author

    channel = message.channel

    amount_of_days: int = None

    bot_spam: bool = channel.name == "bot-spam"

    channel_to_purge_from: discord.TextChannel = None

    date_to_purge_before: datetime = None

    # Handle the help command:
    if len(args) > 0:
        result = any(x == "--help" or
                     x == "--h" or
                     x == "-help" or
                     x == "-h" for x in args)

        if result is True:
            await _send_help_message(bot_spam, user, channel)
            return

    if len(args) < 2:
        await _send_help_message(bot_spam, user, channel)
        return

    # Attempt to parse the first argument to an integer:
    try:
        amount_of_days: int = int(args[0])
    except(ValueError):
        await _send_help_message(bot_spam, user, channel)
        return

    # This will purge every single one of your messages:
    if amount_of_days < 0:
        amount_of_days = 0

    # Retrieve the datetime to purge messages before:
    today = datetime.datetime.now()
    date_to_purge_before: datetime.datetime = today - datetime.timedelta(days=amount_of_days)
    # date_to_purge_before: datetime.datetime = today - datetime.timedelta(minutes=amount_of_days)

    # If no channel provided, purge from all channels:
    if args[1] == "all":
        await _purge_from_all(user, date_to_purge_before)
        return

    # Get the TextChannel from BotSettings that corresponds to
    # the channel name passed in as the second argument:
    channel_to_purge_from = [i for i in BotSettings.text_channels
                             if i.name == args[1]].pop()

    # If we have a valid channel, purge from that channel:
    if channel_to_purge_from is not None:
        await _purge_from_channel(user,
                                  channel_to_purge_from,
                                  date_to_purge_before)
        return

    # Fallback on the help command:
    await _send_help_message(bot_spam, user, channel)


async def _send_help_message(bot_spam: bool,
                             user: discord.Member,
                             channel: discord.TextChannel):
    """
    Acts a switch between responding to the help
    command in DM or responding in the bot-spam channel.
    If the command was issued from bot-spam, respond there.
    """
    if bot_spam is True:
        await _respond_with_help_message_in_botspam(channel)
    else:
        await _respond_with_help_message_in_pm(user)


async def _respond_with_help_message_in_pm(user):
    await user.send(help_message)


async def _respond_with_help_message_in_botspam(channel):
    await channel.send(help_message)


async def _purge_from_all(user: discord.Member,
                          date_to_purge_before: datetime):

    start_time: time = time.time()
    end_time: time = None
    count: int = 0

    for channel in BotSettings.text_channels:
        async for message in channel.history(limit=99999999,
                                             before=date_to_purge_before):
            try:
                await message.delete()
            except(NotFound):
                print("Message id {} not found.".format(str(message.id)))
            except(Forbidden):
                print("You do not have permission to delete {}".format(str(message.id)))
            except(HTTPException):
                print("HTTPException: {}".format(HTTPException.text))
            finally:
                count += 1
                print("Messages deleted {}...".format(str(count)))
                print("Last message id: {}".format(str(message.id)))
                time.sleep(2)

    end_time = time.time()
    finish_time = (end_time - start_time) / 60
    print("Deleted {} messages in {} minutes".format(str(count),
                                                     str(finish_time)))


async def _purge_from_channel(user: discord.Member,
                              channel: discord.TextChannel,
                              date_to_purge_before: datetime):

    async for message in channel.history(limit=99999999,
                                         before=date_to_purge_before):
        await message.delete()
