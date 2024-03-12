# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('password.pkl', '.'), ('username.pkl', '.'), ('green_dragon.png', '.'), ('Neopets-logo.jpg', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Neopets Name Checker v1.2',
    debug=False,
    strip=False,
    upx=True,
    bootloader_ignore_signals=False,
    console=True,
    disable_windowed_traceback=False,
    icon='Blue_wocky_cropped.ico',
)

