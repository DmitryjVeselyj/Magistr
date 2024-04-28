from src.optimization_methods.stochastic_diffusion_search import CryptoStochasticDiffusionSearch
from cryptography_algorithms import AES
import keras
import numpy as  np
from scipy.optimize import dual_annealing, differential_evolution
from difflib import SequenceMatcher

key = [ord('a'), ord('b')] * 8
model = keras.saving.load_model('hoba.keras')

message = b'hoba' * 4
sym_key = ''.join(map(chr, key))
enc_message = AES(sym_key).encrypt(message)

def func(x):
    x = np.array(x, dtype=np.int32)
    return model.predict(np.array([np.array(AES(''.join(map(chr, x))).decrypt(enc_message))]), verbose=False)[0][0]


std = CryptoStochasticDiffusionSearch(func, [[ord('a'), ord('z')] for _ in range(len(key))], 0.7)
res = std.optimize()
# print(res)
# print(key)
# print([chr(k) for k in res.arg])

orig_bin = ''.join(map(lambda x: format(x, '08b'), map(ord,message.decode('ascii'))))
dec_bin = ''.join(map(lambda x: format(x, '08b'), AES(''.join([chr(int(k)) for k in res.arg])).decrypt(enc_message)))
print(SequenceMatcher(None, orig_bin, dec_bin).ratio())


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


