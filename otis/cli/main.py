import argparse

from otis import __version__
from otis.cli.run import Run


def main():
    parser = argparse.ArgumentParser(
        description='Otis elevator.')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='{0} version : {1}'.format(parser.prog, __version__),
        help='Otis version'
    )
    sub_parser = parser.add_subparsers()
    Run(sub_parser)

    args, extra_args = parser.parse_known_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_usage()
