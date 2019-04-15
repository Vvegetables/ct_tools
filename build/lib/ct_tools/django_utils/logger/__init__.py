import logging

DATE_FORAMT = "%Y-%m-%d %H:%M:%S"
LOGGER_FORMAT = logging.Formatter(
    "%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s")

# logging.basicConfig(datefmt=DATE_FORAMT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_logger = logging.FileHandler("error.log")
file_logger.setLevel(logging.ERROR)
file_logger.setFormatter(LOGGER_FORMAT)
 
file_logger2 = logging.FileHandler("debug.log")
file_logger2.setLevel(logging.DEBUG)
file_logger2.setFormatter(LOGGER_FORMAT)

logger.addHandler(file_logger)
logger.addHandler(file_logger2)

if __name__ == "__main__":
    logger.warning("warning")
    logger.debug("debug")
    logger.info("info")
    logger.error("error")