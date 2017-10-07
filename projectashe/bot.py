# -*- coding: utf-8 -*-
import logging
import logging.config

import discord
from discord.ext import commands
import discordion

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("main")

def main():
    FILE_CONFIG = "settings.ini"
    description = "For humanity!"
    bot = commands.Bot(settings.BOT_PREFIX, description=description, pm_help=True)
    ashe = discordion.Bot(bot, FILE_CONFIG)
    ashe.run()


if "__main__" == __name__:
    main()
