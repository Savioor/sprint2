import pyfirmata
import time
from protocol import data_to_raw
from finding_file import find


class Led_Controller(object):
    ON = 1
    OFF = 0
    PINS = [2, 3, 4, 5, 6, 7, 8, 9]
    ARDUINO_PORT = 'com3'
    BLINK_TIME = 0.2

    def __init__(self):
        #     self.__ser = serial.Serial('COM3', 9800, timeout=1)
        self.__board = pyfirmata.Arduino(Led_Controller.ARDUINO_PORT)

    def turn_on(self, light):
        #    self.__ser.port = self.ports[light - 1]
        # self.__ser.write(Led_Controller.ON)
        self.__board.digital[Led_Controller.PINS[light]].write(Led_Controller.ON)

    # print('on')

    def turn_off(self, light):
        #  self.__ser.port = self.ports[light - 1]
        # self.__ser.write(Led_Controller.OFF)
        self.__board.digital[Led_Controller.PINS[light]].write(Led_Controller.OFF)

    # print("off")

    def blink(self, lights):
        #       self.__ser.port = self.ports[light - 1]
        # print('blink')
        for light in lights:
            self.turn_on(light)
        time.sleep(Led_Controller.BLINK_TIME)
        for light in lights:
            self.turn_off(light)
#        time.sleep(Led_Controller.BLINK_TIME)

    def blinks(self, operations):
        for operation in operations:
            lights = []
            for i, light in enumerate(operation):
                if int(light) == Led_Controller.ON:
                    lights.append(i)
            self.blink(lights)



# led_controller = Led_Controller()
# lights = range(8)
# for light in lights:
#      led_controller.turn_on(light)
# arr = data_to_raw(find(), len(Led_Controller.PINS))
# print(arr)
# #  def __del__(self):
# # self.__ser.close()
# for light in lights:
#     led_controller.turn_on(light)
# led_controller.blinks(arr)

#print(data_to_raw(check_usb(), 8))
# lights = range(8)
# for light in lights:
#     led_controller.turn_on(light)
# time.sleep(5)
# for light in lights:
#     led_controller.turn_off(light)
# while True:
#     led_controller.blink(range(0, 8))
# while True:
# input()
# led_controller.turn_on(1)
# input()
# led_controller.turn_off(1)
# led_controller.blink(60,0, 1)
