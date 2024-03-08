import numpy as np
import numdifftools as nd
from .abstract_simulated_annealing import AbstractAnnealer
from ..utils import get_random_value_by_range


class StandardAnnealer(AbstractAnnealer):
    def __init__(self, optimize_func, arg_bounds):
        super().__init__(optimize_func, arg_bounds)
        self._grad = nd.Gradient(self._optimize_func)

    def _cooling_func(self, temp, iter):
        alpha = 0.001
        return temp - alpha * iter

    def _get_new_state_arg(self, old_state, arg_bounds):
        grad = self._grad(old_state)
        if np.linalg.norm(grad) < 1e-2:
            return get_random_value_by_range(arg_bounds)
        return old_state - 0.001 * grad

    def _is_need_to_change_state(self, olf_state_energy, new_state_energy):
        delta_energy = new_state_energy - olf_state_energy

        return delta_energy < 0 or np.random.uniform() < np.exp(-delta_energy / self._temp)

    def _is_more_optimal_energy(self, old_state_energy, new_state_energy):
        return (new_state_energy - old_state_energy) < 0
