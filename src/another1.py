# from .abstract_sds import AbstractStochasticDiffusionSearch
# from .agent import Agent
import random

import numpy as np

from src.optimization_methods.simulated_annealing import StandardAnnealer
from cryptography_algorithms import Caesar
from cryptography_algorithms import AES
from scipy.optimize import dual_annealing, differential_evolution
from difflib import SequenceMatcher

# class StochasticDiffusionSearch(AbstractStochasticDiffusionSearch):
#     def __init__(self, optimize_func, search_space):
#         super().__init__(optimize_func, search_space)
#
#     @abstractmethod
#     def initialize_agent(self):
#         return Agent(''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length)))
#
#     @abstractmethod
#     def diffusion_phase(self):
#         pass
#
#     @abstractmethod
#     def testing_phase(self):
#         pass
#
#     @abstractmethod
#     def is_halt_criteria_reached(self):
#         pass

key = 'P' * 16

message = b'HOBA' * 4

aes = AES(key)
enc_msg = aes.encrypt(message)
iter_cnt = 2
enc_msg_bin = ''.join([str(np.binary_repr(enc)) for enc in enc_msg])
class Agent:
    def __init__(self, hyp_list):
        self._hyp_list = hyp_list
        self._active_per = 0

    def __str__(self):
        return str(self._hyp_list) + '\n' + str(self._active_per)


def metric(hyp):
    try:
        aes = AES(hyp)
        enccc_msg_bin =  ''.join([str(np.binary_repr(enc)) for enc in aes.encrypt(message)])
        return SequenceMatcher(None, enc_msg_bin, enccc_msg_bin).ratio()
    except Exception as e:
        return 0
def test_function(agent):
    indx = random.choice(range(len(key)))
    for i in range(iter_cnt):
        old_sym = agent._hyp_list[indx]
        new_sym = random.choice('abcdefghijklmnopqrstuvwxyz')
        agent._hyp_list[indx] = new_sym
        new_metric = metric(agent._hyp_list)
        if new_metric > agent._active_per:
            agent._hyp_list[indx] = new_sym
            break
        else:
            agent._hyp_list[indx] = old_sym

    return new_metric


def optimize(agents_cnt=100, max_iter=100):
    agents = [Agent([random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(len(key))]) for i in
              range(agents_cnt)]
    eps = 0.4
    for i in range(max_iter):

        if all([agent._active_per > eps for agent in agents]):
            break

        for agent in agents:
            if agent._active_per < eps:
                polled_agent = random.choice(agents)
                if agent._active_per > eps:
                    agent._hyp_list = polled_agent._hyp_list
                else:
                    indx = random.choice(range(len(key)))
                    for i in range(iter_cnt):
                        old_sym = agent._hyp_list[indx]
                        new_sym = random.choice('abcdefghijklmnopqrstuvwxyz')
                        agent._hyp_list[indx] = new_sym
                        new_metric  = metric(agent._hyp_list)
                        if new_metric > agent._active_per:
                            agent._hyp_list[indx] = new_sym
                            agent._active_per = new_metric
                            break
                        else:
                            agent._hyp_list[indx] = old_sym


        for agent in agents:
            agent._active_per = test_function(agent)

    return max(agents, key=lambda x: x._active_per)


print(optimize())
