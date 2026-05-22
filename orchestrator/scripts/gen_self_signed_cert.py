"""Generate a self-signed code-signing certificate (Onda 10 #2).

Outputs a .pfx that `sign_bundle.py` can use to demonstrate the signing
pipeline end-to-end WITHOUT spending money on an OV/EV cert.

A self-signed cert:
    ✅ Proves the signing pipeline works (signtool + verify all green).
    ✅ Tampered binaries lose their signature → Windows refuses to launch
       with the original publisher identity.
    ❌ Does NOT bypass Windows SmartScreen reputation (end users still
       see the "unrecognised publisher" warning).
    ❌ Does NOT chain to a public CA — only the user who trusted your
       self-signed root can run without warnings.

Upgrade path
------------
When you decide to sell to non-technical end users:
    1. Buy an OV cert from Sectigo / DigiCert (€150-400/year), OR
    2. Buy an EV cert (€200-700/year) — instant SmartScreen trust.
    3. Replace the self-signed .pfx with the real one in `sign_bundle.py`.

The OV/EV path produces identical signtool commands — only the cert
changes. The pipeline you ship with the self-signed cert today is the
SAME pipeline you'll run with the real cert tomorrow.

Usage
-----
    python gen_self_signed_cert.py --pfx ./my-cert.pfx --password secret
    python gen_self_signed_cert.py --cn "Acme Lda" --pfx ./acme.pfx
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def generate_pfx(
    out_path: Path,
    cn: str,
    password: str,
    org: str = "DARIO Self-Signed CI",
    country: str = "PT",
    days: int = 365,
) -> Path:
    """Generate a 2048-bit RSA code-signing certificate and write a PKCS#12 (.pfx)."""
    # 1. Key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # 2. Subject + issuer (self-signed → same)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        x509.NameAttribute(NameOID.COMMON_NAME, cn),
    ])

    # 3. Cert with CodeSigning EKU
    now = dt.datetime.now(dt.UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - dt.timedelta(minutes=1))
        .not_valid_after(now + dt.timedelta(days=days))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CODE_SIGNING]),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )

    # 4. Serialize as PKCS#12 (.pfx) — what signtool /f expects
    pfx_bytes = pkcs12.serialize_key_and_certificates(
        name=cn.encode("utf-8"),
        key=private_key,
        cert=cert,
        cas=None,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password.encode("utf-8")
        ),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(pfx_bytes)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a self-signed code-signing .pfx (Onda 10 #2)"
    )
    parser.add_argument("--pfx", type=Path, required=True,
                         help="Output path for the .pfx file.")
    parser.add_argument("--password", required=True,
                         help="Password to encrypt the .pfx.")
    parser.add_argument("--cn", default="DARIO License Self-Signed",
                         help="Common Name (publisher identity). Default: "
                              "'DARIO License Self-Signed'.")
    parser.add_argument("--org", default="DARIO Self-Signed CI",
                         help="Organisation name. Default 'DARIO Self-Signed CI'.")
    parser.add_argument("--country", default="PT", help="2-letter country code")
    parser.add_argument("--days", type=int, default=365, help="Validity in days")
    args = parser.parse_args()

    path = generate_pfx(
        out_path=args.pfx,
        cn=args.cn,
        password=args.password,
        org=args.org,
        country=args.country,
        days=args.days,
    )
    size_kb = path.stat().st_size / 1024
    print(f"Wrote {path} ({size_kb:.1f} KB)")
    print(f"CN:      {args.cn}")
    print(f"Org:     {args.org}")
    print(f"Valid:   {args.days} days")
    print("")
    print("Use it with sign_bundle.py:")
    print(f"  DARIO_CERT_PFX_PASSWORD={args.password} \\")
    print(f"      python scripts/sign_bundle.py dist/dario-license.exe --pfx {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
