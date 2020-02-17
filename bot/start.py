# -*- coding: utf-8 -*-
import logging
from main.bot import Bot

logger = logging.getLogger("main")

def main():
    ashe = Bot(logger=logging.getLogger("bot"))
    ashe.run()


if "__main__" == __name__:
    main()
