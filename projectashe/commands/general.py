import datetime
import time
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

    @commands.command(description="Sends a list of inactive members in the server.")
    async def purgelist(self, context):
        senders = []
        now = datetime.datetime.now()
        channel_count = len(context.guild.text_channels)
        report = await context.channel.send(f"Scanning {channel_count} channels for inactive members.")
        
        for i, channel in enumerate(context.guild.text_channels):
            try:
                async for m in channel.history(limit=None, after=(now - datetime.timedelta(days=14)), oldest_first=False):
                    if m.author not in senders:
                        senders.append(m.author)
            except discord.errors.Forbidden:
                print(f"Can't access {channel.name}")
            else:
                await report.edit(content=f"Scanned {i}/{channel_count} channels for inactive members.")

        inactive_members = "\n".join([f"{u.display_name}" for u in context.guild.members if u not in senders])
        await report.edit(content=f"Scanned {channel_count} channels for inactive members.")
        await context.channel.send(f"Inactive members (2+ weeks since last message): ```{inactive_members}```")
    
    @commands.command(description="Deletes all messages from non-members (excluding pinned messages).")
    async def purgemessages(self, context):
        def is_gone(m):
            return m.author not in m.guild.members

        channel_count = len(context.guild.text_channels)
        report = await context.channel.send(f"Scanning {channel_count} channels for messages from non-members.")

        for i, channel in enumerate(context.guild.text_channels):
            await report.edit(content=f"Purging #{channel.name}... ({i}/{channel_count} channels)")
            try:
                await channel.purge(limit=None, check=is_gone)
            except discord.errors.Forbidden:
                channel_count -= 1
                print(f"Can't access {channel.name}")
                continue
            except:
                await context.channel.send("Something went wrong. Cancelling the purge.")
                return

        await report.edit(content=f"Purged {channel_count}/{len(context.guild.text_channels)} channels.")

    @commands.command(description="Gives a role to a member.", usage="[user ID] [role name]")
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

    @commands.command(description="Removes a role from a member.", usage="[user ID] [role name]")
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

    @commands.command(description="Have you tried turning it off and on?")
    async def restart(self, context):
        await self.bot.client.close()
        time.sleep(5)
        await self.bot.client.login()

    @commands.command(description="Shut me down :c")
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

    @commands.command(description="Reread configuration settings")
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
        servers = {
            533368376148361216: {
                "pics-only": {
                    548737482108174337: f"To keep #selfies clean, only posts with pictures are allowed. Feel free to post comments in #general!",
                    538110190902312976: f"To keep #lets-deaw clean, only posts with pictures are allowed. Discuss art in #lets-draw-discussion!"
                },
                "no-pics": {
                    533377545865789441: f"To keep #general clean, posts with pictures are put in #memes-links-pics instead!",
                    535908960713310220: f"To keep #nsfw-chat clean, posts with pictures are put in #nsfw-memes-links-pics instead!"
                }
            }
        }
        print(f"[{datetime.datetime.now():%H:%M}]({message.guild.name} - {message.channel.name}) {user.name}: {message.content}")
        
        if user.id == 159985870458322944:  # MEE6 Bot
            result = re.compile(r"GG <@(?:.+)>, you just advanced to level ([0-9]+)!").match(message.content)
            if result:
                mentioned = message.mentions[0]
                level = int(result.group(1))
                print(f"{mentioned.name} reached level {level}")
                for r in roles:
                    if level >= r:
                        role = discord.utils.get(message.guild.roles, id=roles[r])
                        await mentioned.add_roles(role, reason=f"User reached level {r}")
        elif message.guild.id in servers and message.channel.id in servers[message.guild.id]["pics-only"]:
            if not message.attachments:
                content = message.clean_content
                channel = message.channel
                guild = message.guild
                try:
                    await message.delete()
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Unable to delete message at {message.jump_url}. {e}")
                else:
                    await self.bot.say(user, f"{servers[guild.id]['pics-only'][channel.id]}\nYour message: ```{content}```")
        elif message.guild.id in servers and message.channel.id in servers[message.guild.id]["no-pics"]:
            if message.attachments:
                content = message.clean_content
                channel = message.channel
                guild = message.guild
                try:
                    await message.delete()
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Unable to delete message at {message.jump_url}. {e}")
                else:
                    await self.bot.say(user, f"{servers[guild.id]['no-pics'][channel.id]}\nYour message: ```{content}```")

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
    
