# -*- coding: utf-8 -*-
import logging

import discordion

from . import commands
from . import settings
from .settings import config


class Bot(discordion.Bot):
    """
    Args:
        client (discord.Bot): The bot instance.
        file_config (str): Filepath of config file with bot's settings.
        
    Attributes:
        db (BotDatabase): The bot's database.
        
    """
    
    def __init__(self, file_config, logger=None, formatter=None, pm_help=False, **options):
        super().__init__(file_config, logger, formatter, pm_help, **options)
        self.db_manual = sqlitehouse.Database(config.get("files", "database_manual"))
        self.db_auto = sqlitehouse.Database(config.get("files", "database_auto"))

    
    def event_member_join(self):
        async def on_member_join(member):
            server = member.server
            response = self.get_phrase(phrases.Category.GREET.value)
            ctx = GeneralContext(server=server, user=member)
            
            response = self.parse(response, context=ctx)
            await self.client.send_message(server, response)

        return on_member_join

    def event_ready(self):
        async def on_ready():
            prefix = config.get("bot", "prefix")
            self.logger.info(f"{self.client.user.name} is now online.")
            self.logger.info(f"ID: {self.client.user.id}")
            self.logger.info(f"Command prefix: {prefix}")

            status = config.get("bot", "status")
            await self.client.change_presence(game=discord.Game(name=status))

        return on_ready
    
    def set_commands(self, *cmds):
        self.client.add_cog(commands.General(self))
        self.client.add_cog(commands.Owner(self))
        
        for c in cmds:
            self.client.add_cog(c)
        
    def set_events(self, *events):
        self.client.event(self.event_ready())
        self.client.event(self.event_member_join())

        for e in events:
            self.client.event(e)
            