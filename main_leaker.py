import os
from time import sleep
from threading import Thread

from protocol import data_to_raw
from finding_file import find
from led_controller import Led_Controller

is_processing = False


def leak_from_usb():
    global is_processing
    led_controller = Led_Controller()
    arr = data_to_raw(find(), len(Led_Controller.PINS))
    wait_until_not_processing()
    is_processing = True
    led_controller.blinks(arr)
    is_processing = False


def wait_until_not_processing():
    global is_processing
    if is_processing:
        print("Other leak is already running, I am wa")
    while is_processing:
        sleep(0.01)


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
    print("Inset USB to leak it, input path of file to leak it")
    usb_leaker_thread = Thread(target=leak_from_usb)
    usb_leaker_thread.start()
    file_leaker_thread = Thread(target=leak_file)
    file_leaker_thread.start()
