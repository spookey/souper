from logging import getLogger

from souper.lib.disk import sure_loc


class Load:  # pylint: disable=too-few-public-methods
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)

        www = sure_loc(args.www, folder=True)
        self._asset = sure_loc(www, args.asset, folder=True)

    def __call__(self):
        store = set()

        return store
