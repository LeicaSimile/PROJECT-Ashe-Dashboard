import discord
from discord.ext.commands.context import Context
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
            message = self.get_phrase(phrases.Category.WELCOME_SERVER.value)

            substitutions = {
                    settings.DISPLAY_NAME: member.display_name,
                    settings.MENTION: member.mention,
                    settings.SERVER_NAME: member.server.name,
                    settings.USER_NAME: member.name
                }
            message = self.parse(message, substitutions)
            await self.client.send_message(server, message)

        return on_member_join

    def event_ready(self):
        async def on_ready():
            logger.info(f"{self.client.user.name} is now online.")
            logger.info(f"ID: {self.client.user.id}")
            logger.info(f"Command prefix: {settings.BOT_PREFIX}")

            await self.client.change_presence(game=discord.Game(name=f"DDR | {settings.BOT_PREFIX}help"))

##            for server in self.client.servers:
##                message = self.get_phrase(phrases.Category.ONLINE.value)
##                message = self.parse(message, {settings.SERVER_NAME: server.name})
##                await self.client.send_message(server, message)

        return on_ready

    def get_phrase(self, category):
        """ Shortcut for getting a random phrase from the database.

        Args:
            category(unicode): The phrase category, as seen in the enum 'Category' in phrases.py.
        """
        return self.db.random_line("phrase", "phrases", {"category_id": category})

    def parse(self, text, context=None, substitutions=None):
        """ Interprets a string and formats accordingly, substituting placeholders with values, etc.

        Args:
            text(unicode): String to parse.
            context(Context, optional): Current context of the message.
            substitutions(dict, optional): Other substitutions to perform. Replaces key with corresponding value.

        Returns:
            text(unicode): Parsed string.
        """
        if not substitutions: substitutions = {}
        text = phrases.parse_all(text)

        ## Add context variables to substitutions.
        substitutions[settings.BOT_DISPLAY_NAME] = self.client.user.name
        substitutions[settings.BOT_NAME] = self.client.user.display_name
        
        try:
            ## Channel variables
            substitutions[settings.CHANNEL_NAME] = context.message.channel.name
        except AttributeError:
            substitutions[settings.CHANNEL_NAME] = ""
            
        try:
            ## User (author) variables
            substitutions[settings.DISPLAY_NAME] = context.message.author.display_name
            substitutions[settings.MENTION] = context.message.author.mention
            substitutions[settings.USER_NAME] = context.message.author.name
        except AttributeError:
            substitutions[settings.DISPLAY_NAME] = ""
            substitutions[settings.MENTION] = ""
            substitutions[settings.USER_NAME] = ""
            
        try:
            ## Server variables
            substitutions[settings.SERVER_NAME] = context.message.server.name
        except AttributeError:
            substitutions[settings.SERVER_NAME] = ""

        for s in substitutions:
            text = text.replace(s, substitutions[s])
            logger.debug(f"parse(): {text} (replaced '{s}' with '{subs[s]}')")
        
        return text
    
    def set_commands(self):
        self.client.add_cog(general.General(self))
        self.client.add_cog(general.Debugging(self))
        self.client.add_cog(music.Music(self))
        
    def set_events(self):
        self.client.event(self.event_ready())
        self.client.event(self.event_member_join())
