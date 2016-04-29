from importlib import import_module

class binding(object):
    def __init__(self, func, inst, type):
        self.func = func.__get__(inst, type) if inst else func
        
    def __getstate__(self):
        return (self.func.__self__.__class__ if hasattr(self.func, '__self__') else self.func.__module__,
                self.func.__self__ if hasattr(self.func, '__self__') else None,
                self.func.__name__)
        
    def __setstate__(self, state):
        type, inst, name = state
        type = import_module(type) if isinstance(type, str) else type
        func = getattr(type, name).binding.func
        self.func = func.__get__(inst, type) if inst else func
        
from functools import update_wrapper

class wrapper(object):
    def __init__(self, func, inst=None, type=None):
        update_wrapper(self, func)
        self.binding = binding(func, inst, type)
        
    def __call__(self, *args, **kwargs):
        return self.binding.func(*args, **kwargs)
        
    def __get__(self, inst, type):
        if not inst or self.__class__ is inst.__class__: return self
        wrapper = self.__class__(self.binding.func, inst, type)
        setattr(inst, self.__name__, wrapper)
        return wrapper