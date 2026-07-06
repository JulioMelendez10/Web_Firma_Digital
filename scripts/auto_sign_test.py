import os
import sys
import base64
import django
from datetime import datetime, timedelta

# Ensure project root is on sys.path when running this script directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from django.core.files import File
from django.utils import timezone

from certificates.models import Certificado
from documentacion.models import Documento
from django.contrib.auth import get_user_model

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_key_and_cert():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "MX"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Test Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, "test.local"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow() - timedelta(days=1))
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )

    certs_dir = os.path.join(MEDIA_ROOT, 'certificados')
    ensure_dir(os.path.join(certs_dir, 'cer'))
    ensure_dir(os.path.join(certs_dir, 'key'))

    key_path = os.path.join(certs_dir, 'key', 'test_key.pem')
    cert_path = os.path.join(certs_dir, 'cer', 'test_cert.pem')

    with open(key_path, 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(cert_path, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return cert_path, key_path

def create_certificado(cert_path, key_path):
    # create Certificado instance assigning files
    with open(cert_path, 'rb') as cer_f, open(key_path, 'rb') as key_f:
        cer_file = File(cer_f)
        key_file = File(key_f)
        certificado = Certificado()
        certificado.archivo_cer.save(os.path.basename(cert_path), cer_file, save=False)
        certificado.archivo_key.save(os.path.basename(key_path), key_file, save=False)
        certificado.numero_serie = str(certificado.pk or 'test-serial')
        certificado.save()
    return certificado

def create_documento(usuario):
    docs_dir = os.path.join(MEDIA_ROOT, 'documentos')
    ensure_dir(docs_dir)
    doc_path = os.path.join(docs_dir, 'test_document.txt')
    with open(doc_path, 'wb') as f:
        f.write(b'This is a test document for signing.\n')

    with open(doc_path, 'rb') as f:
        django_file = File(f)
        documento = Documento(titulo='Documento de prueba', descripcion='Prueba de firma', usuario=usuario)
        documento.archivo.save('test_document.txt', django_file, save=False)
        documento.save()
    return documento

def sign_document(documento, certificado):
    hash_val = documento.calcular_hash()
    with open(certificado.archivo_key.path, 'rb') as key_file:
        key_data = key_file.read()
    private_key = serialization.load_pem_private_key(key_data, password=None)
    signature = private_key.sign(
        hash_val.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    documento.certificado = certificado
    documento.firma_sha256 = base64.b64encode(signature).decode('utf-8')
    documento.esta_firmado = True
    documento.fecha_firma = timezone.now()
    documento.save()

def main():
    User = get_user_model()
    user = User.objects.filter(username='admin').first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', '123456')
    cert_path, key_path = generate_key_and_cert()
    certificado = create_certificado(cert_path, key_path)
    documento = create_documento(user)
    sign_document(documento, certificado)
    print('Created certificado id=', certificado.pk)
    print('Created documento id=', documento.pk)
    print('Visit: http://localhost:8000/certificates/ and http://localhost:8000/documents/{}/'.format(documento.pk))

if __name__ == '__main__':
    main()
