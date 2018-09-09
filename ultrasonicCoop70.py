#!/usr/bin/python
#
#https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
#https://pimylifeup.com/raspberry-pi-distance-sensor/
#
#Libraries
import argparse
import RPi.GPIO as GPIO
from threading import Thread
from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
lock = threading.Lock() 

playVideo = False

class OSCVideoCommand:
    globalVideoPath = "/home/pi/media"
    def __init__(self,ip,port):
        parser_pc = argparse.ArgumentParser()
        parser_pc.add_argument("--ip", default=ip,
        help="The ip of the OSC server")
        parser_pc.add_argument("--port", type=int, default=port,
        help="The port the OSC server is listening on")
        args = parser_pc.parse_args()
        self.client = udp_client.SimpleUDPClient(args.ip, args_pc.port)
        self.videoNumber = 0
        self.isPlaying = False
        Thread.__init__(videoToPlay)

    def videoPaths(x):
        return {
        0: [globalVideoPath+"/01-ZANUSO.mp4", 59 ],
        1: [globalVideoPath+"/02-ZANUSO.mp4", 53 ],
        2: [globalVideoPath+"/03-ZANUSO.mp4", 60 ],
        3: [globalVideoPath+"/04-ZANUSO.mp4", 67 ],
        4: [globalVideoPath+"/05-ZANUSO.mp4", 67 ],
        5: [globalVideoPath+"/06-ZANUSO.mp4", 80 ],
        6: [globalVideoPath+"/07-ZANUSO.mp4", 87 ],
        7: [globalVideoPath+"/08-ZANUSO.mp4", 59 ],
        8: [globalVideoPath+"/09-ZANUSO.mp4", 86 ],
        9: [globalVideoPath+"/10-ZANUSO.mp4", 52 ],
        }.get(x, [globalVideoPath+"/00.mp4", 10 ])
    
    def playingVideo():
        path = videoPaths(self.videoNumber)
        self.client.send_message("/play", path[0] )
        time.sleep(path[1])
        client.send_message("/play", globalVideoPath+"/LOOP-B-Zanuso.mp4" )
        lock.acquire()
        self.isPlaying = False
        lock.stop()
    
    def videoToPlay():
        while True:
            lock.acquire()
            if( playVideo and (not self.isPlaying) ):
                self.isPlaying = True
                threading.Thread(target=playingVideo, args=(lock,path[1]), name='eventLockHolder').start()
            lock.release()

class UltraSound:
    th = 5 #cm
    def __init__(self,name,trigger,echo):
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
            distance = round(TimeElapsed * 17150, 2)
            print ("Measured Distance = %.1f cm" % distance)
            if (distance < self.th):
                lock.acquire()
                playVideo = True
                lock.release()
            time.sleep(1)
 
if __name__ == '__main__':
    ultraSound1 = UltraSound("#1",7,11)
    osc = OSCVideoCommand("192.168.1.3",9000)
    ultraSound1.start()
    osc.start()
    
    try:
        while True :
        time.sleep(0.1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        ultraSound1.stop()
        osc.stop()
        GPIO.cleanup()