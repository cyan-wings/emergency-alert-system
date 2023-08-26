"""
FIT 3140 Assignment 3
Author: Chai Loon, Keong Jin, Matthew Yeow
Date modified: 28/1/2019
Preconditions:
    - A button has to be connected to pin "P8_17".
    - An LED has to be connected to pin "P8_11"
    - A buzzer has to be connected to pin "P9_42"
Description: This project uses a Beaglebone Black microcontroller to output light or sound from an LED or buzzer based on a 
             pattern for button inputs and client's decision.
"""

"""
Required libraries
"""
import socketio
import Adafruit_BBIO.GPIO as GPIO
import time

"""
Initiate client
"""
sio = socketio.Client()

"""
Global Variables:
    alarm_flag: Use to control the ring of alarm.When alarm_flag is false, the alarm will stop ring and vice versa.
    button_flag: Use to check whether app site or client site start to emit messages after the system is initiated.
                 When the button_flag is False, client site emit messages after the system is initiated.
"""
alarm_flag = True
button_flag = True


###########
# Functions ##
###########
def on(output_pin):
    """
    Description: Sets the pin to HIGH, where there would be current flow
    """
    GPIO.output(output_pin, GPIO.HIGH)
    
def off(output_pin):
    """
    Description: Sets the pin to LOW, where there would be no current flow.
    """
    GPIO.output(output_pin, GPIO.LOW)

@sio.on('connect')
def on_connect():
    """
    Description: Register an event handler to print connected client with decorator.
    """
    print('connection established')
    
@sio.on('disconnect')
def on_disconnect():
    """
    Description: Register an event handler to print disconnected client with decorator.
    """
    print('disconnected from server')
	
    
def intermittent(output_pin, delay_time):
    """
    Description: Sets the pin to HIGH then LOW, depending on the delay_time in seconds for the alarm to ring.
    """
    on(output_pin)
    time.sleep(delay_time)
    off(output_pin)
    time.sleep(delay_time)
    
def intermittent_aux(output_pin, delay_time, input_pin):
    """
    Author: Matthew Yeow
    Description: Loops the intermittent state so that it becomes continuous. When input_pin is HIGH, loop breaks.
        The app also send the messages to server for updating the status of alarm in client's webpage.
    Variable:
        alarm_flag: Use as a key to enable or disable alarm. 
    """
    global alarm_flag
    GPIO.add_event_detect(input_pin, GPIO.RISING, bouncetime=0)
    print(GPIO.event_detected(input_pin))
    while GPIO.event_detected(input_pin) == False:
        if alarm_flag == True:
            intermittent(output_pin, delay_time)
            sio.emit('alarm_status_update','Enabled')
        else:
            sio.emit('alarm_status_update','Disabled')
            break
    GPIO.remove_event_detect(input_pin)

def alarm_reaction(output_pin, delay_time, input_pin):
    """
    Author: Matthew Yeow
    Description: Function rings the alarm and checks the long press or short press of button for cancel event or disbale alarm and send messages to server.
        Press within less than 3 seconds will off the alarm. Press and hold for 3 seconds will off both the L.E.D and buzzer.
        The app also send the messages to server for updating the status of alarm and event in client's webpage.
    Variable:
        flag: Use as a key to check the button is press within 3 seconds or press and hold for 3 seconds.
    """
    intermittent_aux(output_pin,delay_time, input_pin)
    flag = True
    start_time = time.time()
    while time.time() - start_time < 3:
        intermittent(output_pin,delay_time)
        if GPIO.input(input_pin) == 0:
            sio.emit('alarm_status_update','Disabled')
            flag = False
            break
    off(output_pin)
    if flag == True:
        sio.emit('alarm_status_update','Disabled')
        sio.emit('detected_event','Cancel Event')

