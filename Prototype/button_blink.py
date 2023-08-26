import Adafruit_BBIO.GPIO as GPIO
import time


def blink(out_pin, delay_time):
    # simple blink function
    GPIO.output(out_pin, GPIO.HIGH)
    time.sleep(delay_time)
    GPIO.output(out_pin, GPIO.LOW)
    time.sleep(delay_time)

def light_up(out_pin):
    # set LED to light up
    GPIO.output(out_pin, GPIO.HIGH)

def light_off(out_pin):
    # turn off LED
    GPIO.output(out_pin, GPIO.LOW)
    
def increase_count(cha):
    global press_count
    # press count will reset after every 4th press
    press_count = int((press_count + 1) % 4)


if __name__ == "__main__":
    input_pin = "P8_19"
    output_pin = "P8_13"
    
    GPIO.setup(input_pin, GPIO.IN)
    GPIO.setup(output_pin, GPIO.OUT)
    
    press_count = int(0)
    
    GPIO.add_event_detect(input_pin, GPIO.RISING, callback=increase_count)
    
    print("Initiation complete!")
     
    while True:
        # off light by default or press for the fourth time
        while press_count == 0:
            light_off(output_pin)
        
        # static light when press for the first time
        while press_count == 1:
            light_up(output_pin)
        
        # blink slow when press for teh second time    
        while press_count == 2:
            blink(output_pin, 0.6)
        
        # blink fast when press for the third time   
        while press_count == 3:
            blink(output_pin, 0.3)
