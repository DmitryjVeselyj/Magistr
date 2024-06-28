from Crypto.Cipher import AES
import base64

# Функция для дополнения текста до кратного 16 (размер блока AES)
def pad(text):
    padding_length = 16 - (len(text) % 16)
    return text + (chr(padding_length) * padding_length)

# Функция для удаления дополнения
def unpad(text):
    padding_length = ord(text[-1])
    return text[:-padding_length]

# Шифрование текста в режиме ECB
def encrypt_ecb(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plain_text)
    encrypted_bytes = cipher.encrypt(padded_text.encode())
    return base64.b64encode(encrypted_bytes).decode()

# Дешифрование текста в режиме ECB
def decrypt_ecb(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted_text.encode())
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return unpad(decrypted_bytes.decode())

# Ключ AES (должен быть 16, 24 или 32 байта)
key = b'This is a key123'

# Пример текста с повторяющимися фразами
plain_text = "HOBAHOBAHOBAHOBAHOBAHOBAHOBAHOBA"

# Шифрование текста
encrypted_text = encrypt_ecb(plain_text, key)
print(f"Encrypted: {encrypted_text}")

# Дешифрование текста
decrypted_text = decrypt_ecb(encrypted_text, key)
print(f"Decrypted: {decrypted_text}")


def encrypt_ecb_blocks(plain_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plain_text)
    encrypted_blocks = [cipher.encrypt(padded_text[i:i+16].encode()) for i in range(0, len(padded_text), 16)]
    return encrypted_blocks

# Зашифрованные блоки
encrypted_blocks = encrypt_ecb_blocks(plain_text, key)
for i, block in enumerate(encrypted_blocks):
    print(f"Block {i}: {block.hex()}")
