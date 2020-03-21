import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)    #pin 7 as GPIO output
GPIO.setup(11, GPIO.OUT)   #pin 11 as GPIO output

h = GPIO.PWM(7,50)    #pin 7: horizontal servo running at 50 Hz
v = GPIO.PWM(11,50)   #pin 11: vertical servo running at 50 Hz
h.start(7.5)          #default: straight
v.start(6)          #default: straight

#PWM -> Degree:
#Horizontal Servo: 12.5 = 0 (left), 10 = 45, 7.5 = 90 (straight), 5 = 135, 2.5 = 180 (right)
#Vertical Servo: 6.5 (low), 6 (medium), 4.5 (high)

print("Starting calibration...")

try:
    h.ChangeDutyCycle(7.5)
    v.ChangeDutyCycle(6)
    time.sleep(1)
    
    print("Calibration successful.")


except KeyboardInterrupt:
    GPIO.cleanup()
    print("Error occured.")

h.stop()
v.stop()
GPIO.cleanup()
