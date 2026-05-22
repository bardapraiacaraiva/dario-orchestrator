# PyInstaller spec for the DARIO license CLI bundle (Onda 9 #3)
# -----------------------------------------------------------------
# Builds a single executable that contains:
#   - license_manager.py  (CLI: activate, init-trial, check, status)
#   - license_client.py   (server I/O + cert pinning)
#   - license_server/     (so VIP customers can self-host)
#
# Build it from the orchestrator dir:
#     cd ~/.claude/orchestrator
#     pyinstaller scripts/dario_license.spec --clean --noconfirm
#
# Output: dist/dario-license[.exe]
#
# Distribution
# ------------
# After building, sign the executable with your code-signing cert:
#     python scripts/sign_bundle.py dist/dario-license.exe
#
# A signed executable means Windows SmartScreen does not warn end-users
# AND modifying the .exe invalidates the signature (Windows refuses to
# launch tampered binaries with the same publisher name).

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['../license_manager.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        # Bundle the license_server package so the same exe can run as a
        # server (`dario-license server`) for VIP customers who self-host.
        ('../license_server', 'license_server'),
        # Client side
        ('../license_client.py', '.'),
    ],
    hiddenimports=[
        # PyInstaller's static analyser sometimes misses these
        'fastapi',
        'uvicorn',
        'uvicorn.lifespan.on',
        'pydantic',
        'pydantic_core',
        'sqlite3',
        'cryptography',
        'cryptography.hazmat.primitives.serialization',
        'cryptography.x509',
        'license_server',
        'license_server.app',
        'license_server.db',
        'license_client',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Trim the bundle — we don't need test runners or build tools.
        'pytest',
        'mypy',
        'ruff',
        'IPython',
        'jupyter',
    ],
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
    [],
    name='dario-license',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                  # UPX confuses some AV engines + signing
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,           # native arch
    codesign_identity=None,     # signed separately via scripts/sign_bundle.py
    entitlements_file=None,
    # icon='scripts/dario.ico',  # uncomment once you have a .ico
)
