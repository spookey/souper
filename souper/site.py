from logging import getLogger
from string import Template

from souper.base import (
    ASSET,
    ERROR_ASSETS,
    ERROR_BASICS,
    EXIT_SUCCESS,
    FICON,
    INDEX,
    LOGIC,
    STORE,
    STYLE,
)
from souper.lib.disk import (
    base_loc,
    copy_file,
    file_dump,
    file_load,
    join_loc,
    json_dump,
    sure_loc,
)


class Site:
    FICON_SRC = base_loc("souper", "tpl", "favicon.ico")
    INDEX_TPL = base_loc("souper", "tpl", "index.tpl.html")
    LOGIC_TPL = base_loc("souper", "tpl", "logic.tpl.js")
    STYLE_TPL = base_loc("souper", "tpl", "style.tpl.css")

    def __init__(self, load, args):
        self._log = getLogger(self.__class__.__name__)
        self.load = load

        self.tgt = sure_loc(args.tgt, folder=True)

        self._vars = {
            "ASSET": ASSET,
            "DELAY": args.delay,
            "FICON": FICON,
            "LOGIC": LOGIC,
            "STORE": STORE,
            "STYLE": STYLE,
            "TITLE": args.title,
        }

    def store(self):
        content = self.load()
        if not content:
            return False

        self._log.info("writing content to store [%s]", STORE)
        store = join_loc(self.tgt, STORE)
        return json_dump(store, content=sorted(content))

    def ficon(self):
        self._log.info("add favicon [%s]", FICON)
        icon = join_loc(self.tgt, FICON)
        return copy_file(self.FICON_SRC, icon)

    def _produce(self, source, name):
        self._log.info("generating [%s] from [%s]", name, source)
        source = file_load(source)
        if not source:
            self._log.warning("empty template [%s]", source)
            return False

        try:
            result = Template(source).substitute(**self._vars)
        except (KeyError, ValueError) as ex:
            self._log.warning("template error [%s]", ex)
            return False

        target = join_loc(self.tgt, name)
        return file_dump(target, content=result)

    def style(self):
        return self._produce(self.STYLE_TPL, STYLE)

    def logic(self):
        return self._produce(self.LOGIC_TPL, LOGIC)

    def index(self):
        return self._produce(self.INDEX_TPL, INDEX)

    def __call__(self):
        if not self.store():
            return ERROR_ASSETS
        if not self.ficon():
            return ERROR_ASSETS
        if not self.style():
            return ERROR_BASICS
        if not self.logic():
            return ERROR_BASICS
        if not self.index():
            return ERROR_BASICS

        return EXIT_SUCCESS
