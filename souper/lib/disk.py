from logging import getLogger
from os import makedirs, path

LOG = getLogger(__name__)


def join_loc(*locations):
    return path.realpath(path.expanduser(path.expandvars(path.join(*(
        (loc.lstrip(path.sep) if num != 0 else loc)
        for num, loc in enumerate(locations)
    )))))


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
