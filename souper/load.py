from collections import namedtuple
from datetime import datetime, timezone
from logging import getLogger

from souper.lib.disk import (
    join_loc,
    json_dump,
    json_load,
    list_loc,
    rm_loc,
    sure_loc,
)
from souper.lib.pull import fetch_file


class Load(object):
    KEY = namedtuple("Key", ("t", "f", "h"))("time", "file", "href")

    def __init__(self, page, args):
        self._log = getLogger(self.__class__.__name__)
        self.now = datetime.now(timezone.utc)
        self.page = page

        www = sure_loc(args.www, folder=True)
        self._asset = sure_loc(www, args.asset, folder=True)
        self._store = join_loc(www, args.store)

        self.cache = json_load(self._store, fallback=[])

    def _save(self):
        self._log.debug('writing cache to store file "%s"', self._store)
        content = list(
            sorted(
                self.cache,
                key=lambda el: (
                    el.get(self.KEY.t),
                    el.get(self.KEY.f),
                ),
            )
        )
        return json_dump(self._store, content=content)

    def _exists(self, name):
        for elem in self.cache:
            if elem.get(self.KEY.f) == name:
                return True
        self._log.debug('image "%s" not present in cache', name)
        return False

    def _remove(self, name):
        if self._exists(name):
            self._log.info('removing image "%s" from cache')
            self.cache = [
                item for item in self.cache if item.get(self.KEY.f) != name
            ]

    def _attach(self, name, href):
        if not self._exists(name):
            if fetch_file(href, join_loc(self._asset, name)):
                self._log.info('adding image "%s"', name)
                self.cache.append(
                    {
                        self.KEY.t: self.now.isoformat(),
                        self.KEY.f: name,
                        self.KEY.h: href,
                    }
                )
                self._save()

    def cleanup(self):
        self._log.info('cleanup "%s" folder and cache', self._asset)
        physical = list_loc(self._asset)
        for name in (elem.get(self.KEY.f) for elem in self.cache):
            if name not in physical:
                self._remove(name)
        for name in physical:
            if not self._exists(name):
                rm_loc(self._asset, name)

    def download(self):
        self.cleanup()
        for base, name in self.page.images():
            self._attach(name, "/".join([base, name]))
        self.cleanup()
