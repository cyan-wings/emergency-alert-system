import socketio

sio = socketio.Client()

ip = '0.0.0.0' #input('Enter Server IP Address: ')
port = '8080' #input('Enter Server Port Number: ')
    
sio.connect('http://'+ip+':'+port) 

events = ['False Alarm', 'Robbery', 'Fire', 'Cancel Event']
response = []
count = 0

@sio.on('event')
def event_test(data):
    global count 
    count += 1
    response.append(data)
    if count == 4:
        if events == response:
            print('test pass')
        else:
            print('test fail')
        sio.disconnect()
         
if __name__ == "__main__":
    # This script serve as unit test for the update_event function of Server.py
    # This is to ensure that the correct signal will be sent to the response team user interface

    for i in range(4):
        sio.emit('detected_event', events[i])