# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/EVERYTHING/My_Future/Python/Metin2Helper.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/EVERYTHING/My_Future/Python/_internal/event_notification.wav', '.'), ('D:/EVERYTHING/My_Future/Python/_internal/exit_notification.wav', '.'), ('D:/EVERYTHING/My_Future/Python/_internal/gficon.ico', '.'), ('D:/EVERYTHING/My_Future/Python/_internal/razador_notification.wav', '.')],
    hiddenimports=['plyer.platforms.win.notification'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Metin2Helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\EVERYTHING\\My_Future\\Python\\gficon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Metin2Helper',
)
