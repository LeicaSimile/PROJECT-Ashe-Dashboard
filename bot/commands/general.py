import discord
from discord.ext import commands

import settings
import phrases


class General(object):
    """General commands."""

    def __init__(self, bot):
        """
        Args:
            bot(projectashe.Bot): Bot instance.
        """
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def shutdown(self, context):
        if context.message.author.id == settings.OWNER_ID:
            shutdown_msg = self.bot.get_phrase(phrases.Category.SHUTDOWN.value)
            await self.bot.client.send_message(context.message.channel, shutdown_msg)
            await self.bot.client.logout()
        else:
            message = "Don't tell me what to do."
            await self.bot.client.send_message(context.message.channel, message)


class Debugging(object):
    """Commands for debugging and testing."""

    def __init__(self, bot):
        """
        Args:
            bot(projectashe.Bot): Bot instance.
        """
        self.bot = bot

    @commands.command(description="Tells you your user ID.", pass_context=True)
    async def getid(self, context):
        user_id = context.message.author.id
        user_name = context.message.author.mention
        
        await self.bot.client.send_message(context.message.channel,
                                           f"{user_name}, your ID is {user_id}")

