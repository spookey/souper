from logging import getLogger

from souper.lib.disk import join_loc, sure_loc


class Load:  # pylint: disable=too-few-public-methods
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)

        self.src = join_loc(args.src)
        self._asset = sure_loc(args.tgt, args.asset, folder=True)

    def __call__(self):
        store = set()

        return store
