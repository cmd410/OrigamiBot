from typing import Callable
from functools import wraps


def condition(c: Callable):
    """Only call function if condition is met"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not c(*args, **kwargs):
                return
            return f(*args, **kwargs)
        return wrapper
    return decorator
