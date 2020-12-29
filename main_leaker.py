import os
from time import sleep
from threading import Thread

from protocol import data_to_raw, bmp_to_raw
from finding_file import find
from led_controller import Led_Controller


def main():
    led_controller = Led_Controller()
    lights = range(8)
    for light in lights:
        led_controller.turn_on(light)
    input("Press Enter to Turn lights off")
    root, files_to_transfer = find()
    print("Found files.", "Transferring", root + '\\' + files_to_transfer[0])
    for i in range(len(files_to_transfer)):
        arr = []
        if files_to_transfer[i][-4:] == ".bmp":
            arr = bmp_to_raw(root + '\\' + files_to_transfer[i], len(Led_Controller.PINS))
        elif files_to_transfer[i][-4:] == ".txt":
            arr = data_to_raw(root + '\\' + files_to_transfer[i], len(Led_Controller.PINS))
        led_controller.blinks(arr)
        if i < len(files_to_transfer) - 1:
            input("Press Enter to transfer: " + root + '\\' + files_to_transfer[i + 1])


if __name__ == '__main__':
    main()
