from src.optimization_methods.simulated_annealing import StandardAnnealer
from cryptography_algorithms import Caesar
from cryptography_algorithms import AES
from scipy.optimize import dual_annealing, differential_evolution
from difflib import SequenceMatcher
from Crypto.Cipher import AES as AESC
# def func(offset):
#     caesar = Caesar(int(offset[0]))
#     return -sum(a == b for a, b in zip("HOBANA", caesar.decrypt("KREDQD")))
#
#
# annealer = StandardAnnealer(func, arg_bounds=[(1, 28)])
# res = annealer.optimize(max_iter=100)
# print(res)


key = 'P' * 16
message = b'HOBA' * 4
aes = AES(key)
enc_msg = aes.encrypt(message)

cipher = AESC.new(key.encode(), AESC.MODE_ECB)
cipher_dec = AESC.new(key.encode(), AESC.MODE_CTR)
en = cipher.encrypt(message)
print(cipher.encrypt(message))
print(enc_msg)
print(cipher_dec.decrypt(en).decode())


def convert_int_str(int_val):
    binary_string = "{:x}".format(int_val)
    splitted_str = [binary_string[i * 2:(i + 1) * 2] for i in range(len(binary_string) // 2)]
    enc_str = ""
    for symbol_in_hex in splitted_str:
        enc_str += (chr(int(symbol_in_hex, 16)))
    return enc_str


def func_aes(int_val):
    key1 = convert_int_str(int(int_val[0])) * 4
    try:
        aes = AES(key1)
        dec_msg = "".join(map(chr, aes.decrypt(enc_msg)))
    except Exception as e:
        return 99999999999
    return -SequenceMatcher(None, key1, key).ratio()


# b'PPPP' = 1347440720
annealer = StandardAnnealer(func_aes, arg_bounds=[(1347440720 - 100, 1347440720 + 100)])
res = annealer.optimize(initial_temp=10000000000, max_iter=10000*2)
print(res)
key = convert_int_str(int(res.arg[0])) * 4
aes = AES(key)

print(message)
print("".join(map(chr, aes.decrypt(enc_msg))).encode())
