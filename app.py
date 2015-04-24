import os
import logging
from logging.handlers import RotatingFileHandler

from waitress import serve

from hiptsi import application

def main():
    logger = logging.getLogger("peewee")
    logger.setLevel(logging.WARNING)

    logger = logging.getLogger("waitress")
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(os.path.join(
        application.config["hiptsi"]["data_directory"], 'application.log'), maxBytes=30*1024*1024, backupCount=5)
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    serve(application, port=application.config["hiptsi"]["port"])

if __name__ == '__main__':
    main()
