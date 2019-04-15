import logging
import sys

DATE_FORAMT = "%Y-%m-%d %H:%M:%S"
LOGGER_FORMAT = logging.Formatter(
    "%(asctime)s - %(filename)s[line: %(lineno)d] - %(levelname)s: %(message)s")

logging.basicConfig(datefmt=DATE_FORAMT)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler(sys.stdout)
console_logger.setFormatter(LOGGER_FORMAT)
console_logger.setLevel(logging.ERROR)

file_logger = logging.FileHandler("error.log")
file_logger.setFormatter(LOGGER_FORMAT)
file_logger.setLevel(logging.ERROR)

file_logger2 = logging.FileHandler("debug.log")
file_logger2.setFormatter(LOGGER_FORMAT)
file_logger2.setLevel(logging.DEBUG)

logger.addHandler(console_logger)
logger.addHandler(file_logger)
logger.addHandler(file_logger2)

if __name__ == "__main__":
    logger.warning("warning")
    logger.debug("debug")
    logger.info("info")
    logger.error("error")