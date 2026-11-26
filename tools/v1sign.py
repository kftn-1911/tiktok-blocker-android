"""Minimal APK v1 (JAR) signer, so no Java/apksigner is needed.

Usage: python v1sign.py in.apk out.apk

Generates a throwaway RSA key + self-signed certificate on every run
(nothing is saved). v1 signing is enough because the app targets SDK 28.
Requires: pip install cryptography
"""
import base64, datetime, hashlib, sys, zipfile
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.x509.oid import NameOID

src, dst = sys.argv[1], sys.argv[2]
b64 = lambda b: base64.b64encode(b).decode()
sha = lambda b: hashlib.sha256(b).digest()

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "placeholder")])
now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
        .public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now).not_valid_after(now + datetime.timedelta(days=365 * 50))
        .sign(key, hashes.SHA256()))

zin = zipfile.ZipFile(src)
entries = [(i, zin.read(i.filename)) for i in zin.infolist()
           if not i.filename.startswith("META-INF/")]

mf = b"Manifest-Version: 1.0\r\nCreated-By: 1.0 (Android)\r\n\r\n"
sf_body = b""
for info, data in entries:
    section = f"Name: {info.filename}\r\nSHA-256-Digest: {b64(sha(data))}\r\n\r\n".encode()
    mf += section
    sf_body += f"Name: {info.filename}\r\nSHA-256-Digest: {b64(sha(section))}\r\n\r\n".encode()
sf = (b"Signature-Version: 1.0\r\nCreated-By: 1.0 (Android)\r\n"
      + f"SHA-256-Digest-Manifest: {b64(sha(mf))}\r\n\r\n".encode() + sf_body)

sig = (pkcs7.PKCS7SignatureBuilder().set_data(sf)
       .add_signer(cert, key, hashes.SHA256())
       .sign(serialization.Encoding.DER,
             [pkcs7.PKCS7Options.DetachedSignature, pkcs7.PKCS7Options.NoAttributes]))

with zipfile.ZipFile(dst, "w") as zout:
    for info, data in entries:
        zout.writestr(info, data, compress_type=info.compress_type)
    for n, d in (("META-INF/MANIFEST.MF", mf), ("META-INF/CERT.SF", sf), ("META-INF/CERT.RSA", sig)):
        zout.writestr(n, d, compress_type=zipfile.ZIP_DEFLATED)
print("signed", dst)
