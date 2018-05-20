# -*- coding: utf-8 -*-
import logging
import logging.config

import discordion

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("main")

def main():
    FILE_CONFIG = "settings.ini"
    ashe = discordion.Bot(FILE_CONFIG)
    ashe.run()


if "__main__" == __name__:
    main()
