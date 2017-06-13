import discord
from discord.ext import commands

import settings
import phrases


class General():
    """General commands."""

    def __init__(self, bot):
        self.bot = bot
        self.db = phrases.Database(phrases.FILE_DATABASE)
        
    @commands.command(pass_context=True)
    async def shutdown(self, context):
        if context.message.author.id == settings.OWNER_ID:
            shutdown_msg = self.db.random_line("phrase", "phrases", {"category_id": phrases.Category.SHUTDOWN.value})
            await self.bot.send_message(context.message.channel, shutdown_msg)
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
                                    f"{user_name}, your ID is {user_id}")

