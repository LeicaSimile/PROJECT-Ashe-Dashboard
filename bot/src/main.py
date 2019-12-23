# -*- coding: utf-8 -*-
import logging
from bot import Bot

logger = logging.getLogger("main")

def main():
    ashe = Bot()
    ashe.run()


if "__main__" == __name__:
    main()
