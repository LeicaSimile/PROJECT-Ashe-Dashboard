import discord
from discord.ext import commands
import logging
import logging.config

from commands import general
from commands import music
import settings
import phrases

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("bot")


class ProjectAshe(object):
    def __init__(self, bot):
        self.bot = bot

    def event_ready(self):
        async def on_ready():
            logger.info(f"{self.bot.user.name} is now online.")
            logger.info(f"ID: {self.bot.user.id}")
            logger.info(f"Command prefix: {settings.BOT_PREFIX}")

            await self.bot.change_presence(game=discord.Game(name=f"DDR | {settings.BOT_PREFIX}help"))

        return on_ready

    def event_member_join(self):
        async def on_member_join(member):
            server = member.server
            await self.bot.send_message(server, f"Salvation, bit by bit. Good to have you on our side, {member.mention}")

        return on_member_join
    
    def set_commands(self):
        self.bot.add_cog(general.General(self.bot))
        self.bot.add_cog(general.Debugging(self.bot))
        self.bot.add_cog(music.Music(self.bot))
        
    def set_events(self):
        self.bot.event(self.event_ready())
        self.bot.event(self.event_member_join())

    def run(self, token):
        self.set_events()
        self.set_commands()
        self.bot.run(token)
