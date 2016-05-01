"""
Energy-Calculator

Aim is to create a webpage that displays energy consumed by a circuit in a real-time graph.

9th May 2016
"""

from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event
#import Adafruit_ADS1x15
import switchreader
import randompusher

ADC_NAMESPACE = '/adc'

RANDOM_NAMESPACE = '/random'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a34db408c9c0efd21fc0dd1a0901a9e8'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)
sr = switchreader.SwitchReader()
switch_thread = None

rp = randompusher.RandomPusher()
pusher_thread = None


def buttonPressed(bus,value):
	print 'buttonPressed', value
	socketio.emit('button', value, namespace=ADC_NAMESPACE)

def newData(bus,value):
	print 'incoming data', value
	socketio.emit('newnumber', value, namespace=ADC_NAMESPACE)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    global switch_thread
    if switch_thread is None:
        switch_thread = Thread(target=sr.run)
        switch_thread.start()
        sr.bus.subscribe(switchreader.BUTTON_EVENT,buttonPressed)
    
    global pusher_thread
    if pusher_thread is None:
        pusher_thread = Thread(target=rp.run)
        pusher_thread.start()
        rp.bus.subscribe(randompusher.RANDOM_EVENT,newData)


    return render_template('index.html',namespace=ADC_NAMESPACE)

@app.route('/blink')
def blink():
    sr.blink(1)
    return "watch me blink"



@socketio.on('connect', namespace=ADC_NAMESPACE)
def sio_connect():
    # need visibility of the global thread object
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.

@socketio.on('disconnect', namespace=ADC_NAMESPACE)
def sio_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8080)
