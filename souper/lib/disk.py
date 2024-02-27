from json import dumps
from logging import getLogger
from os import makedirs, path

ENCODING = "utf-8"

LOG = getLogger(__name__)


def join_loc(*locations):
    return path.realpath(
        path.expanduser(
            path.expandvars(
                path.join(
                    *(
                        (loc.lstrip(path.sep) if num != 0 else loc)
                        for num, loc in enumerate(locations)
                    )
                )
            )
        )
    )


def check_loc(*locations, folder=False):
    loc = join_loc(*locations)
    func = path.isdir if folder else path.isfile
    return path.exists(loc) and func(loc)


def sure_loc(*locations, folder=False):
    location = join_loc(*locations)
    loc = location if folder else path.dirname(location)
    if not check_loc(loc, folder=True):
        LOG.info('creating folder "%s"', loc)
        makedirs(loc)
    return location


def base_loc(*locations):
    return join_loc(
        path.dirname(path.dirname(path.dirname(__file__))), *locations
    )


def file_load(*locations, fallback):
    location = join_loc(*locations)
    if not check_loc(location, folder=False):
        LOG.info('file "%s" does not exist - return fallback', location)
        return fallback
    with open(location, "r", encoding=ENCODING) as handle:
        LOG.debug('reading from file "%s"', location)
        return handle.read()
    LOG.error('error reading file "%s" - return fallback', location)
    return fallback


def file_dump(*locations, content):
    location = sure_loc(*locations)
    with open(location, "w", encoding=ENCODING) as handle:
        LOG.debug('writing to file "%s"', location)
        return handle.write(content)
    LOG.error('error writing file "%s"', location)
    return None


def json_dump(*locations, content):
    return file_dump(
        *locations,
        content=dumps(
            content,
            indent=2,
            sort_keys=True,
        )
    )
