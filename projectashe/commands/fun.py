import datetime
import os

import discord
from discord.ext import commands
from wordcloud import WordCloud

import discordion
from discordion.settings import config

class Fun(commands.Cog):
    """Commands for fun."""

    def __init__(self, bot):
        """
        Args:
            bot(discordion.Bot): Bot instance.
            
        """
        self.bot = bot

    @commands.command(description="Summarizes a server, channel, or user's message history into a word cloud.", usage="[channel/username] (optional)")
    async def wordcloud(self, context):
        arguments = context.message.content.split()
        messages = []
        now = datetime.datetime.now()

        if len(arguments) < 2:
            channel_count = len(context.guild.text_channels)
            report = await context.channel.send(f"Scanning {channel_count} channels.")
            
            for i, channel in enumerate(context.guild.text_channels):
                try:
                    async for m in channel.history(limit=None, after=(now - datetime.timedelta(days=14)), oldest_first=False):
                        if m.author.bot:
                            continue
                        messages.append(m.clean_content)
                except discord.errors.Forbidden:
                    print(f"Can't access {channel.name}")
                else:
                    await report.edit(content=f"Scanned {i}/{channel_count} channels.")
            
            await report.delete()

            wc = WordCloud(width=800, height=400)
            wc.generate(" ".join(messages))

            wc_dir = f"wordcloud/{context.message.guild.id}"
            os.makedirs(wc_dir, exist_ok=True)

            wc_filename = f"/{now:%Y%m%d%H%M%S}.png"
            wc.to_file(wc_filename)
            await context.channel.send(f"A wordcloud for the server's past two weeks:", file=discord.File(wc_filename))
            return
        
        if context.message.mentions:
            pass
        if context.message.channel_mentions:
            channel = context.message.channel_mentions[0]
            try:
                async for m in channel.history(limit=None, after=(now - datetime.timedelta(days=14)), oldest_first=False):
                    if m.author.bot:
                        continue
                    messages.append(m.clean_content)
            except discord.errors.Forbidden:
                print(f"Can't access {channel.name}")
            else:
                wc = WordCloud(width=800, height=400)
                wc.generate(" ".join(messages))

                wc_dir = f"wordcloud/{context.message.guild.id}"
                os.makedirs(wc_dir, exist_ok=True)

                wc_filename = f"/{now:%Y%m%d%H%M%S}.png"
                wc.to_file(wc_filename)
                await context.channel.send(f"A wordcloud for #{channel}'s past two weeks:", file=discord.File(wc_filename))
