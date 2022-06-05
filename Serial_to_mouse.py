import time
import mouse


def move_mouse_5_secs(dir: str) -> None:
    #Local
    time_limit = 5  # seconds
    speed = 1
    #If dir
    if dir == "down":
        speed_x = 0
        speed_y = speed * 1
    elif dir == "up":
        speed_x = 0
        speed_y = speed * -1
    elif dir == "left":
        speed_x = speed * -1
        speed_y = 0
    elif dir == "right":
        speed_x = speed * 1
        speed_y = 0
    else:
        return

    # set up time to move mouse
    start_time = time.time()
    cur_time = time.time()

    while cur_time - start_time < time_limit:
        # get the current mouse location
        cur_x, cur_y = mouse.get_position()

        # Calculate the target location
        target_x = cur_x + speed_x
        target_y = cur_y + speed_y

        # Control the mouse to move to the target location
        mouse.move(target_x, target_y)

        # Update the current time
        cur_time = time.time()
        time.sleep(0.01)

#Move mouse sqaure
move_mouse_5_secs(dir="down")
move_mouse_5_secs(dir="left")
move_mouse_5_secs(dir="up")
move_mouse_5_secs(dir="right")
mouse.click(button="left")
print("Mouse controlling stopped.")
