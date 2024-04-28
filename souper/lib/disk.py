from json import dump
from logging import Logger, getLogger
from os import makedirs, path, unlink, walk
from shutil import copy
from typing import Callable, Final, Iterable, Optional, Tuple

ENCODING: Final[str] = "utf-8"

LOG: Final[Logger] = getLogger(__name__)


def join_loc(*locations: str) -> str:
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


def check_loc(*locations: str, folder: bool = False) -> bool:
    loc: Final[str] = join_loc(*locations)
    func: Final[Callable[[str], bool]] = path.isdir if folder else path.isfile
    return path.exists(loc) and func(loc)


def sure_loc(*locations: str, folder: bool = False) -> str:
    location: Final[str] = join_loc(*locations)
    loc: Final[str] = location if folder else path.dirname(location)
    if not check_loc(loc, folder=True):
        LOG.info("creating folder [%s]", loc)
        makedirs(loc)
    return location


def base_loc(*locations: str) -> str:
    return join_loc(
        path.dirname(path.dirname(path.dirname(__file__))), *locations
    )


def walk_tree(*locations: str) -> Iterable[Tuple[str, str]]:
    location: Final[str] = join_loc(*locations)
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


def copy_file(source: str, *locations: str) -> bool:
    if not check_loc(source, folder=False):
        LOG.error("source does not exist [%s]", source)
        return False
    location: Final[str] = join_loc(*locations)
    LOG.info("copy file [%s] to [%s]", source, location)
    copy(source, location)
    return True


def drop_file(*locations: str) -> bool:
    location: Final[str] = join_loc(*locations)
    if not check_loc(location, folder=False):
        LOG.warning("file [%s] does not exist", location)
        return False
    LOG.info("deleting file [%s] from disk", location)
    unlink(location)
    return True


def file_load(*locations: str) -> Optional[str]:
    location: Final[str] = join_loc(*locations)
    if not check_loc(location, folder=False):
        LOG.warning("file [%s] does not exist", location)
        return None
    with open(location, "r", encoding=ENCODING) as handle:
        LOG.debug("reading from file [%s]", location)
        try:
            return handle.read()
        except (TypeError, ValueError) as ex:
            LOG.exception(ex)
            LOG.error("error reading file [%s]", location)
    return None


def file_dump(*locations: str, content: str) -> bool:
    location: Final[str] = sure_loc(*locations)
    with open(location, "w", encoding=ENCODING) as handle:
        LOG.debug("writing to file [%s]", location)
        try:
            handle.write(content)
            return True
        except (TypeError, ValueError) as ex:
            LOG.exception(ex)
            LOG.error("error writing file [%s]", location)
    return False


def json_dump(*locations: str, content: object) -> bool:
    location: Final[str] = sure_loc(*locations)
    with open(location, "w", encoding=ENCODING) as handle:
        LOG.debug("writing to json file [%s]", location)
        try:
            dump(
                content,
                handle,
                indent=2,
                sort_keys=True,
            )
            return True
        except (TypeError, ValueError) as ex:
            LOG.exception(ex)
            LOG.error("error writing json file [%s]", location)
    return False
