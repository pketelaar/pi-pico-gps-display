from machine import Pin, UART, I2C
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import qrcode

from pimoroni import RGBLED

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()


BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)

led = RGBLED(6, 7, 8)
import utime, time
led.set_rgb(25, 25, 25)
gpsModule = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
print(gpsModule)

buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""
altitude = ""
altfeet = ""
alt2 = ""
speed = ""
cog = ""
cog2 = ""

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime, altitude, speed, cog
    
    timeout = time.time() + 8 
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
    
        if (parts[0] == "b'$GNGGA" and len(parts) == 15):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7] and parts[8] and parts [9]):
                print(buff)
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = longitude
                satellites = parts[7]
                altitude = parts[9]
                #altfeet = float(altitude)
                #alt2 = str(altfeet)
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
        
        if (parts[0] == "b'$GNRMC" and len(parts) == 13):
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7] and parts[8]):
                print(buff)
                
                
                speed = parts[7]
                cog = parts[8]
                FIX_STATUS = True
                break

        
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)
    
    
while True:
    
    getGPS(gpsModule)
    display.set_pen(BLACK)
    display.rectangle(1, 1, 100, 25)
    if(FIX_STATUS == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: "+latitude)
        print("Longitude: "+longitude)
        print("Satellites: " +satellites)
        print("altitude: " +altitude)
        print("Time: "+GPStime)
        print("speed "+speed)
        print("Course "+cog)
        print("----------------------")
        led.set_rgb(0, 25, 0)
        display.clear()        #display.set_pen(BLACK)
        #display.rectangle(1, 1, 100, 25)
        alt2 = round(float(altitude)*3.28)
        #cog2 = round(cog)
       # writes the reading as text in the white rectangle
        display.set_pen(WHITE)
        display.set_font("bitmap8")
        #display.text("GPS Found", 3, 3)
        display.text("Alt : "+str(alt2), 10, 0, scale=5)
        display.set_font("sans")

        display.text("Time : "+GPStime, 10, 70, scale=.75)
        display.text("Course:"+str(cog), 10, 110, scale =.5)
        display.text("Speed:"+speed, 140, 110, scale =.5)
        # time to update the display
        display.update()
        #display.set_pen(BLACK)
        #display.rectangle(1, 1, 100, 25)
        #display.update()
        # waits for 5 seconds
        #time.sleep(5)
             
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("No GPS data is found.")
        #display.set_pen(BLACK)
        #display.rectangle(1, 1, 100, 25)
        display.clear()
        display.set_pen(RED)
        display.set_font("sans")
        display.text("NO GPS", 60, 65, scale=1)
        
        w, h = display.get_bounds()
        display.line(1, 1, 235, 134)
        display.line(0, 134, 235, 0)
        led.set_rgb(50, 0, 0)

        # time to update the display
        display.update()
        #display.set_pen(BLACK)
        #display.rectangle(1, 1, 100, 25)
        display.update()
        TIMEOUT = False
    #display.set_pen(BLACK)
    #display.rectangle(1, 1, 100, 25)
    display.update()
