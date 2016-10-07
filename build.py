#!/usr/bin/env python
import argparse
import os
import sys

from nose.core import run
from subprocess import call


def lint():
    path = os.path.realpath(os.getcwd())
    cmd = 'flake8 {0}'.format(path)
    print(cmd)

    try:
        return_code = call([cmd], shell=True)
        if return_code != 0:
            print("Lint checks failed")
            sys.exit(1)
        else:
            print("Lint checks passed")
    except Exception as e:
        print("Execution: {0}".format(e))


def unit_test():
    path = os.path.realpath(os.path.join(os.getcwd(), 'tests/unit/**'))
    args = [
        path, '-x', '-v', '--with-coverage', '--cover-erase', '--cover-package=./otis'
    ]
    if run(argv=args):
        return 0
    else:
        return 1


def test_suite():
    lint()
    unit_test()


def main():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    lint_parser = sub_parser.add_parser('lint')
    lint_parser.set_defaults(func=lint)

    unit_test_parser = sub_parser.add_parser('unit-test')
    unit_test_parser.set_defaults(func=unit_test)

    test_suite_parser = sub_parser.add_parser('test-suite')
    test_suite_parser.set_defaults(func=test_suite)

    args, extra_args = parser.parse_known_args()
    args.func()


if __name__ == '__main__':
    main()
