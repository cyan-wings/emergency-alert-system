import socketio
import time

# initiate client
sio = socketio.Client()

@sio.on('test_signal_return1')
def cal_time(data):
    global count
    global begin

    count += 1
    if count == 4000:
        print('Time taken: ' + str(time.time() - begin))
        sio.disconnect()

@sio.on('test_signal_return2')
def cal_time(data):
    global count
    global begin

    count += 1
    if count == 4000:
        print('Time taken: ' + str(time.time() - begin))
        sio.disconnect()

@sio.on('test_signal_return3')
def cal_time(data):
    global count
    global begin

    count += 1
    if count == 4000:
        print('Time taken: ' + str(time.time() - begin))
        sio.disconnect()

@sio.on('test_signal_return4')
def cal_time(data):
    global count
    global begin

    count += 1
    if count == 4000:
        print('Time taken: ' + str(time.time() - begin))
        sio.disconnect()


if __name__ =="__main__":
    ip = input('Enter Server IP Address: ')
    port = input('Enter Server Port Number: ')
    
    sio.connect('http://'+str(ip)+':'+str(port)) 

    count = 0

    begin = time.time()
    for i in range(1000):
        sio.emit('test_signal1', 'test1')
        sio.emit('test_signal2', 'test2')
        sio.emit('test_signal3', 'test3')
        sio.emit('test_signal4', 'test4')

    
