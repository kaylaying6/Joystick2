import time

import serial


arduino_serial = serial.Serial("COM3", baudrate=9600)
time.sleep(1) #Give it time to take break

while True:
    #Get the first da ta which might not be complete
    data = arduino_serial.readline()
    # Get the second read which should be complete
    data = arduino_serial.readline()
    data_proccesed = str(data.decode("ascii"))
    try:
        cmd_x, cmd_y, cmd_click = data_proccesed.strip().split(" ")
        cmd_x = int(cmd_x)
        cmd_y = int(cmd_y)
        cmd_click = int(cmd_click) == 0  # 0 is when joystick clicking
        print(cmd_x, cmd_y, cmd_click)
    except ValueError:
        continue