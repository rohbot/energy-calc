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
        self.current_list = []
        self.previous_time = time()
        self.voltage_list=[]

    	
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
            current_reading = (self.adc.read_adc(2,gain=1,data_rate=128)*0.000125)/10/0.01
            voltage_reading = (self.adc.read_adc(3,gain=1,data_rate=128)*0.000125)/10

            current_time = time()

            #    print current_time - previous_time
            if current_time - self.previous_time > 0.0001:
                self.previous_time = current_time


            if len(self.current_list) < 40:
                self.current_list.append(current_reading)

            # print current_list 
            else:
                averaged_current = sum(self.current_list)/40

                # print round(averaged_current,3)
                self.current_list = []
                self.current_list.insert(0,round(averaged_current,1))




            if len(self.voltage_list) < 40:
                self.voltage_list.append(voltage_reading)

            # print current_list
            else:
                averaged_voltage = sum(self.voltage_list)/40

            #print round(averaged_voltage*100,1),round(averaged_current,1)
                self.bus.publish(ADC_EVENT,{'current': round(averaged_current,1), 'voltage': round(averaged_voltage*100,1) , 'time': time() })
                self.voltage_list = []
                self.voltage_list.insert(0,round(averaged_voltage,1))

			
			#sleep(self.delay)


if __name__ == '__main__':
    ar = ADCReader()
    ar.listen(ADC_EVENT)
    ar.run()
