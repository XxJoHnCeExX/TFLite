import RPi.GPIO as GPIO
import time
import picamera

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7,GPIO.OUT)     #pin 7 as GPIO output
GPIO.setup(11, GPIO.OUT)   #pin 11 as GPIO output

h = GPIO.PWM(7,50)    #pin 7: horizontal servo running at 50 Hz
v = GPIO.PWM(11,50)   #pin 11: vertical servo running at 50 Hz
h.start(7.5)          #default: straight
v.start(6)          #default: straight

#PWM -> Degree:
#Horizontal Servo: 12.5 = 0 (left), 10 = 45, 7.5 = 90 (straight), 5 = 135, 2.5 = 180 (right)
#Vertical Servo: 7 (low), 6 (medium), 4.5 (high)
horizontal = [12.5, 10, 7.5, 5, 2.5]
vertical = [7, 6, 4.5]
pic_index = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [9, 10, 11],
    [12, 13, 14]
]

print("Taking pictures...")

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (300,300) 
        time.sleep(3)
        for x in range (0, 5):
            h.ChangeDutyCycle(horizontal[x])
            for y in range (0,3):
                v.ChangeDutyCycle(vertical[y])
                time.sleep(2)
                camera.capture("/home/pi/Servo/Pics/image" + str(pic_index[x][y]) + ".jpg")
                print("Picture " + str(pic_index[x][y]) + " taken.")
                time.sleep(3)
                
        h.ChangeDutyCycle(7.5)       #default
        v.ChangeDutyCycle(6)
        time.sleep(2)
    
    print("Pictures taken.")


except KeyboardInterrupt:
    GPIO.cleanup()
    print("Error occured.")

h.stop()
v.stop()
GPIO.cleanup()