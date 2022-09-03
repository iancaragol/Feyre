import logging
import sys
from logging.handlers import RotatingFileHandler
from os import environ

class LoggerNames:
    """
    Common class containing logger names
    """
    backend_logger = "BACKEND_LOGGER"

    sync_logger = "SYNC_LOGGER"

    redis_logger = "REDIS_LOGGER"

    public_logger = "PUBLIC_LOGGER"

def logger_setup(logger_name : str, logger_file : str):
    """
    Creates a rotating logger with logger_name that writes to logger_file
    """
    logger = logging.getLogger(logger_name)

    env_type = environ.get("ENV")

    if (env_type.lower().startswith("dev")):
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    
    # add a rotating handler
    rotate = RotatingFileHandler(f"./logs/{logger_file}",
                                  maxBytes=20000)

    # add a handler to log to stdout
    stdout = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    rotate.setFormatter(formatter)
    stdout.setFormatter(formatter)

    logger.addHandler(rotate)
    logger.addHandler(stdout)