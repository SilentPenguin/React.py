'''
Senders are callables which call subsiquent methods when called
Receivers are callables which receive calls from Senders
Messengers provide the functionality of both Senders and Receivers

The call function formats whatever you pass it, for the internals of a
receiver. If you don't return a value, then any receivers connected to the
sender will not be called.

Any receivers attached to a sender must be callable using the same signature
as the signature in your return call() statement.

Senders and receivers can then be connected together using the >> syntax, and
disconnected using // syntax.

@sender
def my_sender(i): 
	print i
	return call(i, 1)  #return a value for a receiver
	
@messenger
def my_messenger(i, v):
	return call(i + v)
	
@receiver
def my_receiver(i):
	print i
	
my_sender >> my_messenger >> my_receiver
my_sender(1)
my_sender // my_messenger // my_receiver	
'''

from functools import update_wrapper
from importlib import import_module

def call(*args, **kwargs):
    return args, kwargs

class wrapper(object):
    def __init__(self, func, inst=None, type=None):
        update_wrapper(self, func)
        self.inst = inst
        self.func = func.__get__(inst, type) if inst else func
        
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
        
    def __get__(self, inst, type):
        if not inst or self.__class__ is inst.__class__: return self
        context = self.__class__(self.func, inst, type)
        setattr(inst, self.__name__, context)
        return context
    
    def __getstate__(self):
        return (self.func.im_self if self.inst else self.func.__module__,
                self.__name__,
                self.senders if hasattr(self, 'senders') else None,
                self.receivers if hasattr(self,'receivers') else None)
        
    def __setstate__(self, state):
        inst, name, senders, receivers = state
        self.inst = import_module(inst) if type(inst) is str else inst
        self.func = getattr(self.inst, name).func
        if senders is not None: self.senders = senders
        if receivers is not None: self.receivers = receivers
    
class sender(wrapper):
    def __init__(self, *args):
        wrapper.__init__(self, *args)
        self.receivers = set()
        
    def __call__(self, *args, **kwargs):
        call = self.func(*args, **kwargs)
        if call is None: return
        args, kwargs = call
        for receiver in self.receivers:
            receiver(*args, **kwargs)
            
    def __rshift__(self, target):
        self.receivers.add(target)
        target.senders.add(self)
        return target
        
    def __floordiv__(self, target):
        self.receivers.remove(target)
        target.senders.remove(self)
        return target
        
class receiver(wrapper):
    def __init__(self, *args):
        wrapper.__init__(self, *args)
        self.senders = set()
        
class messenger(sender, receiver):
    def __init__(self, *args):
        sender.__init__(self, *args)
        receiver.__init__(self, *args)
