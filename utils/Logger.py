import logging

class Logger():
    def __init__(self):
        logging.basicConfig(level="INFO", format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger()
        return logger