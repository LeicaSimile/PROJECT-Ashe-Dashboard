# -*- coding: utf-8 -*-
import logging
import re

import discord
import discordion

import commands
from discordion.settings import config


class Bot(discordion.Bot):
    """
    Args:
        client (discord.Bot): The bot instance.
        file_config (str): Filepath of config file with bot's settings.
        
    Attributes:
        db (BotDatabase): The bot's database.
        
    """
    
    def __init__(self, file_config, logger=None, **options):
        super().__init__(file_config, logger, **options)

    def event_ready(self):
        async def on_ready():
            prefix = config.get("bot", "prefix")
            self.logger.info(f"{self.client.user.name} is now online.")
            self.logger.info(f"ID: {self.client.user.id}")
            self.logger.info(f"Command prefix: {prefix}")

            status = config.get("bot", "status")
            await self.client.change_presence(activity=discord.Game(name=status))

        return on_ready
    
    def set_commands(self, *cmds):
        self.client.add_cog(commands.Admin(self))
        self.client.add_cog(commands.Fun(self))

        for c in cmds:
            self.client.add_cog(c)
        
    def set_events(self, *events):
        self.client.event(self.event_ready())

        for e in events:
            self.client.event(e)
            
