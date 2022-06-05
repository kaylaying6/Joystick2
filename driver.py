import time

import mouse
import serial

# Default joystick home position reading
joystick_home = [0, 0, False]

# Open a Serial communication to Arduino that has joystick
arduino_serial = serial.Serial(port="COM3", baudrate=9600)
# Wait for 1 second to make sure the serial communication to Arduino is up
time.sleep(1)

# Get the first read and throw the potential non-completed message
arduino_serial.readline()

# Home position calibration
cali_counter = 0
total_cmd_x = 0
total_cmd_y = 0
for _ in range(200):
    # Read a full sentence of message from Arduino
    data_raw = arduino_serial.readline()

    # Decode the raw message received from the Arduino
    data_decoded = str(data_raw.decode("ascii"))

    # Break down the full sentence of command to 3 elements
    data_breakdown = data_decoded.strip().split(" ")

    # Checking if we are able to get the three elements
    # Throw it if it is broken
    if len(data_breakdown) != 3:
        print("Got a incomplete message {data_breakdown=} from Arduino. Ignored.")
        continue
    cmd_x = int (data_breakdown[0])
    cmd_y = int(data_breakdown[1])

    # Update statistic datas
    cali_counter = cali_counter + 1
    total_cmd_x = total_cmd_x + cmd_x
    total_cmd_y = total_cmd_y + cmd_y

joystick_home[0] = int(total_cmd_x / cali_counter)
joystick_home[1] = (total_cmd_y / cali_counter)

print(
    f"Calibration of joystick home is completed."
      f" Received{cali_counter} valid message. home_x={joystick_home[0]},home_y={joystick_home[1]}"
)

start_time = time.time()

while time.time() - start_time < 5:
    # Read a full sentence of message from Arduino
    data_raw = arduino_serial.readline()

    # Decode the raw message received from the Arduino
    data_decoded = str(data_raw.decode("ascii"))

    # Break down the full sentence of command to 3 elements
    data_breakdown = data_decoded.strip().split(" ")

    # Checking if we are able to get the three elements
    # Throw it if it is broken
    if len(data_breakdown) != 3:
        print("Got a incomplete message {data_breakdown=} from Arduino. Ignored.")
        continue

    cmd_x = int(data_breakdown[0]) - joystick_home[0]
    cmd_y = int(data_breakdown[1]) - joystick_home[0]
    cmd_click = data_breakdown[2] == "0"

    # Execute the mouse commands
    # Got the current mouse position
    cur_x, cur_y = mouse.get_position()
    # Calculate the target mouse position
    target_x = cur_x + cmd_x * 0.01
    target_y = cur_y + cmd_y * 0.01
    # Move mouse to the target position
    mouse.move(target_x, target_y)

