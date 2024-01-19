import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


# Remove to reset logging level to something else
logger.remove(0)
logger.add(sys.stderr, level="INFO")
