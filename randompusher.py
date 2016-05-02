from time import sleep, time
from busclient import BusClient
from random import random

RANDOM_EVENT = 'adc'



class RandomPusher(BusClient):
    def __init__(self, delay = 0.1, bus=None,):
        BusClient.__init__(self,bus)
        self.delay = delay
        self.count = 0
        self.v2 = round(random() * 2,2) 

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print "Making random numbers"
        prev = 0
        voltage = 2
        while self.running:
            self.v2 += random() * -10 + 5
            if self.v2 < 0:
                self.v2 = 0 
            #if prev != v2:
            #print 'reading', self.v2
            self.bus.publish(RANDOM_EVENT,{'current': round(self.v2,2), 'voltage': voltage , 'time': time() })

            #self.bus.publish(RANDOM_EVENT, {'current': round(self.v2,2), '':self.count})
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
