from time import sleep
from cyrusbus import Bus
from busclient import BusClient
import Adafruit_ADS1x15

ADC_EVENT = 'adc'



class ADCReader(BusClient):
    def __init__(self,bus=Bus()):
        BusClient.__init__(self,bus)
       
   
            
    def run(self):
        self.running = True
        self.randomNumberGenerator()

if __name__ == '__main__':
    ar = ADCReader()
    ar.listen(ADC_EVENT)
    ar.run()
