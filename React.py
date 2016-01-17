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

def call(*args, **kwargs):
    return args, kwargs

class sendercontext(object):
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
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

class sender(sendercontext):
    def __get__(self, inst, type):
        func = self.func.__get__(inst, type)
        context = sendercontext(func)
        setattr(inst, func.__name__, context)
        return context
        
class receivercontext(object):
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func
        self.senders = set()
    
    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)
    
class receiver(receivercontext):
    def __get__(self, inst, type):
        func = self.func.__get__(inst, type)
        context = receivercontext(func)
        setattr(inst, func.__name__, context)
        return context

class messengercontext(sendercontext, receivercontext):
    def __init__(self, func):
        sendercontext.__init__(self, func)
        receivercontext.__init__(self, func)
        
class messenger(messengercontext):
    def __get__(self, inst, type):
        func = self.func.__get__(inst, type)
        context = messengercontext(func)
        setattr(inst, func.__name__, context)
        return context
