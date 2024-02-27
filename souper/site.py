from logging import getLogger
from string import Template

from souper.base import APP_NAME
from souper.lib.disk import base_loc, file_dump, file_load, join_loc, sure_loc


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
        self._style = join_loc(www, args.style)

        self._vars = {
            "APP_NAME": APP_NAME,
            "ASSET": args.asset,
            "DELAY": args.delay,
            "LOGIC": args.logic,
            "STORE": args.store,
            "STYLE": args.style,
        }

    def _produce(self, source, target):
        self._log.info('generating "%s" from "%s"', target, source)
        tpl = Template(file_load(source, fallback=""))
        return file_dump(target, content=tpl.substitute(**self._vars))

    def style(self):
        return self._produce(self.STYLE_TPL, self._style)

    def logic(self):
        return self._produce(self.LOGIC_TPL, self._logic)

    def index(self):
        return self._produce(self.INDEX_TPL, self._index)

    def __call__(self):
        self.style()
        self.logic()
        self.index()
        self.load.download()
