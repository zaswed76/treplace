#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='scr',
    version='0.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests', 'config'],
    entry_points={
        'console_scripts':
            ['treplace = scr.trepl:main']
        },
    long_description=open(join(dirname(__file__), 'readme.rst')).read(),
)
