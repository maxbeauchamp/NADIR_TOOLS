#!/usr/bin/env python3

import setuptools, os, re

# with open("README.md", "r") as fh:
    # long_description = fh.read()
long_description = """NATL60 is a set of libraries to deal with NATL60 maps and both nadir/swot NATL60-based datasets
"""

def filter_dirs(x):
  val  = x!='__pycache__'
  val &= x!='.DS_Store'
  val &= x!='pyks'
  val &= not x.endswith('.py')
  return val


def find_version(*file_paths):
    """Get version by regex'ing a file."""
    # Source: packaging.python.org/guides/single-sourcing-package-version

    def read(*parts):
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, *parts), 'r') as fp:
            return fp.read()

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(

    # Basic meta
    name="NATL60",
    version=find_version("natl60", "__init__.py"),
    author="Maxime Beauchamp",
    author_email="maxime.beauchamp76@gmail.com",
    description="NATL60 maps and both nadir/swot NATL60-based datasets toolbox",

    # File inclusion
    # Note: find_packages() only works on __init__ dirs.
    packages=setuptools.find_packages()+\
      ['natl60.mods.'+x for x in os.listdir('natl60/mods') if filter_dirs(x)]
    package_data={
        '': ['dpr_config.ini'],
    },

    py_modules=["example_1","example_2","example_3"],

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxbeauchamp/NATL60",
    keywords='natl60; nadir; swot; NetCDF',
)


