import asyncio
import datetime
import time
import re

import discord
from discord.ext import commands
import settings

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
MOD_ROLE_ID = 535886249458794547
GUILD_OWNER_ID = 533370022295502879

async def validate_access(context, user):
    """Checks if user has permission to use command."""
    return discord.utils.find(lambda r: r.id in [MOD_ROLE_ID, GUILD_OWNER_ID], user.roles)

class Admin(commands.Cog):
    """Commands usable only by the admin."""

    def __init__(self, bot):
        """
        Args:
            bot(Bot): Bot instance.
            
        """
        self.bot = bot

    async def get_inactive_members(self, context, progress_report=True):
        """Returns a list of inactive members."""
        senders = []
        now = datetime.datetime.now()
        channel_count = len(context.guild.text_channels)
        progress_msg = None

        if progress_report:
            progress_msg = await context.channel.send(f"Scanning {channel_count} channels for inactive members.")
        
        for i, channel in enumerate(context.guild.text_channels):
            try:
                async for m in channel.history(limit=None, after=(now - datetime.timedelta(days=14)), oldest_first=False):
                    if m.author not in senders:
                        senders.append(m.author)
            except discord.errors.Forbidden:
                print(f"Can't access {channel.name}")
            else:
                if progress_msg:
                    await progress_msg.edit(content=f"Scanned {i}/{channel_count} channels for inactive members.")
        
        if progress_msg:
            await progress_msg.edit(content=f"Scanned {channel_count} channels for inactive members.")

        return [u for u in context.guild.members if u not in senders]

    async def notify_members(self, context, members, message):
        for member in members:
            await member.send(
                content=message
            )
        
        messaged = "\n".join([f"{m.display_name} ({m.name}#{m.discriminator})" for m in members])
        await context.channel.send(f"Notified the following inactive members: ```{messaged}```")

    async def validate_owner(self, context, function_pass, function_fail=None):
        """Check if the owner issued the command.

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
        if str(context.author.id) == settings.OWNER_ID:
            await function_pass(context)
        else:
            try:
                await function_fail(context)
            except TypeError:
                response = "Don't tell me what to do."
                await self.bot.say(context.channel, response)
                
    @commands.command(description="Sends a list of inactive members in the server.")
    async def purgelist(self, context):
        def check(reaction, user):
            return reaction.message.id == report.id and user == context.message.author and str(reaction.emoji) == "📧"

        if not await validate_access(context, context.message.author):
            return

        inactive_members = await self.get_inactive_members(context)
        inactive_list = "\n".join([f"{u.display_name} ({u.name}#{u.discriminator})" for u in inactive_members])
        report = await context.channel.send(f"{context.author.mention} Inactive members (2+ weeks since last message): ```{inactive_list}```\nReact below to notify them.")
        await report.add_reaction("📧")

        try:
            reaction, user = await self.bot.client.wait_for("reaction_add", timeout=60, check=check)
        except asyncio.TimeoutError:
            await report.edit(content=f"Inactive members (2+ weeks since last message): ```{inactive_list}```")
            await report.clear_reactions()
        else:
            await context.channel.send(f"k")
    
    @commands.command(description="Notifies all purgelist members on their inactivity.")
    async def purgenotify(self, context):
        if not await validate_access(context, context.message.author):
            return

        mod_role = discord.utils.find(lambda r: r.id == MOD_ROLE_ID, context.guild.roles)
        to_notify = await self.get_inactive_members(context)
        message = f"Hello, we noticed you haven't been active for a while at ***{context.guild.name}***.\n\nWe have a policy of **kicking inactive members**, but if you're taking a break, that's alright. **Just let a moderator *({mod_role.name})* know** and we'll make sure to exempt you.\n\n(Do not reply here. This is an automated message and any replies will be ignored)"

        await self.notify_members(context, to_notify, message)

    @commands.command(description="Send a message through me.")
    async def message(self, context):
        async def get_destination(context):
            def check_destination(msg):
                return msg.author.id == context.message.author.id and msg.channel.id == context.channel.id and msg.channel_mentions

            await context.channel.send("Which channel should the message be sent to?")
            try:
                destination = await self.bot.client.wait_for("message", timeout=60, check=check_destination)
                return destination.content
            except asyncio.TimeoutError:
                return False

        async def get_message(context):
            def check_message(msg):
                return msg.author.id == context.message.author.id and msg.channel.id == context.channel.id

            await context.channel.send("What's your message?")
            try:
                message = await self.bot.client.wait_for("message", timeout=60, check=check_message)
                return message.content
            except asyncio.TimeoutError:
                return False

        if not await validate_access(context, context.message.author):
            return

        arguments = context.message.content.split(maxsplit=2)
        destination_id = None
        msg = ""

        try:
            destination_id = arguments[1]
        except IndexError:
            destination_id = await get_destination(context)
            if not destination_id:
                return

        try:
            destination_id = int(destination_id.strip("<># "))
        except ValueError:
            await context.channel.send("I couldn't find that channel on this server.")
            return

        destination = discord.utils.find(lambda c: c.id == destination_id, context.guild.text_channels)
        if not destination:
            await context.channel.send("I couldn't find that channel on this server.")

        try:
            msg = arguments[2]
        except IndexError:
            msg = await get_message(context)
            if not msg:
                return
        
        sent = await destination.send(msg)
        await context.channel.send(f"Message sent: {sent.jump_url}")

    @commands.command(description="Edit a message sent through me.")
    async def edit(self, context):
        if not await validate_access(context, context.message.author):
            return

        arguments = context.message.content.split()
        message_id = 0
        try:
            message_id = arguments[1]
        except IndexError:
            pass
        try:
            message_id = int(message_id)
        except ValueError:
            await context.channel.send(f"{message_id} is not a valid message ID.")
            return

        to_edit = await context.guild.me.fetch_message(message_id)
        if not to_edit:
            await context.channel.send(f"Couldn't find message with ID #{message_id}.")
        elif to_edit.author.id != context.guild.me.id:
            await context.channel.send("I can only edit messages I sent.")
        else:
            preview = discord.Embed(
                title="Message to Edit",
                url=to_edit.jump_url,
                description=to_edit.content,
                timestamp=to_edit.edited_at if to_edit.edited_at else to_edit.created_at
            )
            await context.channel.send(content="Enter the newly edited message below.", embed=preview)
            try:
                new_edit = await self.bot.client.wait_for("message", timeout=60, check=check)
            except asyncio.TimeoutError:
                await context.channel.send("Time's up.")
            else:
                try:
                    to_edit.edit(content=new_edit.content)
                except discord.Forbidden:
                    await context.channel.send("I'm not allowed to edit this message.")
                else:
                    await context.channel.send(f"Message edited: {to_edit.jump_url}")

    @commands.command(description="Shut me down :c")
    async def shutdown(self, context):
        async def log_out(context):
            try:
                response = ""
                await self.bot.say(context.channel, response, context)
            finally:
                await self.bot.client.logout()

        async def sass(context):
            response = "Don't tell me what to do."
            await self.bot.say(context.channel, response)

        await self.validate_owner(context, log_out, sass)

    @commands.Cog.listener()
    async def on_message(self, message):
        async def check_content(message, check, custom_message):
            if check:
                content = message.clean_content
                try:
                    await message.delete()
                except (discord.Forbidden, discord.HTTPException) as e:
                    print(f"Unable to delete message at {message.jump_url}. {e}")
                else:
                    await self.bot.say(message.author, f"{custom_message}\nYour message: ```{content}```")
                    return True

            return False

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
                    538110190902312976: f"To keep #lets-draw clean, only posts with pictures are allowed. Discuss art in #lets-draw-discussion!"
                },
                "no-pics": {
                    533377545865789441: f"To keep #general clean, posts with pictures are put in #memes-links-pics instead!",
                    535908960713310220: f"To keep #nsfw-chat clean, posts with pictures are put in #nsfw-memes-links-pics instead!"
                },
                "no-links": {
                    533377545865789441: f"To keep #general clean, posts with links are put in #memes-links-pics instead!",
                    535908960713310220: f"To keep #nsfw-chat clean, posts with links are put in #nsfw-memes-links-pics instead!"
                }
            }
        }
        if message.guild:
            print(f"[{datetime.datetime.now():%H:%M}]({message.guild.name} - {message.channel.name}) {user.name}: {message.content}")
        else:
            try:
                print(f"[{datetime.datetime.now():%H:%M}]({message.channel.name}) {user.name}: {message.content}")
            except AttributeError:
                print(f"[{datetime.datetime.now():%H:%M}]({user.name}) {message.content}")
            finally:
                return
        
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
        else:
            guild = message.guild
            channel = message.channel

            if guild.id in servers and channel.id in servers[guild.id]["pics-only"]:
                if await check_content(
                    message,
                    not message.attachments,
                    servers[guild.id]["pics-only"][channel.id]
                ):
                    return
            """
            if guild.id in servers and channel.id in servers[guild.id]["no-pics"]:
                if await check_content(
                    message,
                    message.attachments,
                    servers[guild.id]["no-pics"][channel.id]
                ):
                    return
            if guild.id in servers and channel.id in servers[guild.id]["no-links"]:
                if await check_content(
                    message,
                    re.search(URL_REGEX, message.clean_content),
                    servers[guild.id]["no-links"][channel.id]
                ):
                    return
            """
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild.id == 533368376148361216:
            before_roles = [r.id for r in before.roles]
            after_roles = [r.id for r in after.roles]
            if 533499454964105245 not in before_roles and 533499454964105245 in after_roles:
                # Say welcome message
                welcome_channel = discord.utils.get(after.guild.channels, name="general-chat")
                roles_channel = discord.utils.get(after.guild.channels, name="choose-roles")
                help_channel = discord.utils.get(after.guild.channels, name="help")
                moderator_role = discord.utils.get(after.guild.roles, id=535886249458794547)
                await self.bot.say(welcome_channel,
                    f"Welcome to the server, {after.mention}! Be sure to check out {roles_channel.mention} to find others with similar interests. If you have any questions, feel free to message a moderator ({moderator_role.name}) or post in {help_channel.mention}.")
            
        return
    