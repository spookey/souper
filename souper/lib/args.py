from argparse import ArgumentParser

from souper.base import APP_NAME, LOG_LEVELS
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
        '--asset',
        default='asset',
        help=_help('asset folder in web root')
    )
    parser.add_argument(
        '--store',
        default='store.json',
        help=_help('store file name in web root')
    )
    parser.add_argument(
        '--index',
        default='index.html',
        help=_help('index file name in web root')
    )
    parser.add_argument(
        '--style',
        default='style.css',
        help=_help('style file name in web root')
    )
    parser.add_argument(
        '--jscript',
        default='logic.js',
        help=_help('logic file name in web root')
    )

    parser.add_argument(
        '--delay',
        default=10000,
        type=_positive,
        help=_help('milliseconds delay between images')
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
