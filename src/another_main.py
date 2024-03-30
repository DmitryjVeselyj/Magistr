from src.optimization_methods.stochastic_diffusion_search import CryptoStochasticDiffusionSearch

key = [ord('a'), ord('b')] * 20


def func(x):
    return sum(key_elem == x_elem for key_elem, x_elem in zip(key, x)) / len(key)


std = CryptoStochasticDiffusionSearch(func, [[ord('a'), ord('z')] for _ in range(len(key))], 0.75)
res = std.optimize()
print(res)
print(key)
print([chr(k) for k in res.arg])

