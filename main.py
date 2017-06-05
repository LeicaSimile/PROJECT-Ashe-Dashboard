# -*- coding: utf-8 -*-
import configparser
import discord
from discord.ext import commands

from bot.commands import general

BOT_PREFIX = "ashe:"
FILE_CONFIG = "config.ini"

bot = commands.Bot(command_prefix=BOT_PREFIX, description=":D?", pm_help=True)
config = configparser.SafeConfigParser()
config.read(FILE_CONFIG)

TOKEN = config.get("info", "token")

@bot.event
async def on_ready():
    print("{} is now online.".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Command prefix: {}".format(BOT_PREFIX))
    
    await bot.change_presence(game=discord.Game(name="DDR | {}help".format(BOT_PREFIX)))
    bot.add_cog(general.General(bot))


def main():
    bot.run(TOKEN)


if "__main__" == __name__:
    main()
