import random

from src.optimization_methods.stochastic_diffusion_search import CryptoStochasticDiffusionSearch
from cryptography_algorithms import AES
import keras
import numpy as  np
from scipy.optimize import dual_annealing, differential_evolution
from difflib import SequenceMatcher

key = [ord('a'), ord('b')] * 8
model = keras.saving.load_model('hoba.keras')

message = b'cdcd' * 4
sym_key = ''.join(map(chr, key))
enc_message = AES(sym_key).encrypt(message)

def func(x):
    x = np.array(x, dtype=np.int32)
    # print(x)
    # return sum(1 for val in np.array(AES(''.join(map(chr, x))).decrypt(enc_message)) if val >= 97 and val <= 122) / 16
    dec_msg = np.array(AES(''.join(map(chr, x))).decrypt(enc_message))

    # return model.predict(np.median(dec_msg), np.var(dec_msg), np.median(list(map(ord, generated_key))), np.var(list(map(ord, generated_key))))
    return model.predict(np.array([np.array(AES(''.join(map(chr, x))).decrypt(enc_message))]), verbose=False)[0][0]






std = CryptoStochasticDiffusionSearch(func, [[ord('a'), ord('c')] for _ in range(len(key))], 0.1)
res = std.optimize()
# print(res)
# print(key)
# print([chr(k) for k in res.arg])

orig_bin = ''.join(map(lambda x: format(x, '08b'), map(ord,message.decode('ascii'))))
dec_bin = ''.join(map(lambda x: format(x, '08b'), AES(''.join([chr(int(k)) for k in res.arg])).decrypt(enc_message)))
# print(SequenceMatcher(None, orig_bin, dec_bin).ratio())
orig_key_bin = ''.join(map(lambda  x: format(x , '08b'), key))
key_bin = ''.join(map(lambda  x: format(x , '08b'), res.arg))
print(sum(x == y for x, y in zip(orig_key_bin, key_bin)) / len(key_bin))

msg = list(map(ord,message.decode('ascii')))
print(msg)
print(key)
print( model.predict(np.array([np.array(AES(sym_key).decrypt(enc_message))]), verbose=False)[0][0])
# std = dual_annealing(func, [[ord('a'), ord('z')] for _ in range(len(key))])
# res = std
# print(res)
# # print(AES(''.join([chr(int(k)) for k in res.x])).decrypt(enc_message))
# # # print([chr(k) for k in res.arg])
# #
# # print(AES(''.join([chr(int(k)) for k in res.x])).decrypt(enc_message))
#
# orig_bin = ''.join(map(lambda x: format(x, '08b'), map(ord,message.decode('ascii'))))
# dec_bin = ''.join(map(lambda x: format(x, '08b'), AES(''.join([chr(int(k)) for k in res.x])).decrypt(enc_message)))
# print(SequenceMatcher(None, orig_bin, dec_bin).ratio())


