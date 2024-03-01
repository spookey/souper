from json import dump
from logging import getLogger
from os import makedirs, path, unlink, walk
from shutil import copy

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
        LOG.info("creating folder [%s]", loc)
        makedirs(loc)
    return location


def base_loc(*locations):
    return join_loc(
        path.dirname(path.dirname(path.dirname(__file__))), *locations
    )


def walk_tree(*locations):
    location = join_loc(*locations)
    if not check_loc(location, folder=True):
        LOG.warning("invalid location [%s]", location)
        return
    LOG.info("walking location [%s]", location)
    for directory, _, files in walk(location):
        for file_name in files:
            yield (
                file_name,
                join_loc(directory, file_name),
            )


def copy_file(source, *locations):
    if not check_loc(source, folder=False):
        LOG.error("source does not exist [%s]", source)
        return False
    location = join_loc(*locations)
    LOG.info("copy file [%s] to [%s]", source, location)
    copy(source, location)
    return True


def drop_file(*locations):
    location = join_loc(*locations)
    if not check_loc(location, folder=False):
        LOG.warning("file [%s] does not exist", location)
        return False
    LOG.info("deleting file [%s] from disk", location)
    unlink(location)
    return True


def file_load(*locations):
    location = join_loc(*locations)
    if not check_loc(location, folder=False):
        LOG.warning("file [%s] does not exist", location)
        return None
    with open(location, "r", encoding=ENCODING) as handle:
        LOG.debug("reading from file [%s]", location)
        return handle.read()
    LOG.error("error reading file [%s]", location)
    return None


def file_dump(*locations, content):
    location = sure_loc(*locations)
    with open(location, "w", encoding=ENCODING) as handle:
        LOG.debug("writing to file [%s]", location)
        return handle.write(content)
    LOG.error("error writing file [%s]", location)
    return None


def json_dump(*locations, content):
    location = sure_loc(*locations)
    with open(location, "w", encoding=ENCODING) as handle:
        LOG.debug("writing to json file [%s]", location)
        dump(
            content,
            handle,
            indent=2,
            sort_keys=True,
        )
        return True
    LOG.error("error writing json file [%s]", location)
    return False
