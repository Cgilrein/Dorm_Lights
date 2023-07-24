# Developer: Cameron Gilrein
# Dorm lights designed to be easily adaptable for different amount of lights 
# Uses a high-low button with GPIO pins, logic high when not activated and low when pressed

import board
import neopixel
import time
import RPi.GPIO as GPIO
import random
import threading
import logging
### Constant Variables ###
# Change depending on amount of lights and wiring

num_pixels = 50
button_GPIO = 17
encoder_GPIO = 19
light_GPIO = 21
colors = [(255,0,0),(0,255,0),(0,0,255)] # List of colors cycled through, (R,B,G) values

amt_colors = len(colors) - 1  # Used for cycling colors
curent_color = 0 # Used for cycling colors

### Initialize Lights to be Off ###

pixels = neopixel.NeoPixel(board.D21,num_pixels)  # Need to test how to update this based on light pin
pixels.fill((0,0,0))  # Make sure all lights begin off

light_bool = False   # Lights start off

### Setting Standard GPIO mode for RPI ###

GPIO.setmode(GPIO.BCM)

### Functions ###

def toggleLights():  
    # Switch lights to either on or off, depending on previous state of lights
    if light_bool is False:
        light_bool = True
        for i in range(num_pixels):  # Activate lights
            time.sleep(0.01)
            pixels[i] = (curent_color)
    else:
        light_bool = False
        pixel_reverse = num_pixels - 1
        for i in range(num_pixels):
            time.sleep(0.01)
            pixels[pixel_reverse] = ((0,0,0))
            pixel_reverse -= 1 # Deactivate lights

def switchLightColor():
    if current_color > amt_colors:
        current_color = 0
    pixels.fill((current_color))   # Fill pixels with current color
    current_color += 1  # Increment current color

##########################################################
##########################################################

# Threads

def thread_OnOff(name):
    logging.info("Thread %s: starting", name)

    previousReading_button = 1
    while True:

        time.sleep(0.01)
        current = GPIO.input(button_GPIO)  # Take reading of button at current moment
        if current != previousReading_button:
            toggleLights()
            print("Lights Toogled")
        else:
            pass
        # Set up next loop
        previousReading_button = current

def thread_Color(name):
    logging.info("Thread %s: starting", name)

    previousReading_encoder = 1
    while True:

        time.sleep(0.01)
        current = GPIO.input(encoder_GPIO)  # Take reading of button at current moment
        if current != previousReading_encoder:
            switchLightColor()
            print("Color Switched")
        else:
            pass
        # Set up next loop
        previousReading_encoder = current

##########################################################
##########################################################

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = []
    on_off_Thread = threading.Thread(target=thread_OnOff, args=("on/off",))
    color_Thread = threading.Thread(target=thread_Color, args=("color",))
    threads.append(on_off_Thread)
    threads.append(color_Thread)

    on_off_Thread.start()
    color_Thread.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
