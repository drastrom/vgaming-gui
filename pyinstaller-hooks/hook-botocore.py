#-----------------------------------------------------------------------------
# Copyright (c) 2015-2020, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------
#
# Botocore is a low-level interface to a growing number of Amazon Web Services.
# Botocore serves as the foundation for the AWS-CLI command line utilities. It
# will also play an important role in the boto3.x project.
#
# The botocore package is compatible with Python versions 2.6.5, Python 2.7.x,
# and Python 3.3.x and higher.
#
# https://botocore.readthedocs.org/en/latest/
#
# Tested with botocore 1.4.36

import os.path
from PyInstaller.utils.hooks import get_package_paths
try:
    from PyInstaller.compat import is_py2
except ImportError:
    import sys
    is_py2 = sys.version[0] == 2

from PyInstaller.utils.hooks import is_module_satisfies

if is_module_satisfies('botocore >= 1.4.36'):
    if is_py2:
        hiddenimports = ['HTMLParser']
    else:
        hiddenimports = ['html.parser']


pkg_base, pkg_dir = get_package_paths('botocore')

datas = [(os.path.join(pkg_dir, "cacert.pem"), 'botocore'),
         (os.path.join(pkg_dir, "data", "*.json"), 'botocore/data'),
         (os.path.join(pkg_dir, "data", "ec2", "2016-11-15"), 'botocore/data/ec2/2016-11-15')]
