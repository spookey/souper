from logging import getLogger
from re import compile as re_compile

from bs4 import BeautifulSoup

from souper.lib.pull import fetch_text


class Page(object):
    ASSET_RX = r'(http://asset-.\.soupcdn\.com/asset/\d{3,5})/'
    IMAGE_RX = r'(.{4}_.{4})(_.{3,4})?\.(jpeg|jpg|gif|png)'
    SINCE_RX = r'SOUP\.Endless\.next_url.+/(since/\d*)'

    def __init__(self, args):
        self._log = getLogger(self.__class__.__name__)
        self.username = args.username
        self.pages = args.pages
        self._loop = 0

    def _soup(self, since):
        purl = 'http://{user}.soup.io/{since}'.format(
            user=self.username, since=since
        )
        text = fetch_text(purl)
        if text:
            return BeautifulSoup(text, 'html.parser')
        self._log.warning(
            'no page for user "%s" since "%s"', self.username, since
        )
        return None

    @property
    def user_valid(self):
        self._log.debug('validating username "%s"', self.username)
        soup = self._soup(since='')
        if soup and not soup.find('form.user_create'):
            return True

        self._log.error('user "%s" does not exist', self.username)
        return False

    def _since(self, soup):
        self._log.info('searching for next page of "%s"', self.username)
        pattern = re_compile(self.SINCE_RX)
        script = soup.find('script', text=pattern)
        if script:
            return pattern.search(script.text).group(1)
        return None

    def _images(self, soup):
        self._log.info('searching for images of "%s"', self.username)
        pattern = re_compile(self.ASSET_RX + self.IMAGE_RX)
        for elem in soup.find_all('img', src=pattern):
            search = pattern.search(elem['src'])
            yield search.group(1), '.'.join(search.group(2, 4))

    def images(self):
        since = ''

        while since is not None:
            self._loop += 1
            self._log.info('crawling page "#%s"', self._loop)

            soup = self._soup(since=since)
            if not soup:
                self._log.warning(
                    'no page for "%s" since "%s"', self.username, since
                )
                break

            yield from self._images(soup)

            since = self._since(soup)
            if self.pages:
                if self._loop >= self.pages:
                    since = None

        self._log.info('you\'ve reached the end.')
