# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from bot.commands import general
import settings


bot = commands.Bot(command_prefix=settings.BOT_PREFIX, description=":D?", pm_help=True)


def add_commands():
    bot.add_cog(general.General(bot))
    bot.add_cog(general.Debugging(bot))

@bot.event
async def on_ready():
    print("{} is now online.".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Command prefix: {}".format(settings.BOT_PREFIX))

    add_commands()
    await bot.change_presence(game=discord.Game(name="DDR | {}help".format(settings.BOT_PREFIX)))
    

def main():
    bot.run(settings.TOKEN)


if "__main__" == __name__:
    main()
