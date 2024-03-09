from src.cryptography_algorithms.abstract_crypto_algorithm import AbstractCryptoAlgorithm


class Caesar(AbstractCryptoAlgorithm):
    def __init__(self, offset):
        self._offset = offset

    def encrypt(self, msg):
        encrypted_msg = ""
        for symbol in msg:
            if symbol.isupper():
                encrypted_msg += chr((ord(symbol) + self._offset - 65) % 26 + 65)
            else:
                encrypted_msg += chr((ord(symbol) + self._offset - 97) % 26 + 97)

        return encrypted_msg

    def decrypt(self, msg):
        decrypted_msg = ""
        for symbol in msg:
            if symbol.isupper():
                decrypted_msg += chr((ord(symbol) - self._offset - 65) % 26 + 65)
            else:
                decrypted_msg += chr((ord(symbol) - self._offset - 97) % 26 + 97)

        return decrypted_msg
