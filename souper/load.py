from logging import getLogger

from souper.base import ASSET, EXTENSIONS
from souper.lib.disk import copy_file, drop_file, join_loc, sure_loc, walk_tree


class Load:
    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)

        self.src = join_loc(args.src)
        self._asset = sure_loc(args.tgt, ASSET, folder=True)

    def collect(self):
        result = set()
        self._log.info("collecting files from [%s]", self.src)
        for name, source in walk_tree(self.src):
            if not name.startswith(".") and any(
                name.lower().endswith(ext) for ext in EXTENSIONS
            ):
                if not copy_file(source, self._asset, name):
                    return None
                result.add(name)

        return result

    def cleanup(self, store):
        if not store:
            return None

        self._log.info("cleaning files in [%s]", ASSET)
        for name, target in walk_tree(self._asset):
            if name not in store:
                if not drop_file(target):
                    return None

        return store

    def __call__(self):
        store = self.collect()

        return self.cleanup(store)
