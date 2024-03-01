from logging import (
    DEBUG,
    ERROR,
    INFO,
    NOTSET,
    WARNING,
    Formatter,
    StreamHandler,
    getLogger,
)

FORMATTER = Formatter(
    """
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [ %(pathname)s:%(lineno)d ]
  %(message)s
    """.lstrip()
)

LOG_LEVEL_DEFAULT = "warning"
LOG_LEVELS = {
    "d": DEBUG,
    "debug": DEBUG,
    "e": ERROR,
    "error": ERROR,
    "i": INFO,
    "info": INFO,
    "w": WARNING,
    LOG_LEVEL_DEFAULT: WARNING,
}


def setup_logging(level_name):
    root_log = getLogger()
    root_log.setLevel(NOTSET)

    handler = StreamHandler(stream=None)
    level = LOG_LEVELS.get(level_name, WARNING)

    handler.setFormatter(FORMATTER)
    handler.setLevel(level)
    root_log.addHandler(handler)
