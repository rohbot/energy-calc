from time import sleep, time
from busclient import BusClient
import Adafruit_ADS1x15

ADC_EVENT = 'adc'


class ADCReader(BusClient):

    def __init__(self, gain=1, delay = 0.1, shuntValue = 0.01, opampGain = 3, bus=None):
    	BusClient.__init__(self,bus)
    	self.adc = Adafruit_ADS1x15.ADS1115()
    	self.delay = delay
    	self.setGain(gain)
    	self.shuntValue = shuntValue
    	self.opampGain = opampGain
    	
    def setGain(self,gain):
    	if gain == 2/3:
    		self.gain = 2/3
    		self.multiplier = 0.00001875
    	elif gain == 2:
    		self.gain = 2
    		self.multiplier = 0.00000625
    	elif gain == 4:
    		self.gain = 4
    		self.multiplier = 0.000003125
    	elif gain == 8:
    		self.gain = 8
    		self.multiplier = 0.0000015625
    	elif gain == 16:
    		self.gain = 16
    		self.multiplier = 0.00000078125			
    	else:
    		self.gain = 1
    		self.multiplier = 0.000125

             
    def run(self):
		self.running = True
		while self.running:
			voltage = 1	
			#current = (self.adc.read_adc(0, gain=self.gain) * self.multiplier) / self.opampGain / self.shuntValue
			current = self.adc.read_adc_difference(0, gain=self.gain)
			self.bus.publish(ADC_EVENT,{'current': round(current,3), 'voltage': voltage , 'time': time() })
			sleep(self.delay)


if __name__ == '__main__':
    ar = ADCReader()
    ar.listen(ADC_EVENT)
    ar.run()
