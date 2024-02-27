from logging import getLogger

from souper.lib.disk import join_loc, json_dump, sure_loc


class Load:  # pylint: disable=too-few-public-methods
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)

        www = sure_loc(args.www, folder=True)
        self._asset = sure_loc(www, args.asset, folder=True)
        self._store = join_loc(www, args.store)

    def _save(self, store):
        self._log.debug('writing cache to store file "%s"', self._store)
        content = list(sorted(store))
        return json_dump(self._store, content=content)

    def download(self):
        store = set()

        self._save(store)
