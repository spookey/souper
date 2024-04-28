from logging import Logger, getLogger
from string import Template
from typing import Collection, Final, Mapping, Optional, Union

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
from souper.lib.args import Args
from souper.lib.disk import (
    base_loc,
    copy_file,
    file_dump,
    file_load,
    join_loc,
    json_dump,
    sure_loc,
)
from souper.load import Load


class Site:
    FICON_SRC: Final[str] = base_loc("souper", "tpl", "favicon.ico")
    INDEX_TPL: Final[str] = base_loc("souper", "tpl", "index.tpl.html")
    LOGIC_TPL: Final[str] = base_loc("souper", "tpl", "logic.tpl.js")
    STYLE_TPL: Final[str] = base_loc("souper", "tpl", "style.tpl.css")

    def __init__(self, load: Load, args: Args):
        self._log: Final[Logger] = getLogger(self.__class__.__name__)
        self.load: Final[Load] = load

        self.tgt: Final[str] = sure_loc(args.tgt, folder=True)

        self._vars: Final[Mapping[str, Union[str, int]]] = {
            "ASSET": ASSET,
            "DELAY": args.delay,
            "FICON": FICON,
            "LOGIC": LOGIC,
            "STORE": STORE,
            "STYLE": STYLE,
            "TITLE": args.title,
        }

    def store(self) -> bool:
        content: Final[Optional[Collection[str]]] = self.load()
        if not content:
            return False

        self._log.info("writing content to store [%s]", STORE)
        store: Final[str] = join_loc(self.tgt, STORE)
        return json_dump(store, content=sorted(content))

    def ficon(self) -> bool:
        self._log.info("add favicon [%s]", FICON)
        icon: Final[str] = join_loc(self.tgt, FICON)
        return copy_file(self.FICON_SRC, icon)

    def _produce(self, source: str, name: str) -> bool:
        self._log.info("generating [%s] from [%s]", name, source)
        content: Final[Optional[str]] = file_load(source)
        if not content:
            self._log.warning("empty template [%s]", source)
            return False

        try:
            result: Final[str] = Template(content).substitute(**self._vars)
        except (KeyError, ValueError) as ex:
            self._log.warning("template error [%s]", ex)
            return False

        target: Final[str] = join_loc(self.tgt, name)
        return file_dump(target, content=result)

    def style(self) -> bool:
        return self._produce(self.STYLE_TPL, STYLE)

    def logic(self) -> bool:
        return self._produce(self.LOGIC_TPL, LOGIC)

    def index(self) -> bool:
        return self._produce(self.INDEX_TPL, INDEX)

    def __call__(self) -> int:
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
