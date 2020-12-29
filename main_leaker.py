import os
from time import sleep
from threading import Thread

from protocol import data_to_raw
from finding_file import find
from led_controller import Led_Controller


def leak_txt_file(file_path):
    pass


def leak_bmp_file(file_path):
    pass


def leak_file():
    global is_processing
    file_path = input()
    while not os.path.isfile(file_path) and not file_path[:-4] not in (".txt", ".bmp"):
        print("Cannot open file.")
        file_path = input("Try Again:")
    wait_until_not_processing()
    is_processing = True
    if file_path[:-4] == ".txt":
        leak_txt_file(file_path)
    else:
        leak_bmp_file(file_path)
    is_processing = False


def main():
    lights = range(8)
    for light in lights:
        led_controller.turn_on(light)
    input("Press Enter to Turn lights off")
    root, files_to_transfer = find()
    print("Found files.", "Transferring", root + '\\' + files_to_transfer[0])
    for i in range(files_to_transfer):
        arr = data_to_raw(root + '\\' + files_to_transfer[i], len(Led_Controller.PINS))
        led_controller.blinks(arr)
        if i != 2:
            input("Press Enter to transfer: " + root + '\\' + files_to_transfer[i + 1])
