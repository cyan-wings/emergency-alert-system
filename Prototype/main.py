"""

FIT 3140 Assignment 1

Author: Group 5(Matthew Yeow, Keong Jin, Chai Loon, Yee Wearn
Date modified: 20/1/2019
Preconditions:
    - A button has to be connected to pin "P8_19"
    - An LED has to be connected to pin "P8_13"
    - A buzzer has to be connected to pin "P9_42"
Description: This project uses a BeagleBoard microcontroller to output light or sound from an LED or buzzer based on a pattern for button inputs
"""

"""
Required libraries
"""
import Adafruit_BBIO.GPIO as GPIO
import time
        
def on(output_pin):
    """
    Description: Sets the pin to HIGH, where there would be current flow
    """
    GPIO.output(output_pin, GPIO.HIGH)

def off(output_pin):
    """
    Description: Sets the pin to LOW, where there would be no current flow
    """
    GPIO.output(output_pin, GPIO.LOW)
    
def intermittent(output_pin, delay_time):
    """
    Description: Sets the pin to HIGH then LOW, depending on the delay_time in seconds
    """
    on(output_pin)
    time.sleep(delay_time)
    off(output_pin)
    time.sleep(delay_time)
    
def intermittent_aux(output_pin, delay_time, input_pin):
    """
    Author: Matthew Yeow
    Description: Loops the intermittent state so that it becomes continuous. When input_pin is HIGH, loop breaks.
    """
    GPIO.add_event_detect(input_pin, GPIO.RISING, bouncetime=0)
    print(GPIO.event_detected(input_pin))
    while GPIO.event_detected(input_pin) == False:
        intermittent(output_pin, delay_time)
    GPIO.remove_event_detect(input_pin)
    
def button_press_count(input_pin, count):
    """
    Parameters:
        count = The initial number of count (set to 0)
    Description: When button is pressed once, a 5 second timer starts. Function returns the number times input_pin is HIGH during the 5 second timeout.
    Return: The number of button presses.
    """
    print("Press button once to start\n")
    GPIO.add_event_detect(input_pin, GPIO.RISING, bouncetime=0)
    while True:
        if GPIO.event_detected(input_pin) == True:
            count += 1
            print("Enter combination within 5 seconds")
            start_time = time.time()
            while time.time() - start_time < 5:
                if GPIO.event_detected(input_pin) == True:
                    count += 1
            break
    GPIO.remove_event_detect(input_pin)
    return count
            
def clean():
    GPIO.cleanup()
    

if __name__ == "__main__":
    clean()
    
    #Initiation of pins
    input_button = "P8_19"
    output_led = "P8_13"
    output_buzzer = "P9_42"
    
    GPIO.setup(input_button, GPIO.IN)
    GPIO.setup(output_led, GPIO.OUT)
    GPIO.setup(output_buzzer, GPIO.OUT)

    #Phase 1: Button count combination
    count = button_press_count(input_button, 0)
    print(count)

    #Phase 2: Output (LED and buzzer)
    if count == 1:
        #Default state
        on(output_led)
        off(output_buzzer)
        
    elif count == 2:
        #State 1: LED blink slow and buzzer is on.
        on(output_buzzer)
        intermittent_aux(output_led, 0.6, input_button)
        #Phase 3: Disabling the alarm or buzzer
        #Press within less than 3 seconds will off only the buzzer; pressing once more after will off the LED
        #Press and hold for 3 seconds will off both the LED and buzzer
        flag = True
        start_time = time.time()
        while time.time() - start_time < 3:
            intermittent(output_led, 0.6)
            if GPIO.input(input_button) == 0:
                flag = False
                break
        off(output_buzzer)
        if flag == False:
            #if while loop terminates before 3 seconds, LED continues blinking
            intermittent_aux(output_led, 0.6, input_button)
            
    elif count == 3:
        #State 2: LED blink fast and buzzer is on.
        on(output_buzzer)
        intermittent_aux(output_led, 0.1, input_button)
        #Phase 3: Disabling the alarm or buzzer
        #Press within less than 3 seconds will off only the buzzer; pressing once more after will off the LED
        #Press and hold for 3 seconds will off both the LED and buzzer
        flag = True
        start_time = time.time()
        while time.time() - start_time < 3:
            intermittent(output_led, 0.1)
            if GPIO.input(input_button) == 0:
                flag = False
                break
        off(output_buzzer)
        if flag == False:
            #if while loop terminates before 3 seconds, LED continues blinking
            intermittent_aux(output_led, 0.1, input_button)
