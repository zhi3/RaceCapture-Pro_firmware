# -*- mode: python -*-
# RaceCapture PyInstaller spec file. This builds a folder with the necessary files to
# run RaceCapture - it also includes *all* kv files and *all* ttf files from the root
# RaceCapture folder. If we add kv or ttf files which are not to go in the distribution
# (or add any other file types that are required) then these will need to be manually
# enumerated in this file. CLR 2014-05-26
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals(), ['hooks'])
def addKVs():
    import os
    extraDatas = []
    for file in os.listdir('..'):
        if file.endswith(".kv") | file.endswith(".ttf"):
            print "Adding datafile: " + file
            extraDatas.append((file, "../" + file, 'DATA'))
    return extraDatas

a = Analysis(['..//racecapture.py'],
             pathex=['..//'],
             hiddenimports=[],
             runtime_hooks=None)
a.datas += addKVs()
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='racecapture.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='racecapture')