@sio.on('alarm_action')
def alarm_function(data):
    """
    Author: Chai Loon
    Description: Register an event handler to look for the 'alarm_action' event from server and use the data to enable or disable alarm with decorator.
        The app also send the messages to server for updating the status of alarm in client's webpage.
    Variables:
        alarm_flag: Use as a key to enable or disable alarm.
        button_flag: Use as a key to know the client site or the app site start to emit messages after the system initiated.
    """
    global alarm_flag
    global button_flag
    button_flag = False
    if data == 'enable':
        alarm_flag = True
        sio.emit('alarm_status_update','Enabled')
        GPIO.remove_event_detect(input_button)
        GPIO.add_event_detect(input_button, GPIO.RISING, bouncetime=0)
        while GPIO.input(input_button) == 0:
            intermittent(output_buzzer, 0.1)
            if alarm_flag == False:
                sio.emit('alarm_status_update','Disabled')
                break
        sio.emit('alarm_status_update','Disabled')
        alarm_flag=True
    elif data == 'disable':
        alarm_flag = False

@sio.on('alarm_action_timer')
def alarm_timer_function(data):
    """
    Author: Chai Loon
    Description: Register an event handler to look for the 'alarm_action_timer' event from server with decorator.Use the 
        alarm status data to enable or disable alarm and alarm timer data to enable alarm within the time limit of 
        client's input. The app also send the messages to server for updating the status of alarm in client's webpage.
    Variables:
        alarm_flag: Use as a key to enable or disable alarm.
        button_flag: Use as a key to know the client site or the app site start to emit messages after the system initiated.
    """
    global alarm_flag
    global button_flag
    button_flag = False
    alarm_status=data['status']
    alarm_timer=int(data['timer'])
    if alarm_status =='enable':
        alarm_flag=True
        time.sleep(1)
        start=time.time()
        while time.time()-start <= alarm_timer:
            intermittent(output_buzzer,0.1)
            if alarm_flag==False:
                break
            elif GPIO.input(input_button)==1:
                break
        sio.emit('alarm_status_update','Stop')
        alarm_flag=True

@sio.on('safe_action')
def safe_function(data):
    """
    Author: Chai Loon
    Description: Register an event handler to look for the 'safe_action' event from server and use the data to lock or unlock safe
        with decorator. When the safe is locked, the L.E.D light up and vice versa.The app also send the messages to server 
        for updating the status of safe in client's webpage.
    """
    if data == 'lock':
        on(output_led)
        sio.emit('safe_status_update','Locked')
        
    elif data =='unlock':
        off(output_led)
        sio.emit('safe_status_update','Unlocked')

###########
###########
        
if __name__ =="__main__":
    # Setup
    input_button = "P8_17"
    output_led = "P8_11"
    output_buzzer = "P9_42"
    
    GPIO.setup(input_button, GPIO.IN)
    GPIO.setup(output_led, GPIO.OUT)
    GPIO.setup(output_buzzer, GPIO.OUT)
    
    ip = input('Enter Server IP Address: ')
    port = input('Enter Server Port Number: ')
    
    sio.connect('http://'+ip+':'+port) 
    
    print("System initiated")

    print("Press button once to start\n")
    # var count: Count number of button presses within 5 seconds.
    count = 0
    GPIO.add_event_detect(input_button, GPIO.RISING, bouncetime=0)
    while button_flag == True:
        if GPIO.event_detected(input_button) == True:
            button_flag=True
            count += 1
            print("Enter combination within 5 seconds")
            start_time = time.time()
            while time.time() - start_time < 5:
                if GPIO.event_detected(input_button) == True:
                    button_flag=True
                    count += 1
            break
    GPIO.remove_event_detect(input_button)
    
    print(count)
    
    # Send messages to server when the button on the app is pressed.
    # Call the function to enable alarm when the button is pressed twice or thrice.
    
    if count == 1:
        sio.emit('detected_event','False Alarm')
        
    elif count == 2:
        sio.emit('detected_event', 'Robbery')
        alarm_reaction(output_buzzer, 0.1, input_button)
            
    elif count == 3:
        sio.emit('detected_event', 'Fire')
        alarm_reaction(output_buzzer, 0.1, input_button)

  
