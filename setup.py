# coding=utf8
import os
from setuptools import setup, find_packages


def read_relative_file(filename):
    """Returns contents of the given file.
    Filename argument must be relative to this module.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


version = '1.0'


setup(name='marmelune.games.circularroledealer',
      version=version,
      description="Utility to distribute players in a game, so that the " \
                  "whole players form a circle.",
      long_description=open("README").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=["Programming Language :: Python",
                   "Development Status :: 1 - Planning",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Topic :: Games/Entertainment",
                  ],
      keywords='game distribute players circle ring',
      author='Benoît Bryon',
      author_email='benoit@marmelune.net',
      url='http://github.com/benoitbryon/marmelune.circularroledealer/',
      license='BSD',
      packages=find_packages('src', ''),
      package_dir = {'': 'src'},
      namespace_packages=['marmelune', 'marmelune.games'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
