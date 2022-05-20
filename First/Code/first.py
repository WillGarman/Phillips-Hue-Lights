from turtle import color
from phue import Bridge
from decouple import config
import time

#https://github.com/studioimaginaire/ph

bridge_ip_address = config('bridge_ip_address') #get ip from .env file


def connectToLights(bridge_ip_address):
    b = Bridge(bridge_ip_address)

    #b.connect() #only run first time to connect to bridge 
    #print('Connected')
    lights = b.lights #get all light objects
    return lights

def rgb_to_xy(red, green, blue):
    """ conversion of RGB colors to CIE1931 XY colors
    Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
    Args: 
        red (float): a number between 0.0 and 1.0 representing red in the RGB space
        green (float): a number between 0.0 and 1.0 representing green in the RGB space
        blue (float): a number between 0.0 and 1.0 representing blue in the RGB space
    Returns:
        xy (list): x and y
    """
    red = float(round(red/255, 3)) #convert regular RGB values to range of 0.0 - 1.0
    green = float(round(green/255, 3))
    blue = float(round(blue/255, 3))


    # gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

    # convert rgb to xyz
    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    # convert xyz to xy
    x = x / (x + y + z)
    y = y / (x + y + z)

    # TODO check color gamut if known
     
    return [x, y]

def turnLightsOff(lights):
    for light in lights:
        light.on = False
        
def turnLightsOn(lights, xy, brightness, transitionTime):
    for light in lights:
            light.on = True
            #light.hue = hue
            light.xy = xy
            #light.saturation = saturation
            light.brightness = brightness
            light.transitiontime = transitionTime

def flashLights(lights, colors):
    while(True):
        for color in colors:
            time.sleep(.1)
            turnLightsOn(lights, color, 100, 0)
            turnLightsOff(lights)
            

#Select colors using RGB -> https://colorpicker.me/

color1 = rgb_to_xy(196, 0, 240)
color2 = rgb_to_xy(240, 0, 0)
color3 = rgb_to_xy(15, 255, 0)
color4 = rgb_to_xy(240, 220, 226)
colorList = [color1, color2, color3, color4]

flashLights(connectToLights(bridge_ip_address), colorList)
    