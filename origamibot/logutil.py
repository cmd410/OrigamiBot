from functools import wraps
from time import time


def timeit(func):
    """Check how long a function takes to execute"""
    @wraps(func)
    def new_func(*args, **kwargs):
        st = time()
        result = func(*args, **kwargs)
        print(f'timeit: {time() - st}')
        return result
    return new_func
