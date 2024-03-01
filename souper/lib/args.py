from argparse import ArgumentParser

from souper.base import APP_NAME
from souper.lib.note import LOG_LEVEL_DEFAULT, LOG_LEVELS


def arguments():

    def _help(txt):
        return f"{txt} (default: '%(default)s')"

    def _positive(num):
        num = int(num)
        if num >= 0:
            return num
        raise ValueError()

    parser = ArgumentParser(APP_NAME, epilog="c[_]")

    parser.add_argument(
        "-v",
        "--verbosity",
        choices=LOG_LEVELS.keys(),
        default=LOG_LEVEL_DEFAULT,
        help=_help("log level"),
    )

    parser.add_argument(
        "--title",
        default=APP_NAME,
        help=_help("index document title"),
    )
    parser.add_argument(
        "--delay",
        default=10000,
        type=_positive,
        help=_help("milliseconds delay between images"),
    )

    parser.add_argument(
        "src",
        help="source folder location",
    )
    parser.add_argument(
        "tgt",
        help="target folder location",
    )

    return parser.parse_args()
