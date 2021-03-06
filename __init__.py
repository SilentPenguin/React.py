from decorators import call, sender, receiver, messenger

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