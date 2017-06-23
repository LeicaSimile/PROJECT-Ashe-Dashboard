import discord
import logging
import logging.config

from commands import general
from commands import music
from context import GeneralContext
import settings
import phrases

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("bot")


class Bot(object):
    """
    Attributes:
        client(discord.Bot): The bot instance.
        db_file(str): File path of the bot's database. Used to create 'db', a Database instance.
    """
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
            ctx = GeneralContext(server=server, user=member)
            
            message = self.parse(message, context=ctx)
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
            context(GeneralContext, optional): Current context of the message.
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
            substitutions[settings.CHANNEL_NAME] = context.channel.name
        except AttributeError:
            substitutions[settings.CHANNEL_NAME] = ""
            
        try:
            ## User (author) variables
            substitutions[settings.DISPLAY_NAME] = context.user.display_name
            substitutions[settings.MENTION] = context.user.mention
            substitutions[settings.USER_NAME] = context.user.name
        except AttributeError:
            substitutions[settings.DISPLAY_NAME] = ""
            substitutions[settings.MENTION] = ""
            substitutions[settings.USER_NAME] = ""
            
        try:
            ## Server variables
            substitutions[settings.SERVER_NAME] = context.server.name
        except AttributeError:
            substitutions[settings.SERVER_NAME] = ""

        for s in substitutions:
            text = text.replace(s, substitutions[s])
            logger.debug(f"parse(): {text} (replaced '{s}' with '{substitutions[s]}')")
        
        return text
    
    def set_commands(self):
        self.client.add_cog(general.General(self))
        self.client.add_cog(general.Debugging(self))
        self.client.add_cog(music.Music(self))
        
    def set_events(self):
        self.client.event(self.event_ready())
        self.client.event(self.event_member_join())
