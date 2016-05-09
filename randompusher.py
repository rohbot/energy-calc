from time import sleep
from cyrusbus import Bus
from busclient import BusClient
from random import random

RANDOM_EVENT = 'random'



class RandomPusher(BusClient):
    def __init__(self,bus=Bus()):
        BusClient.__init__(self,bus)
        self.delay = 1
        self.count = 0
        self.v2 = round(random() * 15,2) 

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print "Making random numbers"
        prev = 0
        while self.running:
            self.v2 += random() * -10 + 5
            if self.v2 < 0:
                self.v2 = 0 
            #if prev != v2:
            print 'reading', self.v2
            self.bus.publish(RANDOM_EVENT, {'y': round(self.v2,2), 'x':self.count})
            #socketio.emit('newnumber', {'y': self.v2, 'x':self.count}, namespace='/blender')
            self.count += 1
            sleep(self.delay)
            
    def reset(self):
        self.count = 0
        self.v2 = round(random() * 15,2)

            
    def run(self):
        self.running = True
        self.randomNumberGenerator()

if __name__ == '__main__':
    rp = RandomPusher()
    rp.listen(RANDOM_EVENT)
    rp.run()
