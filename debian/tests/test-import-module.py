#!/usr/bin/env -S python3 -Werror
#
#   Helios, intelligent music.
#   Copyright (C) 2015-2024 Cartesian Theatre. All rights reserved.
#

# System imports...
import sys

# Just verify we can import...
import helios
from helios.client import get_version

# Entry point...
if __name__ == '__main__':

    # Verify we can print the version...
    print(F'Helios client module version {get_version()}')

    sys.exit(0)

