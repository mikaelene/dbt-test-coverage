#!/usr/scripts/env python
from setuptools import find_packages
from distutils.core import setup
from src import __version__


package_name = "dbt-test-coverage"
package_version = __version__
description = """A package for test coverage in dbt projects"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    author="Mikael Ene",
    author_email="mikael.ene@gmail.com",
    url="https://github.com/mikaelene/dbt-test-coverage",
    packages=find_packages(),
    install_requires=[
        'PyYAML>=3.11',
    ],
    entry_points={
            'console_scripts': ['dbt-test-coverage=src.main:main'],
        },
)
