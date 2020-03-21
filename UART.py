import time
import serial

ser = serial.Serial('/dev/ttyAMA0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
time.sleep(1)

print ("STEP 3 OF 3: Sending data to Arduino...")

try:
    objects_file = open("objects.txt", "r")
    data = objects_file.readline()
    ser.write(data.encode())
    print ("Data sent successfully!\r\n")
    
except:
    print ("ERROR: Couldn't send message through UART.\r\n")
    
finally:
    ser.close()
    pass