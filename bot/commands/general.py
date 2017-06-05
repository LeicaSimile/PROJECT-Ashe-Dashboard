import discord
from discord.ext import commands

import settings


class General():
    """General commands."""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def shutdown(self, context):
        if context.message.author.id == settings.OWNER_ID:
            await self.bot.send_message(context.message.channel, "Shutting down.")
            await self.bot.logout()
        else:
            await self.bot.send_message(context.message.channel, "Don't tell me what to do.")


class Debugging():
    """Commands for debugging and testing."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Tells you your user ID.", pass_context=True)
    async def getid(self, context):
        user_id = context.message.author.id
        user_name = context.message.author.mention
        
        await self.bot.send_message(context.message.channel,
                                    "{}, your ID is {}".format(user_name, user_id))

