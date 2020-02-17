# -*- coding: utf-8 -*-
import logging
import logging.config
import yaml
from main.bot import Bot

with open("logging.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
logging.config.dictConfig(log_config)

def main():
    ashe = Bot(logger=logging.getLogger("bot"))
    ashe.run()


if "__main__" == __name__:
    main()
