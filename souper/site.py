from logging import getLogger
from string import Template

from souper.lib.disk import (
    base_loc,
    file_dump,
    file_load,
    join_loc,
    json_dump,
    sure_loc,
)


class Site:
    INDEX_TPL = base_loc("souper", "tpl", "index.tpl.html")
    LOGIC_TPL = base_loc("souper", "tpl", "logic.tpl.js")
    STYLE_TPL = base_loc("souper", "tpl", "style.tpl.css")

    def __init__(self, load, args):
        self._log = getLogger(self.__class__.__name__)
        self.load = load

        www = sure_loc(args.www, folder=True)
        self._index = join_loc(www, args.index)
        self._logic = join_loc(www, args.logic)
        self._store = join_loc(www, args.store)
        self._style = join_loc(www, args.style)

        self._vars = {
            "ASSET": args.asset,
            "DELAY": args.delay,
            "LOGIC": args.logic,
            "STORE": args.store,
            "STYLE": args.style,
            "TITLE": args.title,
        }

    def store(self):
        content = self.load()
        self._log.info("writing content to store file [%s]", self._store)
        return json_dump(self._store, content=sorted(content))

    def _produce(self, source, target):
        self._log.info("generating [%s] from [%s]", target, source)
        source = file_load(source)
        if not source:
            self._log.warning("empty template [%s]", source)
            return False

        try:
            result = Template(source).substitute(**self._vars)
        except (KeyError, ValueError) as ex:
            self._log.warning("template error [%s]", ex)
            return False

        return file_dump(target, content=result)

    def style(self):
        return self._produce(self.STYLE_TPL, self._style)

    def logic(self):
        return self._produce(self.LOGIC_TPL, self._logic)

    def index(self):
        return self._produce(self.INDEX_TPL, self._index)

    def __call__(self):
        self.store()
        self.style()
        self.logic()
        self.index()
