from logging import getLogger

from souper.base import APP_NAME
from souper.lib.args import arguments
from souper.lib.note import setup_logging
from souper.load import Load
from souper.site import Site

LOG = getLogger(__name__)


def main():
    args = arguments()
    setup_logging(args)
    LOG.info("%s ready", APP_NAME)

    load = Load(args)
    site = Site(load, args)

    site()
    LOG.info("%s done", APP_NAME)
    return 0
