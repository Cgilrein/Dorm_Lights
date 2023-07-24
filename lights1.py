# Developer: Cameron Gilrein
# Dorm lights desgined to be easily adaptable for different amount of lights 
# Uses a high-low button with GPIO pins, logic high when not activated and low when pressed

import board
import neopixel
import time
import RPi.GPIO as GPIO
import random
import threading
### Constant Variables ###
# Change depending on amount of lights and wiring

num_pixels = 50
button_GPIO = 17
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

def special():
    pass

##########################################################
##########################################################

previous_reading = 1  # Start button at logic high

if __name__ == "__main__":

    try:
        while True:
            time.sleep(0.01)
            current = GPIO.input(button_GPIO)  # Take reading of button at current moment
            # Print useful info to terminal (For Debugging)
            print("Previous: " + str(previous_reading) + " | Current: "+ str(current) + " | Light Status: " + light_bool)
            if current != previous_reading:
                switchLightColor()
            elif current == 0 and previous_reading == 0:
                special()
            else:
                pass
    except:
            print("Error....Skipping")  # If theres an error simply restart cylce
