from argparse import ArgumentParser
from typing import Final, NamedTuple, cast

from souper.base import APP_NAME
from souper.lib.note import LOG_LEVEL_DEFAULT, LOG_LEVELS


class Args(NamedTuple):
    verbosity: str
    title: str
    delay: int
    src: str
    tgt: str


def arguments() -> Args:

    def _help(txt: str) -> str:
        return f"{txt} (default: '%(default)s')"

    def _positive(num: str) -> int:
        val: Final[int] = int(num)
        if val >= 0:
            return val
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

    return cast(Args, parser.parse_args())
