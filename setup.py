#!/usr/bin/env python
import os
from setuptools import setup, find_packages

import otis

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
requirements = []

setup(
    name=otis.__title__,
    version=otis.__version__,
    description="Otis.",
    author='David Remm',
    author_email='daveremm@gmail.com',
    url='https://github.com/davidremm/otis',
    scripts=["bin/otis"],
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ],
)
