# -*- coding: utf-8 -*-
import configparser

BOT_PREFIX = "ashe:"
FILE_CONFIG = "config.ini"

"""Settings from config file"""
config = configparser.SafeConfigParser()
config.read(FILE_CONFIG)

OWNER_ID = config.get("info", "owner-id")
TOKEN = config.get("info", "token")
