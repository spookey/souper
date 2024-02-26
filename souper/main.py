from souper.lib.args import arguments
from souper.lib.note import setup_logging
from souper.load import Load
from souper.site import Site


def main():
    args = arguments()
    setup_logging(args.verbosity)

    load = Load(args)
    site = Site(load, args)

    site()
    return 0
