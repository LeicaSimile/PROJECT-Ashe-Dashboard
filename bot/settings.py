# -*- coding: utf-8 -*-
import configparser
import logging
import logging.config
import os.path

BOT_PREFIX = "ashe:"
FILE_CONFIG = os.path.join(os.path.dirname(__file__), "config.ini")
FILE_LOG = os.path.join(os.path.dirname(__file__), "logging.ini")

logging.config.fileConfig(FILE_LOG)
logger = logging.getLogger("phrases")
logger.debug(os.path.abspath(FILE_LOG))

config = configparser.SafeConfigParser()
config.read(FILE_CONFIG)


"""Settings from config file"""
BOT_ID = config.get("info", "id")
OWNER_ID = config.get("info", "owner-id")
SECRET = config.get("info", "secret")
TOKEN = config.get("info", "token")

"""Placeholders for variables in phrases"""
DISPLAY_NAME = "%display_name%"
MENTION = "%mention%"
SERVER_NAME = "%server%"
USER_NAME = "%name%"

"""Formatting symbols for parsing phrases"""
SENTINEL = "%SENTINEL%"  # Temporary substitute for replacements
ESCAPE_CHAR = "\\"

OPEN_CHOOSE = "<"  # Must be a single char
CLOSE_CHOOSE = ">"  # Must be a single char
SPLIT_CHOOSE = "|"

OPEN_OMIT = "{"  # single char
CLOSE_OMIT = "}"  #single char

OPEN_UPPER = r"\[upper]"
CLOSE_UPPER = r"\[/upper]"

OPEN_LOWER = r"\[lower]"
CLOSE_LOWER = r"\[/lower]"

OPEN_SENTENCE = r"\[sencase]"
CLOSE_SENTENCE = r"\[/sencase]"

OPEN_STARTCASE = r"\[startcase]"
CLOSE_STARTCASE = r"\[/startcase]"
