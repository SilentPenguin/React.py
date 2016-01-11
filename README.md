# React.py

React.py is a simple python script for functional reactive programming under python.
Using simple syntax, functions, and methods can be connected up in chains.
This allows your code to respond to certain actions in a modular way.

#How does it work?

There are three types of decotrator in React.py:
* Senders transmit their return value to Receivers.
* Receivers are called when any sender that they are connected to returns.
* Messengers act as both senders and receivers.

Finally, Senders and Messengers can return the result of a call(), to call any Receivers that are connected to themselves.
When ```return call()``` is made, any Receivers connected to the Sender will be called after the sender returns.
The signature passed in ```call(*args, **kargs)``` will be used in the call to the receiver.
If a value is not returned, any entities connected to the sender will not be called.

# What does it look like?

React's calls are best used as decorators:

```python
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
```

They can then be connected together by performing:

```python
my_sender >> my_messenger >> my_receiver  #Connects all three functions together
my_sender(1)                              #outputs 1, 2, note, all three functions were called in order.
my_sender // my_messenger // my_receiver  #Disconnects all three functions
```
