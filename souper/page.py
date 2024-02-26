from logging import getLogger


class Page:
    def __init__(self):
        self._log = getLogger(self.__class__.__name__)

    @property
    def user_valid(self):
        return True

    def images(self):
        yield
        self._log.info("you've reached the end.")
