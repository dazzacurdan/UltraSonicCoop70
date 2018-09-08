	
#Libraries
import RPi.GPIO as GPIO
from threading import Thread
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 

class UltraSound:
    def __init__(self),name,trigger,echo:
        self.name = name
        self.gpioTrigger = trigger
        self.gpioEcho = echo
        GPIO.setup(self.gpioTrigger, GPIO.OUT)
        GPIO.setup(self.gpioEcho, GPIO.IN)
        Thread.__init__(distance)
        time.sleep(2)
        print "UltraSound "+name+" ready"

    def distance():
        while True:
            # set Trigger to HIGH
            GPIO.output(self.gpioTrigger, True)
        
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(self.gpioTrigger, False)
        
            StartTime = time.time()
            StopTime = time.time()
        
            # save StartTime
            while GPIO.input(self.gpioEcho) == 0:
                StartTime = time.time()
        
            # save time of arrival
            while GPIO.input(self.gpioEcho) == 1:
                StopTime = time.time()
        
            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            print ("Measured Distance = %.1f cm" % distance)
            time.sleep(1)
 
if __name__ == '__main__':
    ultraSound1 = UltraSound("#1",7,11)
    try:
        ultraSound1.start()
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        ultraSound1.stop()
        GPIO.cleanup()