import sys
import logging
from config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s: %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.handlers = [stream_handler]