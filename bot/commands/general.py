import datetime
import time
import re

import discord
from discord.ext import commands
import settings

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

class Admin(commands.Cog):
    """Commands usable only by the admin."""

    def __init__(self, bot):
        """
        Args:
            bot(Bot): Bot instance.
            
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

        inactive_members = "\n".join([f"{u.display_name} ({u.name}#{u.discriminator})" for u in context.guild.members if u not in senders])
        await report.edit(content=f"Scanned {channel_count} channels for inactive members.")
        await context.channel.send(f"Inactive members (2+ weeks since last message): ```{inactive_members}```")
    
    @commands.command(description="Notifies all purgelist members on their inactivity.")
    async def purgenotify(self, context):
        mod_role = discord.utils.find(lambda r: r.id == 535886249458794547, context.guild.roles)
        to_notify = mod_role.members

        for member in to_notify:
            await member.send(
                content=f"Hello, we noticed you haven't been active for a while at {context.guild.name}. We have a policy of kicking inactive members, but if you're taking a break, that's alright. Just let a moderator ({mod_role.name}) know and we'll make sure to exempt you"
            )

        messaged = "\n".join([f"{u.display_name} ({u.name}#{u.discriminator})" for u in to_notify])
        await context.channel.send(f"Notified the following inactive members: ```{messaged}```")

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

    @commands.command(description="Have you tried turning it off and on?")
    async def restart(self, context):
        await self.bot.client.close()
        time.sleep(5)
        await self.bot.client.login()

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
        if str(context.author.id) == settings.OWNER_ID:
            await function_pass(context)
        else:
            try:
                await function_fail(context)
            except TypeError:
                response = "Don't tell me what to do."
                await self.bot.say(context.channel, response)
    