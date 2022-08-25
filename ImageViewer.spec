# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ImageViewer.py'],
    pathex=[],
    binaries=[],
    datas=[("ui","ui/"),("utils","utils/"),('iter_4000.pth','.')],
    hiddenimports=['mmcv._ext'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
for d in a.datas:
    if '_C.cp38-win_amd64.pyd' in d[0]:
        a.datas.remove(d)
        break
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ImageViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
