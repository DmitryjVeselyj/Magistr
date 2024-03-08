from src.optimization_methods.simulated_annealing import StandardAnnealer
from cryptography_algorithms import Caesar


def func(offset):
    caesar = Caesar(int(offset[0]))
    return -sum(a == b for a, b in zip("HOBANA", caesar.decrypt("KREDQD")))


annealer = StandardAnnealer(func, arg_bounds=[(1, 28)])
res = annealer.optimize(max_iter=100)
print(res)
