from logging import Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from pprint import pformat

from souper import APP_NAME
from souper.lib import LOG_LEVELS
from souper.lib.disk import sure_loc


def _log_folder(folder_path, level_name):
    return sure_loc(folder_path, '{}_{}.log'.format(APP_NAME, level_name))


def _attach_handler(root, handler, formatter, level):
    handler.setFormatter(formatter)
    handler.setLevel(level)
    root.addHandler(handler)


def setup_logging(args):
    root_log = getLogger()
    formatter = Formatter('''
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [ %(pathname)s:%(lineno)d ]
  %(message)s
    '''.lstrip())

    level_name = args.verbosity.lower()
    level_dbg = LOG_LEVELS['debug']
    level_use = LOG_LEVELS.get(level_name, level_dbg)
    log_size = 10 * (1024 * 1024)

    root_log.setLevel(level_dbg)

    _attach_handler(
        root_log, StreamHandler(
            stream=None
        ), formatter, level_use
    )
    _attach_handler(
        root_log, RotatingFileHandler(
            _log_folder(args.log, level_name),
            maxBytes=log_size, backupCount=9,
        ), formatter, level_use
    )
    if level_use != level_dbg:
        _attach_handler(
            root_log, RotatingFileHandler(
                _log_folder(args.log, 'debug'),
                maxBytes=log_size, backupCount=4,
            ), formatter, level_dbg
        )


def keep_args(args):
    getLogger(__name__).debug('arguments:\n%s', pformat(vars(args)))
