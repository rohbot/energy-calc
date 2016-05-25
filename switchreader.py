import RPi.GPIO as GPIO
import time
from busclient import BusClient

BUTTON_EVENT = 'button'

class SwitchReader(BusClient):

    def __init__(self,LED_PIN = 13, SWITCH_PIN = 11, bus=None):

        BusClient.__init__(self,bus)
        self.LED_PIN = LED_PIN
        self.SWITCH_PIN = SWITCH_PIN

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.SWITCH_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_PIN, GPIO.OUT)  
        self.count = 0
        self.lastPressed = time.time()
        
        
    def blink(self,delay):
        self.blinking = 1
        self.blinkCounter = delay *  10  
                
        GPIO.output(self.LED_PIN,GPIO.HIGH)  
        time.sleep(delay)
        GPIO.output(self.LED_PIN,GPIO.LOW)  
        time.sleep(delay)

    
    def run(self):
        self.running = True
        for i in range(2):
            print 'blink'
            self.blink(0.5)

        while self.running:
            if GPIO.input(self.SWITCH_PIN) == False and time.time() - self.lastPressed > 1:
                GPIO.output(self.LED_PIN,GPIO.HIGH)
                self.count += 1  
                self.bus.publish(BUTTON_EVENT, self.count) 
                pressed = True
                self.lastPressed = time.time()
                #print time.time(), 'ON' , self.count
                
                time.sleep(1)


            else:
                pressed = False
                GPIO.output(self.LED_PIN,GPIO.LOW)

            if self.blinking == 1:
                print 'Blink'
                GPIO.output(self.LED_PIN,GPIO.HIGH)
                self.blinkCounter -= 1
                if self.blinkCounter < 1:
                    self.blinking = 0
                    GPIO.output(self.LED_PIN,GPIO.LOW)
                    print 'blink off'



            
            time.sleep(0.1)

if __name__ == '__main__':
    switchThread = SwitchReader()
    switchThread.listen(BUTTON_EVENT)
    switchThread.run()
