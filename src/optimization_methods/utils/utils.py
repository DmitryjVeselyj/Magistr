import numpy as np


def get_random_value_by_range(bounds):
    return np.array([np.random.uniform(elem_interval[0], elem_interval[1]) for elem_interval in bounds])