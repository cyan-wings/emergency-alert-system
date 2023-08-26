import socketio

sio = socketio.Client()

ip = '0.0.0.0' #input('Enter Server IP Address: ')
port = '8080' #input('Enter Server Port Number: ')
    
sio.connect('http://'+ip+':'+port) 

ins = ['enable', 'disable']
response = []
count = 0

@sio.on('alarm_action')
def alarm_function(data):
    global count 
    count += 1
    response.append(data)
    if count == 2:
        if ins == response:
            print('test pass')
        else:
            print('test fail')
        sio.disconnect()
         
if __name__ == "__main__":
    # This script serve as unit test for the alarm_function of Server.py
    # This is to ensure that the correct signal will be sent to the app

    for i in range(2):
        sio.emit('alarm', ins[i])
