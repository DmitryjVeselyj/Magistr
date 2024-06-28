from ..abstract_optimization_method import OptimizationMethod
from abc import abstractmethod
from ..utils.optimal_value import OptimalResult


class AbstractStochasticDiffusionSearch(OptimizationMethod):
    @abstractmethod
    def __init__(self, optimize_func, arg_bounds):
        self._optimize_func = optimize_func
        self._arg_bounds = arg_bounds
        self._agents = []

    def optimize(self, agents_cnt=100, max_iter=1000):
        self._agents = self.initialize_agents(agents_cnt)

        iter_cnt = 0
        while iter_cnt < max_iter and not self.is_halt_criteria_reached():
            self.diffusion_phase()
            self.testing_phase()
            iter_cnt += 1

        best_agent = max(self._agents, key=lambda agent: agent.score)
        return OptimalResult(best_agent.hyp, best_agent.score)

    def initialize_agents(self, agents_cnt):
        agents = []
        for i in range(agents_cnt):
            agents.append(self.initialize_agent())

        return agents

    @abstractmethod
    def initialize_agent(self):
        pass

    @abstractmethod
    def is_halt_criteria_reached(self):
        pass

    @abstractmethod
    def diffusion_phase(self):
        pass

    @abstractmethod
    def testing_phase(self):
        pass
