#!/usr/bin/python3
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2019 Cartesian Theatre. All rights reserved.
#

# Import modules...
from __future__ import with_statement
from setuptools import setup, find_namespace_packages
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

# Provide setup parameters for package...
setup(

    # Metadata...
    author='Cartesian Theatre',
    author_email='info@heliosmusic.io',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description='Pure python 3 module to communicate with a Helios server.',
    keywords=['music', 'similarity', 'match', 'catalogue', 'digital', 'signal', 'processing'],
    license='LGPL',
    long_description=get_long_description(),
    name='helios-client',
    project_urls={
        'Bug Tracker': 'https://github.com/cartesiantheatre/python-helios-client/issues',
        'Documentation': 'https://heliosmusic.io/api.html',
        'Source Code': 'https://github.com/cartesiantheatre/python-helios-client'
    },
    url='https://www.heliosmusic.io',
    version='0.1.dev20190816',

    # Options...
    # TODO: Many of these dependencies are for utilities package only, not
    #  client.
    include_package_data=True,
    install_requires=[
        'argparse',
        'attrs',
        'colorama',
        'hfilesize',
        'marshmallow',
        'requests',
        'termcolor',
        'tqdm',
        'zeroconf'
    ],
    package_dir={'': 'Source'},
    packages=find_namespace_packages(where='Source'),
    python_requires='>= 3.7',
    zip_safe=True
)

