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
        "--asset",
        default="asset",
        help=_help("asset folder in web root"),
    )
    parser.add_argument(
        "--store",
        default="store.json",
        help=_help("store file name in web root"),
    )
    parser.add_argument(
        "--index",
        default="index.html",
        help=_help("index file name in web root"),
    )
    parser.add_argument(
        "--style",
        default="style.css",
        help=_help("style file name in web root"),
    )
    parser.add_argument(
        "--logic",
        default="logic.js",
        help=_help("logic file name in web root"),
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
