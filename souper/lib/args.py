from argparse import ArgumentParser

from souper import APP_NAME
from souper.lib import LOG_LEVELS
from souper.lib.disk import base_loc


def arguments():

    def _help(txt):
        return '{} (default: "%(default)s")'.format(txt)

    def _positive(num):
        num = int(num)
        if num > 0:
            return num
        raise ValueError()

    parser = ArgumentParser(
        APP_NAME,
        epilog='c[_]'
    )

    parser.add_argument(
        '-v', '--verbosity',
        choices=LOG_LEVELS.keys(),
        default='warning',
        help=_help('log level')
    )
    parser.add_argument(
        '-l', '--log',
        default=base_loc('logs'),
        help=_help('log files folder')
    )

    parser.add_argument(
        '-w', '--www',
        default=base_loc('www'),
        help=_help('web root output path')
    )
    parser.add_argument(
        '-i', '--index',
        default='index.html',
        help=_help('index file name')
    )
    parser.add_argument(
        '-j', '--js',
        default='logic.js',
        help=_help('logic file name')
    )
    parser.add_argument(
        '-s', '--store',
        default='store.json',
        help=_help('store file name')
    )

    parser.add_argument(
        '-p', '--pages',
        type=_positive,
        default=0,
        help=_help('crawl only a number pages [0 is no limit]')
    )

    parser.add_argument(
        'username',
        help='soup user name'
    )

    return parser.parse_args()
