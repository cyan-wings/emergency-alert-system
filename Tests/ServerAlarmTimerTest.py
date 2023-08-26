import socketio

sio = socketio.Client()

ip = '0.0.0.0' #input('Enter Server IP Address: ')
port = '8080' #input('Enter Server Port Number: ')
    
sio.connect('http://'+ip+':'+port) 

@sio.on('alarm_action_timer')
def alarm_duration_test(data):
    try:
        if data['status'] == 'enable' and data['timer'] == 1000:
            print("pass test")
            sio.disconnect()
        else:
            print("fail test")
            sio.disconnect()
        
    except TypeError:
        print("fail test")
        sio.disconnect()
         
if __name__ == "__main__":
    # This script serve as unit test for the alarm_duration_function of Server.py
    # This is to ensure that the server will send back a dictionery instead of a string
    # This is also to ensure the duration received by app is correct 

    sio.emit('duration', {'status':'enable','timer':1000})
    
