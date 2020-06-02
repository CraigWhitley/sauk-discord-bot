import discord
from typing import List


class BotSettings:
    client: discord.Client = None
    text_channels: List[discord.TextChannel] = []
