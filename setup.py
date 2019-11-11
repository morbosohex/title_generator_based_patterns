#!/usr/bin/env python
from setuptools import find_packages

from setuptools import setup

setup(
    name='TitleGenerator',
    version='0.1',
    description='Title generator : based on patterns and dictionary, \
                generate a list of phrases',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        'click>=3.3',
        'beautifulsoup4>=4.4.1',
        'requests>=2.8.1'
    ],
    entry_points={
        'console_scripts': 'title=title_generator.commands.base:cli'
    },
)

