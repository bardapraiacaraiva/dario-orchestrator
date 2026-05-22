"""Sign a built PyInstaller binary with a code-signing certificate (Onda 9 #3).

Wraps Microsoft `signtool` (Windows) or `codesign` (macOS). Linux binaries
are not code-signed by convention (use deb/rpm package signing instead).

Prerequisites
-------------
Windows:
    - signtool.exe in PATH (ships with Windows 10/11 SDK)
    - A code-signing certificate (e.g. from Sectigo / DigiCert).
      Either:
        a) Installed in the local cert store under "My" — pass --cert-subject
           "CN=Your Org Name"
        b) Standalone .pfx file — pass --pfx ./your.pfx and the password via
           DARIO_CERT_PFX_PASSWORD env var (or --pfx-password).

macOS:
    - codesign (built into macOS)
    - A Developer ID Application certificate installed in the keychain.
      Pass --cert-identity "Developer ID Application: Your Org (TEAMID)".

Usage
-----
    # Windows, with cert in cert store
    python sign_bundle.py dist/dario-license.exe --cert-subject "CN=ACME Lda"

    # Windows, with .pfx
    DARIO_CERT_PFX_PASSWORD=secret \\
        python sign_bundle.py dist/dario-license.exe --pfx ./acme.pfx

    # macOS
    python sign_bundle.py dist/dario-license \\
        --cert-identity "Developer ID Application: ACME Lda (XXXXXXXXXX)"

The signature is verified with:
    - Windows : signtool verify /pa /v dist/dario-license.exe
    - macOS   : codesign --verify --verbose dist/dario-license

Honesty
-------
Code signing is *not* an obfuscation technique. What it gives you:

    1. Windows SmartScreen + macOS Gatekeeper accept the binary without
       warnings (huge UX win — uninformed users no longer see "this app
       is unrecognised").
    2. Any modification of the .exe AFTER signing invalidates the
       signature. Tampered binaries fail to launch with the original
       publisher identity, so the attacker can't impersonate you.
    3. End-users have a verifiable chain of trust: cert → CA → root.

What it does NOT do:
    - Prevent reverse engineering (the binary is still inspectable).
    - Stop someone re-signing with their own cert under a different
      publisher name (but that loses your reputation).

Combine with the Onda 8 license server (server-side enforcement) +
Cython obfuscation (Onda 9 #2) + cert pinning (Onda 9 #1) for defence
in depth.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str]) -> int:
    print(f"[sign] $ {' '.join(cmd)}")
    return subprocess.call(cmd)


def sign_windows(
    binary: Path,
    cert_subject: str | None,
    pfx: Path | None,
    pfx_password: str | None,
    timestamp_url: str,
) -> int:
    if not shutil.which("signtool"):
        print(
            "[sign] ERROR: signtool.exe not found in PATH. Install the "
            "Windows 10/11 SDK and re-open the terminal.",
            file=sys.stderr,
        )
        return 2

    cmd = [
        "signtool",
        "sign",
        "/fd",
        "SHA256",
        "/tr",
        timestamp_url,
        "/td",
        "SHA256",
    ]
    if pfx:
        cmd += ["/f", str(pfx)]
        password = pfx_password or os.getenv("DARIO_CERT_PFX_PASSWORD")
        if password:
            cmd += ["/p", password]
        else:
            print(
                "[sign] WARNING: signing with .pfx but no password supplied — "
                "signtool will prompt interactively.",
                file=sys.stderr,
            )
    elif cert_subject:
        cmd += ["/n", cert_subject, "/s", "My"]
    else:
        print(
            "[sign] ERROR: provide either --cert-subject or --pfx.",
            file=sys.stderr,
        )
        return 2

    cmd += ["/v", str(binary)]
    rc = _run(cmd)
    if rc != 0:
        return rc

    # Verify
    return _run(["signtool", "verify", "/pa", "/v", str(binary)])


def sign_macos(binary: Path, cert_identity: str | None) -> int:
    if not shutil.which("codesign"):
        print("[sign] ERROR: codesign not found. Install Xcode CLT.", file=sys.stderr)
        return 2
    if not cert_identity:
        print("[sign] ERROR: --cert-identity is required on macOS.", file=sys.stderr)
        return 2

    cmd = [
        "codesign",
        "--force",
        "--options",
        "runtime",
        "--timestamp",
        "--sign",
        cert_identity,
        str(binary),
    ]
    rc = _run(cmd)
    if rc != 0:
        return rc
    return _run(["codesign", "--verify", "--verbose", str(binary)])


def main() -> int:
    parser = argparse.ArgumentParser(description="Code-sign a PyInstaller binary")
    parser.add_argument("binary", type=Path, help="Path to the executable to sign")
    parser.add_argument(
        "--cert-subject",
        help="Windows: Subject CN of cert in the 'My' store "
             "(e.g. 'CN=Your Org Name').",
    )
    parser.add_argument(
        "--pfx", type=Path, help="Windows: path to a .pfx certificate file."
    )
    parser.add_argument(
        "--pfx-password",
        help="Password for the .pfx (or set DARIO_CERT_PFX_PASSWORD env).",
    )
    parser.add_argument(
        "--cert-identity",
        help="macOS: 'Developer ID Application: Your Org (TEAMID)' identity.",
    )
    parser.add_argument(
        "--timestamp-url",
        default="http://timestamp.digicert.com",
        help="RFC 3161 timestamp server URL (default: DigiCert).",
    )
    args = parser.parse_args()

    if not args.binary.exists():
        print(f"[sign] ERROR: binary not found: {args.binary}", file=sys.stderr)
        return 1

    system = platform.system()
    if system == "Windows":
        return sign_windows(
            args.binary, args.cert_subject, args.pfx, args.pfx_password,
            args.timestamp_url,
        )
    if system == "Darwin":
        return sign_macos(args.binary, args.cert_identity)
    print(
        f"[sign] Code-signing not applicable on {system}. "
        "Use distro-level package signing (deb-sign, rpmsign, etc.) instead.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
