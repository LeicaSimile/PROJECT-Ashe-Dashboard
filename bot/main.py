# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import logging
import logging.config


import projectashe
import settings

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("main")
bot = commands.Bot(command_prefix=settings.BOT_PREFIX, description="For humanity!", pm_help=None)

def main():
    ashe = projectashe.ProjectAshe(bot)
    ashe.run(settings.TOKEN)


if "__main__" == __name__:
    main()
