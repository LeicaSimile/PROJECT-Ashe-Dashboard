# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import logging
import logging.config


import projectashe
import settings

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("main")

def main():
    bot = commands.Bot(settings.BOT_PREFIX, description="For humanity!", pm_help=True)
    ashe = projectashe.ProjectAshe(bot, settings.FILE_DATABASE)
    ashe.run(settings.TOKEN)


if "__main__" == __name__:
    main()
