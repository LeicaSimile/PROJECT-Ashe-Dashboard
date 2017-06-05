import discord
from discord.ext import commands


class General():
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Tells you your user ID.", pass_context=True)
    async def get_id(self, context):
        user_id = context.message.author.id
        user_name = context.message.author.name
        await self.bot.send_message(context.message.channel,
                                    "{}, your ID is {}".format(user_name, user_id))
        
    @commands.command(description="D:", pass_context=True)
    async def shutdown(self, context):
        await self.bot.send_message(context.message.channel, "Shutting down.")
        await self.bot.logout()
