from logging import Formatter, StreamHandler, getLogger

from souper.base import LOG_LEVELS


def _attach_handler(root, handler, formatter, level):
    handler.setFormatter(formatter)
    handler.setLevel(level)
    root.addHandler(handler)


def setup_logging(args):
    root_log = getLogger()
    formatter = Formatter(
        """
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [ %(pathname)s:%(lineno)d ]
  %(message)s
    """.lstrip()
    )

    level_name = args.verbosity.lower()
    level_dbg = LOG_LEVELS["debug"]
    level_use = LOG_LEVELS.get(level_name, level_dbg)

    root_log.setLevel(level_dbg)

    _attach_handler(
        root_log,
        StreamHandler(stream=None),
        formatter,
        level_use,
    )
