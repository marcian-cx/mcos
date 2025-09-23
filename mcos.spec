# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['launch_mcos.py'],
    pathex=[],
    binaries=[],
    datas=[('demo_vault', 'demo_vault')],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'markdown',
        'pymdownx.tasklist',
        'pymdownx.superfences',
        'dateutil.parser',
        'pandas',
        'yaml'
    ],
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
    name='MCOS',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MCOS',
)

app = BUNDLE(
    coll,
    name='MCOS.app',
    icon='mcos.icns',
    bundle_identifier='com.marcian.mcos',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Markdown',
                'CFBundleTypeExtensions': ['md', 'markdown'],
                'CFBundleTypeRole': 'Editor'
            }
        ]
    },
)
