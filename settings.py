# -*- coding: utf-8 -*-
import configparser

BOT_PREFIX = "ashe:"
FILE_CONFIG = "config.ini"

"""Settings from config file"""
config = configparser.SafeConfigParser()
config.read(FILE_CONFIG)

OWNER_ID = config.get("info", "owner-id")
TOKEN = config.get("info", "token")

"""Placeholders for variables in phrases"""
DISPLAY_NAME = "%display_name%"
MENTION = "%mention%"
SERVER_NAME = "%server%"
USER_NAME = "%name%"

