import datetime
import io
import os
import discord
from discord.ext import commands
from wordcloud import WordCloud
from matplotlib.image import imread
from status import CommandStatus

class Fun(commands.Cog):
    """Commands for fun."""

    def __init__(self, bot):
        """
        Args:
            bot(Bot): Bot instance.
            
        """
        self.bot = bot

    @commands.command(description="Summarizes a server, channel, or user's message history into a word cloud.", usage="[channel/username] (optional)")
    async def wordcloud(self, context):
        arguments = context.message.content.split()
        messages = []
        channels = context.guild.text_channels
        now = datetime.datetime.now()
        days = 14
        user = None
        subject = context.guild.name

        if context.message.mentions:
            user = context.message.mentions[0]
            subject = user.display_name
        if context.message.channel_mentions:
            channels = [context.message.channel_mentions[0]]
            subject = f"#{channels[0].name}"

        report = await context.channel.send(f"Scanning {subject}'s past {days} days...")

        for channel in channels:
            try:
                async for m in channel.history(limit=None, after=(now - datetime.timedelta(days=days)), oldest_first=False):
                    if user:
                        if m.author == user:
                            messages.append(m.clean_content)
                        continue
                    if m.author.bot:
                        continue
                    messages.append(m.clean_content)
            except discord.errors.Forbidden:
                print(f"Can't access {channel.name}")
        
        if "picture provided" == "":
            img_mask = imread("wordcloud/mask.png")
            wc = WordCloud(background_color=None, mask=img_mask, contour_width=2, contour_color="white")
        else:
            wc = WordCloud(width=1000, height=400)

        wc.generate(" ".join(messages))
        
        wc_dir = f"wordcloud/{context.message.guild.id}"
        os.makedirs(wc_dir, exist_ok=True)

        wc_filename = f"{now:%Y%m%d%H%M%S}.png"
        wc_filepath = os.path.join(wc_dir, wc_filename)
        wc.to_file(wc_filepath)

        await report.delete()
        await context.channel.send(f"A wordcloud for {subject}'s past {days} days:", file=discord.File(wc_filepath))
        return CommandStatus.COMPLETED
