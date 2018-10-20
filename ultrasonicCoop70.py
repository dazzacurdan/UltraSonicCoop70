#!/usr/bin/python
#
#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#https://pimylifeup.com/raspberry-pi-distance-sensor/
#
#Libraries
import argparse
import RPi.GPIO as GPIO
import threading
from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
lock = threading.Lock() 
aStopEvent = threading.Event()
isPlaying = False
videoNumber = 0

class OSCVideoCommand(threading.Thread):
    
    def __init__(self,event,ip,port):
        threading.Thread.__init__(self)
        self.globalVideoPath = "/home/pi/media"
        parser_pc = argparse.ArgumentParser()
        parser_pc.add_argument("--ip", default=ip,
        help="The ip of the OSC server")
        parser_pc.add_argument("--port", type=int, default=port,
        help="The port the OSC server is listening on")
        args = parser_pc.parse_args()
        self.client = udp_client.SimpleUDPClient(args.ip, args.port)
        self.videoNumber = 0
        self.isPlaying = False
        self.stopEvent = event
    
    def videoPaths(self,x):
        return {
        0: [self.globalVideoPath+"/01-ZANUSO.mp4", 59 ],
        1: [self.globalVideoPath+"/02-ZANUSO.mp4", 53 ],
        2: [self.globalVideoPath+"/03-ZANUSO.mp4", 60 ],
        3: [self.globalVideoPath+"/04-ZANUSO.mp4", 67 ],
        4: [self.globalVideoPath+"/05-ZANUSO.mp4", 67 ],
        5: [self.globalVideoPath+"/06-ZANUSO.mp4", 80 ],
        6: [self.globalVideoPath+"/07-ZANUSO.mp4", 87 ],
        7: [self.globalVideoPath+"/08-ZANUSO.mp4", 59 ],
        8: [self.globalVideoPath+"/09-ZANUSO.mp4", 86 ],
        9: [self.globalVideoPath+"/10-ZANUSO.mp4", 52 ],
        }.get(x, [self.globalVideoPath+"/00.mp4", 10 ])
    
    def playingVideo(self):
        path = self.videoPaths(self.videoNumber)
        print ("/play: "+path[0])
        self.client.send_message("/play", path[0] )
        time.sleep(path[1])
        print ("/play: "+globalVideoPath+"/LOOP-B-Zanuso.mp4")
        client.send_message("/play", globalVideoPath+"/LOOP-B-Zanuso.mp4" )
        self.isPlaying = False
        self.videoNumber = (self.videoNumber+1)%10
        time.sleep(2)
        
    def run(self):
        global playVideo
        _playVideo = False
        while True:
            if(self.stopEvent.wait(0)):
                print (self.name+":Asked to stop")
                break;
            lock.acquire()
            try:
                _playVideo = playVideo
            finally:
                lock.release()

            if( _playVideo and (not self.isPlaying) ):
                self.isPlaying = True
                self.playingVideo()
        print (self.name+":Stopped")

