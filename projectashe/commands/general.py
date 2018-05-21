import discord
from discord.ext import commands

import discordion
from discordion.settings import config


class General(object):
    """General commands."""

    def __init__(self, bot):
        """
        Args:
            bot(discordion.Bot): Bot instance.
            
        """
        self.bot = bot

    @commands.command(description="Tells you your user ID.", pass_context=True)
    async def getid(self, context):
        user_id = context.message.author.id
        user_name = context.message.author.mention
        
        await self.bot.client.send_message(context.message.channel,
                                           f"{user_name}, your ID is {user_id}")


class Owner(object):
    """Commands usable only by the owner."""

    def __init__(self, bot):
        """
        Args:
            bot(discordion.Bot): Bot instance.
            
        """
        self.bot = bot

    @commands.command(pass_context=True)
    async def shutdown(self, context):
        context = discordion.GeneralContext(context=context)
        if context.user.id == config.get("bot", "owner_id"):
            try:
                response = self.bot.get_phrase("")
                
                await self.bot.say(context.channel, response, context)
            finally:
                await self.bot.client.logout()
        else:
            response = "Don't tell me what to do."
            await self.bot.say(context.channel, response)

    @commands.command(pass_context=True)
    async def changegame(self, context):
        async def change_status(context):
            status = context.argument
            g = discord.Game(name=status)
            await self.bot.client.change_presence(game=g)

        await self.validate_owner(context, change_status)

    @commands.command(pass_context=True)
    async def reconfig(self, context):
        async def read_config(context):
            discordion.settings.read_settings(self.bot.file_config)
            await self.bot.say(context.channel, "Settings updated.")

        await self.validate_owner(context, read_config)

    async def validate_owner(self, context, function_pass, function_fail=None):
        """ Check if the owner issued the command.

        Args:
            context (discord.Context): Context of the command.
            function_pass (func): Function to call if check passes.
                Must be a coroutine that accepts a GeneralContext object
                as an argument.
            function_fail (func, optional): Function to call if check fails.
                Must be a coroutine that accepts a GeneralContext object
                as an argument. If none provided, bot will give a stock
                warning to the user.

        """
        context = discordion.GeneralContext(context=context)
        if context.user.id == config.get("bot", "owner_id"):
            await function_pass(context)
        else:
            try:
                await function_fail(context)
            except TypeError:
                response = "Don't tell me what to do."
                await self.bot.say(context.channel, response)
    
