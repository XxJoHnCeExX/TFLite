######## Webcam Object Detection Using Tensorflow-trained Classifier #########
# Author: Juan Carlos Raya

# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util

# Define variables
MODEL_NAME = 'TFLite_model'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
min_conf_threshold = 0.9
IM_DIR = 'Pics'

# Import TensorFlow libraries
# If tensorflow is not installed, import interpreter from tflite_runtime, else import from regular tensorflow
pkg = importlib.util.find_spec('tensorflow')
if pkg is None:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

# Get path to current working directory 
CWD_PATH = os.getcwd()     # (/home/pi/TFLite)

# Define path to images, tflite file, and label map file and grab all image filenames
PATH_TO_IMAGES = os.path.join(CWD_PATH,IM_DIR) # (/home/pi/TFLite/Pics)
images = glob.glob(PATH_TO_IMAGES + '/*') # grab all images
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME) # (/home/pi/TFLite/Sample_TFLite_model/detect.tflite)
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME) # (/home/pi/TFLite/Sample_TFLite_model/labelmap.txt)

# Load the label map and read all labels
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]     # 300 pixels
width = input_details[0]['shape'][2]      # 300 pixels

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Create an array for storing detect objects and respective accuracy
objects = []

# Loop over every image and perform detection
print("Running object detection...")
for image_path in images:
    print(image_path[21:]) # Print image name
    
    # Load image and resize to expected shape [1xHxWx3]
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            accuracy = int(scores[i]*100) # Get accuracy from scores
            
            print("    Detected Item #" + str(i + 1))
            print("\tObject: " + object_name + ", Accuracy: " + str(accuracy))
            
            # Averaging the values
            isInList = False
            for k in range(len(objects)):
                if(str(object_name) == str(objects[k][0])):
                    isInList = True
                    print("Is already in list")
                    
            if(isInList == False):
                objects.append((object_name, int(scores[i]*100)))
                print("Not in list, adding now")
            
            # Writing to text file
            objects_file = open("objects.txt", "w")
            for item in objects:
                objects_file.write(str(item) + "\n")
            objects_file.close()
            

print(objects)

# Clean up
cv2.destroyAllWindows()

