# List of Simulation Commands
# Author: Juan Raya 815538874
# SDSU Spring 2020 Senior Design Team #59 (Kaladesh) 

# 1. Move into Project Folder
cd TFLite

# 2. Run Servo Python Script to take Pictures
python3 TakePics.py

# 3. Run TensorFlow Lite on Images and Write to objects.txt file
python3 detect.py

# 4. Send Information to Arduino Uno/Mega
python3 UART.py 