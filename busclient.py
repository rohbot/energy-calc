from cyrusbus import Bus
import signal


KILL_EVENT = 'event.kill'

class BusClient():

	def __init__(self, bus = Bus()):
		self.bus = bus
		self.bus.subscribe(KILL_EVENT, self.kill)
		self.running = False
		
	def kill(self,signum, frame):
		print 'kill', signum, frame
		self.running = False

	def listen(self,eventName):
		self.bus.subscribe(eventName,self.printMsg)
		print 'Subscribed to ' + eventName

	def printMsg(self, *args, **kwargs):
		print args, kwargs		


        