from typing import Final

from souper.lib.args import Args, arguments
from souper.lib.note import setup_logging
from souper.load import Load
from souper.site import Site


def main() -> int:
    args: Final[Args] = arguments()
    setup_logging(args.verbosity)

    load: Final[Load] = Load(args)
    site: Final[Site] = Site(load, args)

    return site()
