# -*- coding: utf-8 -*-
import configparser
import discord
from discord.ext.commands import Bot
from discord.ext import commands

BOT_PREFIX = "ashe-"
FILE_CONFIG = "config.ini"

client = commands.Bot(command_prefix=BOT_PREFIX)
config = configparser.SafeConfigParser()
config.read(FILE_CONFIG)

def main():
    token = config.get("info", "token")
    client.run(token)

if "__main__" == __name__:
    main()
