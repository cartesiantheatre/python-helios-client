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
def getLongDescription():
    long_description = []
    with open('README.md') as file:
        long_description.append(file.read())
    return '\n\n'.join(long_description)

# Provide setup parameters for package...
setup(

    # Basic metadata...
    name='helios',
    version='0.1.dev20190518',
    package_dir={'': 'Source'},
    packages=find_namespace_packages(where='Source'),

    include_package_data=True,

    # Depends 
    install_requires=[
        'colorama',
        'hfilesize',
        'requests',
        'termcolor'
    ],

    # Extended metadata to display on PyPI...
    author="Cartesian Theatre",
    author_email="technical_support@heliosmusic.io",
    description="Pure python 3 module to communicate with a Helios server.",
    long_description=getLongDescription(),
    license="LGPL",
    keywords=['music', 'similarity', 'match', 'catalogue', 'digital', 'signal', 'processing'],
    url="https://www.heliosmusic.io",
    project_urls={
        "Bug Tracker": "https://github.com/cartesiantheatre/python3-helios/issues",
        "Documentation": "https://heliosmusic.io/api.html",
        "Source Code": "https://github.com/cartesiantheatre/python3-helios"
    },
    python_requires=">= 3.*",
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
)

