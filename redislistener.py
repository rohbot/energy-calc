from time import sleep
from cyrusbus import Bus
from busclient import BusClient
import redis

REDIS_EVENT = 'redis'
REDIS_CHANNEL = 'socketio'


class RedisListener(BusClient):
    def __init__(self,bus=Bus()):
        BusClient.__init__(self,bus)
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(REDIS_CHANNEL)

    
    def work(self, item):
        #print item['data']
        try:
            tags = item['data'].split()
            self.bus.publish(REDIS_EVENT, item['data'])
        except:
            print 'bad tag:', item['data']
    def run(self):
        self.running = True
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)
            
 
if __name__ == '__main__':
    rl = RedisListener()
    rl.listen(REDIS_EVENT)
    rl.run()
