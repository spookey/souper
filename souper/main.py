from logging import getLogger

from souper.base import APP_NAME
from souper.lib.args import arguments
from souper.lib.note import keep_args, setup_logging
from souper.load import Load
from souper.page import Page

LOG = getLogger(__name__)


def main():
    args = arguments()
    setup_logging(args)
    keep_args(args)
    LOG.info('%s ready', APP_NAME)

    page = Page(args)
    if not page.user_valid:
        return 1

    load = Load(page, args)
    # load.download()

    LOG.info('%s done', APP_NAME)
    return 0
