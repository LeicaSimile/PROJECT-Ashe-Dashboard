# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

from bot.commands import general
import settings


bot = commands.Bot(command_prefix=settings.BOT_PREFIX, description=":D?", pm_help=True)




@bot.event
async def on_ready():
    print("{} is now online.".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Command prefix: {}".format(settings.BOT_PREFIX))
    
    await bot.change_presence(game=discord.Game(name="DDR | {}help".format(settings.BOT_PREFIX)))
    bot.add_cog(general.General(bot))


def main():
    bot.run(settings.TOKEN)


if "__main__" == __name__:
    main()
