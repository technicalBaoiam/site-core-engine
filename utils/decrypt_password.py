# encrypt password private key (login/signup) this varaible is needed to decrypt encrypted password coming from client
import os
import rsa
from base64 import b64decode
from django.conf import settings
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_private_key():
    private_rsa_path = os.path.join(settings.BASE_DIR / "utils/private_key.pem")
    with open(private_rsa_path, 'r') as key_file:
        private_key = key_file.read()
    return private_key

def decrypt_password(encrypted_password):
    try:
        # load the private key from settings
        print(encrypted_password, 'enc pass line 1')
        private_key_pem = get_private_key().encode()

        # convert from PKCS#8 (if needed) to PKCS#1 (format expected by rsa module)
        private_key_obj = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )

        # export the private key as PKCS#1 (DER format)
        private_key_pkcs1 = private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,  # PKCS#1 format
            encryption_algorithm=serialization.NoEncryption()
        )

        # load the PKCS#1 private key into the rsa library
        private_key = rsa.PrivateKey.load_pkcs1(private_key_pkcs1)

        # decode the base64 encrypted password
        encrypted_password_bytes = b64decode(encrypted_password)

        # decrypt the encrypted password using the private key
        decrypted_password = rsa.decrypt(encrypted_password_bytes, private_key)

        # convert the decrypted password from bytes to a string and return it
        print(decrypted_password.decode('utf-8'),'decrypted pass')
        return decrypted_password.decode('utf-8')

    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        raise ValueError("Invalid password decryption")
