from logging import (
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    Formatter,
    Handler,
    Logger,
    StreamHandler,
    getLogger,
)
from typing import Final, Mapping

FORMATTER: Final[Formatter] = Formatter(
    """
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [ %(pathname)s:%(lineno)d ]
  %(message)s
    """.lstrip()
)

LOG_LEVEL_DEFAULT: Final[str] = "warning"
LOG_LEVELS: Final[Mapping[str, int]] = {
    "d": DEBUG,
    "debug": DEBUG,
    "e": ERROR,
    "error": ERROR,
    "i": INFO,
    "info": INFO,
    "w": WARNING,
    LOG_LEVEL_DEFAULT: WARNING,
}


def setup_logging(level_name: str) -> None:
    root_log: Final[Logger] = getLogger()
    root_log.setLevel(NOTSET)

    handler: Final[Handler] = StreamHandler(stream=None)
    level = LOG_LEVELS.get(level_name, WARNING)

    handler.setFormatter(FORMATTER)
    handler.setLevel(level)
    root_log.addHandler(handler)
