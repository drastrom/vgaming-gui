#!/usr/bin/env python

import subprocess
import sys

from PyInstaller.compat import exec_python_rc
from wx.tools.pywxrc import XmlResourceCompiler

XmlResourceCompiler().MakePythonModule(["vgaming.xrc"], "vgaming_xrc.py", embedResources=True, generateGetText=True, assignVariables=False)

retcode = exec_python_rc("-OO", "-m", "PyInstaller", "vgaming.spec")
if retcode:
	raise subprocess.CalledProcessError(retcode, sys.executable)
