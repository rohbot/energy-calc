#import RPi.GPIO as GPIO
import time
from cyrusbus import Bus
from busclient import BusClient

BUTTON_EVENT = 'button'

class SwitchReader(BusClient):

    def __init__(self,LED_PIN = 13, SWITCH_PIN = 11, bus=Bus()):

        BusClient.__init__(self,bus)
        self.LED_PIN = LED_PIN
        self.SWITCH_PIN = SWITCH_PIN

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setwarnings(False)

        # GPIO.setup(self.SWITCH_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(self.LED_PIN, GPIO.OUT)  
        self.count = 0
        self.lastPressed = time.time()
        
        #super(SwitchThread, self, bus).__init__()
        
    def blink(self,delay):
        GPIO.output(self.LED_PIN,GPIO.HIGH)  
        time.sleep(delay)
        GPIO.output(self.LED_PIN,GPIO.LOW)  
        time.sleep(delay)

    
    def run(self):
        self.running = True
        for i in range(3):
            print 'blink'
            #self.blink(0.5)

        while self.running:
            #if True == False: # or GPIO.input(self.SWITCH_PIN) == False and not pressed and 
            if time.time() - self.lastPressed > 2:
                #GPIO.output(self.LED_PIN,GPIO.HIGH)
                self.count += 1  
                #socketio.emit('button', self.count, namespace='/blender')
                self.bus.publish(BUTTON_EVENT, self.count) 
                #redis.publish('button', '1')
                pressed = True
                self.lastPressed = time.time()
                #print time.time(), 'ON' , self.count
                
                time.sleep(1)


            else:
                pressed = False
                #GPIO.output(self.LED_PIN,GPIO.LOW)  

            
            time.sleep(0.1)

if __name__ == '__main__':
    switchThread = SwitchReader()
    switchThread.listen(BUTTON_EVENT)
    switchThread.run()
