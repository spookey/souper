from logging import getLogger

from souper import APP_NAME
from souper.lib.args import arguments
from souper.lib.note import keep_args, setup_logging

LOG = getLogger(__name__)


def main():
    args = arguments()
    setup_logging(args)
    keep_args(args)

    LOG.info('%s ready', APP_NAME)
    return 0
