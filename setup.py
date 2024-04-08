#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# Import modules...
from __future__ import with_statement
from setuptools import setup, find_packages
import importlib.util
import os
import sys

# To allow this script to be run from any path, change the current directory to
#  the one hosting this script so that setuptools can find the required files...
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Get the long description from the ReadMe.md...
def get_long_description():
    long_description = []
    with open('README.md') as file:
        long_description.append(file.read())
    return '\n\n'.join(long_description)

# Read the module version directly out of the source...
def get_version():

    # Path to file containing version string...
    version_file = None

    # Load the version module...
    spec = importlib.util.spec_from_file_location('__version__', 'Source/helios/__version__.py')
    spec.cached = None # Doesn't work
    version_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_module)

    # Return the version string...
    return version_module.version

# Provide setup parameters for package...
setup(

    # Metadata...
    author='Cartesian Theatre',
    author_email='kip@heliosmusic.io',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description='Pure python 3 module to communicate with a Helios server.',
    keywords=[
        'music',
        'similarity',
        'match',
        'catalogue',
        'digital',
        'signal',
        'processing',
        'machine',
        'learning'],
    license='LGPL',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    name='helios-client',
    project_urls={
        'Bug Tracker': 'https://github.com/cartesiantheatre/python-helios-client/issues',
        'Documentation': 'https://heliosmusic.io/api.html',
        'Source Code': 'https://github.com/cartesiantheatre/python-helios-client'
    },
    url='https://www.heliosmusic.io',
    version=get_version(),

    # Options...
    include_package_data=True,
    install_requires=[
        'attrs >= 18.2.0',
        'brotli',
        'marshmallow >= 3.16.0',
        'requests',
        'requests-toolbelt',
        'simplejson',
        'tqdm',
        'urllib3'
    ],
    package_dir={'': 'Source'},
    packages=find_packages(where='Source'),
    python_requires='>= 3.7',
    zip_safe=True
)

