from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncriptacionService:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)

    def _get_or_create_key(self):
        key_file = "datos/secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                return file.read()
        else:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(b"mi_clave_secreta"))
            
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, "wb") as file:
                file.write(key)
            return key

    def encriptar(self, texto):
        try:
            texto_bytes = texto.encode()
            texto_encriptado = self.fernet.encrypt(texto_bytes)
            return texto_encriptado.decode()
        except Exception as e:
            print(f"Error al encriptar: {e}")
            return None

    def desencriptar(self, texto_encriptado):
        try:
            texto_bytes = texto_encriptado.encode()
            texto_desencriptado = self.fernet.decrypt(texto_bytes)
            return texto_desencriptado.decode()
        except Exception as e:
            print(f"Error al desencriptar: {e}")
            return None 