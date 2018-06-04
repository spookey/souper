from logging import getLogger

from requests import codes, request

LOG = getLogger(__name__)


def _raw_request(url):
    LOG.info('sending request to "%s"', url)
    response = request('get', url)

    if not response.ok:
        LOG.warning(
            'request to "%s" failed with "%s" - "%s"',
            response.url, response.status_code, response.reason
        )

    return response


def fetch_text(url):
    response = _raw_request(url)
    if response.status_code == codes.get('ok'):
        return response.text

    return None
