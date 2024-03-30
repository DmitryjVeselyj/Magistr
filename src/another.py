# from .abstract_sds import AbstractStochasticDiffusionSearch
# from .agent import Agent
import random

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

key = 'abc'*6


class Agent:
    def __init__(self, hyp_list):
        self._hyp_list = hyp_list
        self._active_per = 0

    def __str__(self):
        return str(self._hyp_list) + '\n' + str(self._active_per)


def test_function(agent):
    indx = random.choice(range(len(key)))
    for i in range(10):
        old_sym = agent._hyp_list[indx]
        new_sym = random.choice('abcdefghijklmnopqrstuvwxyz')
        agent._hyp_list[indx] = new_sym
        if sum(k_sym == hyp_sym for k_sym, hyp_sym in zip(key, agent._hyp_list)) / len(key) > agent._active_per:
            agent._hyp_list[indx] = new_sym
            break
        else:
            agent._hyp_list[indx] = old_sym

    return sum(k_sym == hyp_sym for k_sym, hyp_sym in zip(key, agent._hyp_list)) / len(key)


def optimize(agents_cnt=1000, max_iter=10000):
    agents = [Agent([random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(len(key))]) for i in
              range(agents_cnt)]
    eps = 0.60
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
                    for i in range(10):
                        old_sym = agent._hyp_list[indx]
                        new_sym = random.choice('abcdefghijklmnopqrstuvwxyz')
                        agent._hyp_list[indx] = new_sym
                        if sum(k_sym == hyp_sym for k_sym, hyp_sym in zip(key, agent._hyp_list)) / len(
                                key) > agent._active_per:
                            agent._hyp_list[indx] = new_sym
                            break
                        else:
                            agent._hyp_list[indx] = old_sym


        for agent in agents:
            agent._active_per = test_function(agent)

    return max(agents, key=lambda x: x._active_per)


print(optimize())
