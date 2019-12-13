# -*- coding: utf-8 -*-
import logging
import re
import discord
import commands
import settings
from imgurpython import ImgurClient

class Bot(object):
    """
    Args:
        client (discord.Bot): The bot instance.
        
    """
    
    def __init__(self, logger=None, **options):
        self.logger = logger or logging.getLogger(__name__)
        command_prefix = ";"
        description = settings.DESCRIPTION

        self.client = discord.ext.commands.Bot(command_prefix=command_prefix, description=description, **options)

    def run(self):
        self.set_events()
        self.set_commands()
        self.client.run(settings.CLIENT_TOKEN, reconnect=True)

    def event_ready(self):
        """Override on_ready"""
        async def on_ready():
            prefix = ";"
            self.logger.info(f"{self.client.user.name} is now online.")
            self.logger.info(f"ID: {self.client.user.id}")
            self.logger.info(f"Command prefix: {prefix}")

            status = f"DDR | {prefix}help for help"
            await self.client.change_presence(activity=discord.Game(name=status))

        return on_ready

    async def say(self, channel, message, context=None):
        await channel.send(content=message)
    
    def set_commands(self, *cmds):
        self.client.add_cog(commands.Admin(self))
        self.client.add_cog(commands.Fun(self))

        for c in cmds:
            self.client.add_cog(c)
        
    def set_events(self, *events):
        self.client.event(self.event_ready())

        for e in events:
            self.client.event(e)
