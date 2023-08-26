import Adafruit_BBIO.GPIO as GPIO
import time

#For LED blinking
def blink(out_pin, delay_time):
    GPIO.output(out_pin, GPIO.HIGH)
    time.sleep(delay_time)
    GPIO.output(out_pin, GPIO.LOW)
    time.sleep(delay_time)
    

#For LED to turn off
def light_off(output_pin):
    GPIO.output(output_pin, GPIO.LOW)

#Notify user when the system is ready
#After 5 seconds, it would not detect button pressing
#Count of press will increase by one when it detect the button pressed once 
def check_press(channel):
    global countOfPress
    print("Please  press the button")
    GPIO.add_event_detect(inputPin, GPIO.RISING, bouncetime=450)
    start = time.time()
    while time.time() - start < 6:
        if GPIO.event_detected(inputPin) == True:
            countOfPress=countOfPress+1
            print(countOfPress)
    GPIO.remove_event_detect(channel)
    
   

if __name__ == "__main__":
    inputPin = "P8_19"
    outputPin = "P8_13"
    countOfPress = 0
    count=[]
    
    GPIO.setup(inputPin, GPIO.IN)
    GPIO.setup(outputPin, GPIO.OUT)
    
    check_press(inputPin)
   
    while True:
         # blink slow when press twice
         # after 5 seconds press twice to off the LED
        if countOfPress == 2:
            blink(outputPin,0.7)
            if GPIO.input(inputPin)==1:
               count.append(1)
            if len(count)==2:
                light_off(outputPin)
                break
       
      
        # blink fast when press thrice
        # after 5 seconds press twice to off the LED
        elif countOfPress == 3:
            blink(outputPin,0.3)  
                if GPIO.input(inputPin)==1:
               count.append(1)
            if len(count)==2:
                light_off(outputPin)
                break
            
     
