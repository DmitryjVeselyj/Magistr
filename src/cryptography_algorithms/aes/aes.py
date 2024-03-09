from ..abstract_crypto_algorithm import AbstractCryptoAlgorithm
from .aes_encryption import AESEncryptionHelper
from .aes_decryption import AESDecryptionHelper


class AES(AbstractCryptoAlgorithm):
    def __init__(self, key):
        self._key = key

    def encrypt(self, input_bytes):
        return AESEncryptionHelper(self._key).execute(input_bytes)

    def decrypt(self, input_bytes):
        return AESDecryptionHelper(self._key).execute(input_bytes)
