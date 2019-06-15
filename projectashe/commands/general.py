import datetime
import re
import discord
from discord.ext import commands

import discordion
from discordion.settings import config


class Admin(commands.Cog):
    """Commands usable only by the admin."""

    def __init__(self, bot):
        """
        Args:
            bot(discordion.Bot): Bot instance.
            
        """
        self.bot = bot

    @commands.command()
    async def addrole(self, context):
        async def give_role(context):
            msg_parts = context.message.content.split(" ", 2)
            try:
                user = discord.utils.get(context.guild.members, id=int(msg_parts[1]))
                role = discord.utils.get(context.guild.roles, name=msg_parts[2])
                await user.add_roles(role, reason="My owner told me to.")
            except IndexError:
                await self.bot.say(context.channel, "Say: ;addrole [user ID] [role name]")
            except AttributeError:
                await self.bot.say(context.channel, f"Couldn't find user ID {msg_parts[1]}.")
            else:
                await context.message.add_reaction(u"\U0001F44D")
                
        await self.validate_owner(context, give_role)

    @commands.command()
    async def removerole(self, context):
        async def remove_role(context):
            msg_parts = context.message.content.split(" ", 2)
            try:
                user = discord.utils.get(context.guild.members, id=int(msg_parts[1]))
                role = discord.utils.get(context.guild.roles, name=msg_parts[2])
                await user.remove_roles(role, reason="My owner told me to.")
            except IndexError:
                await self.bot.say(context.channel, "Say: ;removerole [user ID] [role name]")
            except AttributeError:
                await self.bot.say(context.channel, f"Couldn't find user ID {msg_parts[1]}.")
            else:
                await context.message.add_reaction(u"\U0001F44D")
                
        await self.validate_owner(context, remove_role)

    @commands.command()
    async def shutdown(self, context):
        async def log_out(context):
            try:
                response = self.bot.get_phrase(database.Category.SHUTDOWN.value)
                await self.bot.say(context.channel, response, context)
            finally:
                await self.bot.client.logout()

        async def sass(context):
            response = "Don't tell me what to do."
            await self.bot.say(context.channel, response)

        await self.validate_owner(context, log_out, sass)

    @commands.command()
    async def reconfig(self, context):
        async def read_config(context):
            discordion.settings.read_settings(self.bot.file_config)
            await self.bot.say(context.channel, "Settings updated.")

        await self.validate_owner(context, read_config)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        roles = {
            5: 533369804334039061,
            10: 533369803965071381,
            20: 533369912207474706,
            30: 533369949591175169,
            50: 573702137918390272
        }
        print(f"[{datetime.datetime.now():%H:%M}]({message.guild.name} - {message.channel.name}) {user.name}: {message.content}")
        
        if user.id == 159985870458322944:  # MEE6 Bot
            result = re.compile(r"GG <@(?:.+)>, you just advanced to level ([0-9]+)!").match(message.content)
            if result:
                mentioned = message.mentions[0]
                level = int(result.group(1))
                print("{mentioned.name} reached level {level}")
                for r in roles:
                    if level >= r:    
                        role = discord.utils.get(message.guild.roles, id=roles[r])
                        await mentioned.add_roles(role, reason=f"User reached level {r}")

    async def validate_owner(self, context, function_pass, function_fail=None):
        """ Check if the owner issued the command.

        Args:
            context (discord.Context): Context of the command.
            function_pass (func): Function to call if check passes.
                Must be a coroutine that accepts a GeneralContext object
                as an argument.
            function_fail (func, optional): Function to call if check fails.
                Must be a coroutine that accepts a GeneralContext object
                as an argument. If none provided, bot will give a stock
                warning to the user.

        """
        if str(context.author.id) == config.get("bot", "owner_id"):
            await function_pass(context)
        else:
            try:
                await function_fail(context)
            except TypeError:
                response = "Don't tell me what to do."
                await self.bot.say(context.channel, response)
    
