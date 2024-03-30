from .abstract_sds import AbstractStochasticDiffusionSearch
from .agent import Agent
import random


class CryptoStochasticDiffusionSearch(AbstractStochasticDiffusionSearch):
    def __init__(self, optimize_func, arg_bounds, desired_score):
        super().__init__(optimize_func, arg_bounds)
        self._desired_score = desired_score

    def initialize_agent(self):
        return Agent([random.randrange(bound[0], bound[1]) for bound in self._arg_bounds], False)

    def diffusion_phase(self):
        for agent in self._agents:
            if agent.score > self._desired_score:
                continue

            polled_agent = random.choice(self._agents)
            if polled_agent.score > self._desired_score:
                agent.hyp = polled_agent.hyp
            else:
                agent.hyp = self.get_new_hypothesis(agent)

    def testing_phase(self):
        for agent in self._agents:
            agent.score = self._optimize_func(agent.hyp)

    def get_new_hypothesis(self, agent):
        indx = random.choice(range(len(self._arg_bounds)))

        for i in range(10):
            tmp_agent_hyp = agent.hyp
            tmp_agent_hyp[indx] = random.randrange(self._arg_bounds[indx][0], self._arg_bounds[indx][1])
            new_score = self._optimize_func(tmp_agent_hyp)
            if new_score > agent.score:  # calc two times not good
                return tmp_agent_hyp

        return agent.hyp

    def is_halt_criteria_reached(self):
        eps = 0.75
        return all([agent.score > eps for agent in self._agents])
