import sys
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

def videoGPIO(x):
    return {
       0: [12, 5 ],
       1: [23, 24 ],
       2: [27, 22 ],
       3: [4, 17 ],
       4: [6, 13 ],
       5: [26, 16 ],
    }.get(x, [0, 0 ])

print ("Distance measurement in progress")
ultrasonicID=1
if len(sys.argv) > 1:
  ultrasonicID=sys.argv[1]
gpio = videoGPIO(int(ultrasonicID))

print("TRIG: "+str(gpio[0])+" ECHO: "+str(gpio[1]))
GPIO.setup(gpio[0],GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(gpio[1],GPIO.IN)                   #Set pin as GPIO in

try:
  pulse_start = time.time()
  pulse_end = time.time()
  while True:
      GPIO.output(gpio[0], False)                 #Set TRIG as LOW
      print ("Waitng For Sensor To Settle")
      time.sleep(0.5)                            #Delay of 2 seconds

      GPIO.output(gpio[0], True)                  #Set TRIG as HIGH
      time.sleep(0.00001)                      #Delay of 0.00001 seconds
      GPIO.output(gpio[0], False)                 #Set TRIG as LOW

      while GPIO.input(gpio[1])==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse

      while GPIO.input(gpio[1])==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse 

      pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

      distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
      distance = round(distance, 2)            #Round to two decimal points
      
      if distance > 2 and distance < 400:      #Check whether the distance is within range
        print ("Distance:",distance - 0.5,"cm")  #Print distance with 0.5 cm calibration
      else:
        print ("Out Of Range")
except KeyboardInterrupt:
  print("Reset GPIO settings")
  GPIO.cleanup()