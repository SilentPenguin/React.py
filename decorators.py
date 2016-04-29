from bases import binding, wrapper

def call(*args, **kwargs):
    return args, kwargs
    
class sender(wrapper):
    def __init__(self, *args):
        wrapper.__init__(self, *args)
        self.receivers = set()
        
    def __call__(self, *args, **kwargs):
        call = self.binding.func(*args, **kwargs)
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