# -*- coding: utf-8 -*-
from discord.ext.commands import context

import settings


class GeneralContext(context.Context):
    """Expanded version of the Discord Context class.

    This class can be used outside of command functions, such as
    inside event handlers. It needs to be created manually.

    Attributes:
        channel(discord.Channel):
        server(discord.Server):
        user(discord.Member/User):
    """

    def __init__(self, **attrs):
        attrs["prefix"] = settings.BOT_PREFIX
        super().__init__(**attrs)
        self.channel = attrs.pop("channel", None)
        self.server = attrs.pop("server", None)
        self.user = attrs.pop("user", None)

        self._extract_message()

    def _extract_message(self):
        """Assigns some of the message variables to this class's variables."""
        if self.message:
            self.channel = self.message.channel if not self.channel else self.channel
            self.server = self.message.server if not self.server else self.server
            self.user = self.message.author if not self.user else self.user
