import json
import os
import logging
from logging.handlers import RotatingFileHandler

from waitress import serve
from hiptsi import application

logger = logging.getLogger(__name__)

def main():
    logger.info("Runnning")
    serve(application, port=application.config["hiptsi"]["port"])

if __name__ == '__main__':
    main()
