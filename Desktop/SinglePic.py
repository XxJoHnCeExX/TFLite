import picamera

print("Taking single picture...")

with picamera.PiCamera() as camera:
    camera.resolution = (300,300)
    camera.brightness = 50
    camera.image_effect = 'none'
    camera.exposure_mode = 'nightpreview'
    camera.awb_mode = 'auto'
    camera.capture("/home/pi/TFLite/sample.jpg")

print("Picture taken.")



