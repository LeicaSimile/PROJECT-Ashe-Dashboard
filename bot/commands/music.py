import discord
from discord.ext import commands

import settings


class Music(object):
    """Music commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True, pass_context=True)
    async def fadein(self, context, seconds : int=2):
        pass

    @commands.command(no_pm=True, pass_context=True)
    async def fadeout(self, context, seconds : int=2):
        pass
    
    @commands.command(no_pm=True, pass_context=True)
    async def pause(self, context):
        pass
    
    @commands.command(no_pm=True, pass_context=True)
    async def play(self, context, link : str):
        pass

    @commands.command(no_pm=True, pass_context=True)
    async def skip(self, context):
        pass
    
    @commands.command(no_pm=True, pass_context=True)
    async def stop(self, context):
        pass

    @commands.command(no_pm=True, pass_context=True)
    async def volume(self, context, vol : int):
        pass
