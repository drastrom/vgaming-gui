# -*- mode: python ; coding: utf-8 -*-
# vim: set filetype=python :

import time
import sys

import PyInstaller.utils.hooks
PyInstaller.utils.hooks.PY_IGNORE_EXTENSIONS.add(".pyc")
PyInstaller.utils.hooks.PY_IGNORE_EXTENSIONS.add(".pyo")

block_cipher = None

DEBUG = False

year = time.localtime().tm_year
version = (0,0,0,1)
verstr_4part = u"%d.%d.%d.%d" % version
verstr_3part = u"%d.%d.%d" % version[:3]
company_name = u'Drästrøm Science'
product_name = u'vGaming GUI'
copyright = (u'© 2020 ' +
             (' - %d ' % (year,) if year > 2020 else '') +
             company_name)
win_version = None

if sys.platform.startswith('win'):
    from PyInstaller.utils.win32.versioninfo import VSVersionInfo, \
        FixedFileInfo, StringFileInfo, VarFileInfo, StringTable, \
        StringStruct, VarStruct
    # For more details about fixed file info 'ffi' see:
    # http://msdn.microsoft.com/en-us/library/ms646997.aspx
    win_version = VSVersionInfo(
      ffi=FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=version,
        prodvers=version,
        # Contains a bitmask that specifies the valid bits 'flags'r
        mask=0x3f,
        # Contains a bitmask that specifies the Boolean attributes of the file.
        flags=0x2 | 0x1 if DEBUG else 0,
        # The operating system for which this file was designed.
        # 0x4 - NT and there is no need to change it.
        OS=0x40004,
        # The general type of file.
        # 0x1 - the file is an application.
        fileType=0x1,
        # The function of the file.
        # 0x0 - the function is not defined for this fileType
        subtype=0x0,
        # Creation date and time stamp.
        date=(0, 0)
        ),
      kids=[
        StringFileInfo(
          [
          StringTable(
            u'040904B0',
            [StringStruct(u'CompanyName', company_name),
            StringStruct(u'FileDescription', product_name),
            StringStruct(u'FileVersion', verstr_4part),
            StringStruct(u'InternalName', u'vgaming.py'),
            StringStruct(u'LegalCopyright', copyright),
            StringStruct(u'OriginalFilename', u'vgaming.exe'),
            StringStruct(u'ProductName', product_name),
            StringStruct(u'ProductVersion', verstr_4part)])
          ]),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
      ]
    )


a = Analysis(['vgaming.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['pyinstaller-hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='vgaming',
          debug=DEBUG,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          version=win_version,
          manifest='resources/manifest.xml',
          icon='resources/drake_molecule.ico')
app = BUNDLE(exe,
             name='vgaming.app',
             icon='resources/drake_molecule.icns',
             version=verstr_3part,
             bundle_identifier='science.drastrom.vgaming-gui',
             info_plist={
               'CFBundleDisplayName': product_name,
               'CFBundleDevelopmentRegion': 'en_US',
               'CFBundleVersion': verstr_4part if version[3] != 0 else verstr_3part,
               'NSHumanReadableCopyright': copyright
	     })
