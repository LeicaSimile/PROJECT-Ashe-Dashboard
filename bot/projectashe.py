import discord
import logging
import logging.config

from commands import general
from commands import music
import settings
import phrases

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("bot")


class Bot(object):
    def __init__(self, client, db_file):
        self.client = client
        self.db = phrases.Database(db_file)

    def run(self, token):
        self.set_events()
        self.set_commands()
        self.client.run(token)

    def event_member_join(self):
        async def on_member_join(member):
            server = member.server
            await self.client.send_message(server, f"Salvation, bit by bit. Good to have you on our side, {member.mention}")

        return on_member_join

    def event_ready(self):
        async def on_ready():
            logger.info(f"{self.client.user.name} is now online.")
            logger.info(f"ID: {self.client.user.id}")
            logger.info(f"Command prefix: {settings.BOT_PREFIX}")

            await self.client.change_presence(game=discord.Game(name=f"DDR | {settings.BOT_PREFIX}help"))
            await self.client.say(self.db.random_line("phrase", "phrases", {"category_id": phrases.Category.ONLINE.value}))

        return on_ready

    def parse(self, text):
        """ Interprets a string and formats accordingly, substituting placeholders with values, etc.

        Args:
            text(unicode): String to parse.

        Returns:
            text(unicode): Parsed string.
        """
        return text
    
    def set_commands(self):
        self.client.add_cog(general.General(self))
        self.client.add_cog(general.Debugging(self))
        self.client.add_cog(music.Music(self))
        
    def set_events(self):
        self.client.event(self.event_ready())
        self.client.event(self.event_member_join())
