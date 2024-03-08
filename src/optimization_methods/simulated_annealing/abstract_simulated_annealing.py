from ..abstract_optimization_method import OptimizationMethod
from abc import abstractmethod
from ..utils.optimal_value import OptimalResult
from ..utils import get_random_value_by_range


class AbstractAnnealer(OptimizationMethod):
    @abstractmethod
    def __init__(self, optimize_func, arg_bounds):
        self._state_arg = None
        self._state_energy = None
        self._temp = None

        self._optimize_func = optimize_func
        self._arg_bounds = arg_bounds

    def optimize(self, init_state_arg=None, initial_temp=7777, max_iter=1000):
        self._init_params(init_state_arg, initial_temp)
        optimal_result = OptimalResult(self._state_arg, self._state_energy)

        for i in range(max_iter):
            self._temp = self._cooling_func(self._temp, i)
            if self._temp <= 0:
                break

            new_state_arg = self._get_new_state_arg(self._state_arg, self._arg_bounds)
            new_state_energy = self._optimize_func(new_state_arg)

            if self._is_need_to_change_state(self._state_energy, new_state_energy):
                self._change_state(new_state_arg, new_state_energy)

                if self._is_more_optimal_energy(optimal_result.value, new_state_energy):
                    optimal_result.arg = new_state_arg
                    optimal_result.value = new_state_energy

        return optimal_result

    def _init_params(self, init_state_arg, initial_temp):
        self._state_arg = get_random_value_by_range(self._arg_bounds) if init_state_arg is None else init_state_arg
        self._state_energy = self._optimize_func(self._state_arg)
        self._temp = initial_temp

    @abstractmethod
    def _cooling_func(self, temp, iter):
        pass

    @abstractmethod
    def _get_new_state_arg(self, old_state, values):
        pass

    @abstractmethod
    def _is_need_to_change_state(self, old_state_energy, new_state_energy):
        pass

    @abstractmethod
    def _is_more_optimal_energy(self, old_state_energy, new_state_energy):
        pass

    def _change_state(self, state_arg, state_energy):
        self._state_arg = state_arg
        self._state_energy = state_energy
