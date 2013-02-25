# coding=utf8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read().strip()


NAME = 'circleofgifts'
VERSION = read_relative_file('VERSION')
DESCRIPTION = "Small application to deal roles in a game."
README = read_relative_file('README')
PACKAGES = [NAME]
ENTRY_POINTS = {}


def run_setup():
    """Actually setup package."""
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=README,
          classifiers=["Programming Language :: Python",
                       "Development Status :: 1 - Planning",
                       "License :: OSI Approved :: BSD License",
                       "Operating System :: OS Independent",
                       "Topic :: Games/Entertainment"],
          keywords='game, distribute, players, circle, ring',
          author='Benoît Bryon',
          author_email='benoit@marmelune.net',
          url='http://github.com/benoitbryon/circleofgifts/',
          license='BSD',
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=['setuptools'],
          entry_points=ENTRY_POINTS)


if __name__ == '__main__':  # Don't trigger setup during import().
    run_setup()
