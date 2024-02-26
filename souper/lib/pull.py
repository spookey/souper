from logging import getLogger
from os import fsync

from requests import codes, request

from souper.lib.disk import sure_loc

LOG = getLogger(__name__)


def _raw_request(url):
    LOG.info('sending request to "%s"', url)
    response = request("get", url, timeout=60)

    if not response.ok:
        LOG.warning(
            'request to "%s" failed with "%s" - "%s"',
            response.url,
            response.status_code,
            response.reason,
        )

    return response


def fetch_text(url):
    response = _raw_request(url)
    if response.status_code == codes.get("ok"):
        return response.text

    return None


def fetch_file(url, target, chunk_size=1024):
    location = sure_loc(target, folder=False)
    response = _raw_request(url)
    if response.status_code == codes.get("ok"):
        with open(location, "wb") as handle:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    handle.write(chunk)
                    handle.flush()
                    fsync(handle.fileno())
            return True

    LOG.error('error downloading file from "%s"', url)
    return False
