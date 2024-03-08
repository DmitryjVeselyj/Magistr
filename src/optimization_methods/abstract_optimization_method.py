from abc import ABC, abstractmethod


class OptimizationMethod(ABC):
    @abstractmethod
    def optimize(self, *args, **kwargs):
        pass
