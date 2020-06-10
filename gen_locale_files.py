#!/usr/bin/env python

import sys, os

prefix = sys.prefix
try:
    prefix = sys.real_prefix
except AttributeError:
    try:
        prefix = sys.base_prefix
    except AttributeError:
        pass

# This path is correct on Windows.  On various Linux distros, it seems
# that they consider this script 'documentation' or an 'example' and thus
# do not install it by default, or into an easily found location.
script = os.path.join(prefix, "Tools", "i18n", "pygettext.py")

os.system('python "%s" -d vgaming -p locale *.py' % script)
