# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


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
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , manifest='resources/manifest.xml', icon='resources/drake_molecule.ico')
app = BUNDLE(exe,
             name='vgaming.app',
             icon='resources/drake_molecule.icns',
             bundle_identifier=None)