class UltraSound(threading.Thread):
    
    def __init__(self,event,name,trigger,echo):
        threading.Thread.__init__(self)
        self.name = name
        ###GPIO
        self.gpioTrigger = trigger
        self.gpioEcho = echo
        ###PATH
        self.globalVideoPath = "/home/pi/media"
        ###OSC
        parser_pc = argparse.ArgumentParser()
        parser_pc.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
        parser_pc.add_argument("--port", type=int, default=9000,
        help="The port the OSC server is listening on")
        args = parser_pc.parse_args()
        self.client = udp_client.SimpleUDPClient(args.ip, args.port)
        self.stopEvent = event
        
        #lock.acquire()
        #try:
        #    print("init videoNumber: "+self.name)
        #    videoNumber = 0
        #finally:
        #    lock.release()
        time.sleep(2)
    
    def videoPaths(self,x):
        return {
        0: [self.globalVideoPath+"/01-ZANUSO.mp4", 10 ],
        1: [self.globalVideoPath+"/02-ZANUSO.mp4", 10 ],
        2: [self.globalVideoPath+"/03-ZANUSO.mp4", 60 ],
        3: [self.globalVideoPath+"/04-ZANUSO.mp4", 67 ],
        4: [self.globalVideoPath+"/05-ZANUSO.mp4", 67 ],
        5: [self.globalVideoPath+"/06-ZANUSO.mp4", 80 ],
        6: [self.globalVideoPath+"/07-ZANUSO.mp4", 87 ],
        7: [self.globalVideoPath+"/08-ZANUSO.mp4", 59 ],
        8: [self.globalVideoPath+"/09-ZANUSO.mp4", 86 ],
        9: [self.globalVideoPath+"/10-ZANUSO.mp4", 52 ],
        }.get(x, [self.globalVideoPath+"/LOOP.mp4", 10])

    def measureDistance(self):
        GPIO.output(self.gpioTrigger, False)                 #Set TRIG as LOW
        #print ("Waitng For Sensor To Settle")
        time.sleep(0.1)                            #Delay of 2 seconds

        GPIO.output(self.gpioTrigger, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(self.gpioTrigger, False)                 #Set TRIG as LOW

        pulse_start = time.time()
        pulse_end = time.time()

        while GPIO.input(self.gpioEcho)==0:               #Check whether the ECHO is LOW
            pulse_start = time.time()                      #Saves the last known time of LOW pulse

        while GPIO.input(self.gpioEcho)==1:               #Check whether the ECHO is HIGH
            pulse_end = time.time()                #Saves the last known time of HIGH pulse 

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2) - 0.5           #Round to two decimal points
        return distance

    def playVideo(self):
        global videoNumber
        lock.acquire()
        try:
            path = self.videoPaths(videoNumber)
        finally:
            lock.release()
        print ("/play: "+path[0])
        self.client.send_message("/play", path[0] )
        time.sleep(path[1])
        
        lock.acquire()
        try:
            path = self.videoPaths(10)
            print ("/play: "+path[0])
            self.client.send_message("/play", path[0] )
            videoNumber = (videoNumber+1)%10
        finally:
            lock.release()
        time.sleep(2)

    def run(self):
        th=30
        pulse_start=time.time()
        pulse_end=time.time()
        GPIO.setup(self.gpioTrigger, GPIO.OUT)
        GPIO.setup(self.gpioEcho, GPIO.IN)
        
        global isPlaying
        
        print("UltraSound "+self.name+" ready on port "+str(self.gpioTrigger)+" "+str(self.gpioEcho))
        
        while True:
            if(self.stopEvent.wait(0)):
                print (self.name+":Asked to stop")
                break;
            distance = self.measureDistance()
            #print (self.name+" distance: "+str(distance)+" cm "+str(th))
            if ((not isPlaying) and distance > 2 and distance < th):
                lock.acquire()
                try:
                    print("Play: "+self.name)
                    isPlaying = True
                finally:
                    lock.release()
                
                self.playVideo()

                lock.acquire()
                try:
                    print("lock released")
                    isPlaying = False
                finally:
                    lock.release()

        print (self.name+":Stopped")


 
if __name__ == '__main__':
    #osc = OSCVideoCommand(aStopEvent,"127.0.0.1",9000)
    #osc.start()
    myInstances = []
    myClasses = {
        "myObj01": [aStopEvent,"a",23,24],
        "myObj02": [aStopEvent,"b",27,22],
        #"myObj03": [aStopEvent,"c",23,24],
        }
    
    myInstances = [UltraSound(myClasses[thisClass][0],myClasses[thisClass][1],myClasses[thisClass][2],myClasses[thisClass][3]) for thisClass in myClasses.keys()]
    
    for thisObj in myInstances:
        thisObj.start()

    try:
        while True :
            time.sleep(0.1)
            # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        aStopEvent.set()
        for thisObj in myInstances:
            thisObj.join()
        #osc.join()
        GPIO.cleanup()