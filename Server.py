import eventlet
import socketio
import time
import logging
import datetime

# Allocate Server to sio
sio = socketio.Server()

# Create a log for events and actions
logging.basicConfig(filename='panic.log',level=logging.DEBUG)

app = socketio.WSGIApp(sio, static_files={
    '/Client.js' : {'content_type': 'text/js', 'filename': 'Client.js'},
    '/styles.css' : {'content_type': 'text/css', 'filename': 'styles.css'},
    '/': {'content_type': 'text/html', 'filename': 'Client.html'}
})

def index(request):
    """Serve the client-side application."""
    with open('Client.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# print connected client
@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

#print disconnected client
@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)
    
# detect command (safe) from response team webpage and issue it to beaglebone app
@sio.on('safe')
def safe_function(sid, data):
    if data == 'lock':
        sio.emit('safe_action', 'lock')
    elif data == 'unlock':
        sio.emit('safe_action', 'unlock')
    logging.info(str(datetime.datetime.now()) + ' Response team ' + data + ' safe')

# receive status update (lock) from beaglebone app, and send to response team
@sio.on('safe_status_update')
def update_lock_status(sid, data):
    sio.emit('safe_status', data)

# detect command (alarm) from response team webpage and issue it to beaglebone app
@sio.on('alarm')
def alarm_function(sid, data):
    if data == 'enable':
        sio.emit('alarm_action', 'enable')
    elif data == 'disable':
        sio.emit('alarm_action', 'disable')
    logging.info(str(datetime.datetime.now()) + ' Response team ' + data + ' alarm')

# receive status update (alarm) from beaglebone app, and send to response team
@sio.on('alarm_status_update')
def update_alarm_status(sid, data):
    sio.emit('alarm_status', data)

# detect duration of the alarm from response team webpage and issue it to beaglebone app
@sio.on('duration')
def alarm_duration_function(sid,data):
    sio.emit('alarm_action_timer', {'status':data['status'],'timer':data['timer']})

# receive button event from beaglebone app, and send to response team
@sio.on('detected_event')
def update_event(sid, data):
    sio.emit('event', data)
    logging.info(str(datetime.datetime.now()) + ' Event Detected: ' + data)

#These four function is for Performance test
#use them with PerformanceTestA.py and PerformanceTtestB.py
"""
@sio.on('test_signal1')
def return_test(sid, data):
    sio.emit('test_signal_return1', 'test1')
    logging.info('test return 1')

@sio.on('test_signal2')
def return_test(sid, data):
    sio.emit('test_signal_return2', 'test2')
    logging.info('test return 2')

@sio.on('test_signal3')
def return_test(sid, data):
    sio.emit('test_signal_return3', 'test3')
    logging.info('test return 1')

@sio.on('test_signal4')
def return_test(sid, data):
    sio.emit('test_signal_return4', 'test4')
    logging.info('test return 4')
"""


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
