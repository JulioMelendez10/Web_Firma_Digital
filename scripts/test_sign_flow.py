import os
import tempfile
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# This script validates the signing flow locally by creating a temp key pair,
# signing sample content with a private key, and verifying with the public key.

BASE_DIR = Path(__file__).resolve().parent.parent

# Generate a private/public key pair for the test
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Sample document and digest
sample_text = b'This is a signature test for Web Firma Digital.'
digest = hashes.Hash(hashes.SHA256())
digest.update(sample_text)
hash_value = digest.finalize()

# Sign the hash with the private key
signature = private_key.sign(hash_value, padding.PKCS1v15(), hashes.SHA256())

# Verify using the public key
try:
    public_key.verify(signature, hash_value, padding.PKCS1v15(), hashes.SHA256())
    print('OK: Signature verification succeeded')
except Exception as e:
    print('ERROR: Signature verification failed')
    print(e)

# Write key files as a quick smoke test
with tempfile.TemporaryDirectory() as tmpdir:
    key_path = Path(tmpdir) / 'private_test.key'
    cert_path = Path(tmpdir) / 'public_test.pem'

    key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(key_path, 'wb') as key_file:
        key_file.write(key_bytes)

    pem_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(cert_path, 'wb') as cert_file:
        cert_file.write(pem_bytes)

    print('Test key and cert written to:', key_path, cert_path)
