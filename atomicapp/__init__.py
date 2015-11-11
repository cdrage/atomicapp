"""
 Copyright 2015 Red Hat, Inc.

 This file is part of Atomic App.

 Atomic App is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Atomic App is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with Atomic App. If not, see <http://www.gnu.org/licenses/>.
"""
import logging
import os
from atomicapp.constants import LOG_FILE

# Let's make sure logging works upon first startup
path = LOG_FILE

# Touch if it doesn't exist
if not (os.path.exists(path)):
    try:
        os.utime(path, None)
    except:
        open(path, 'a').close()

if not (os.access(path, os.W_OK)):
    raise RuntimeError("%s is not writeable" % path)

# Setup log handling
handler = logging.FileHandler(path)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger("atomicapp").addHandler(handler)
logging.getLogger("atomicapp").propagate = True
