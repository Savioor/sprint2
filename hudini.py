from led_controller import Led_Controller
import time

led_controller = Led_Controller()

while True:
    x = input()
    if 0 < input < 9:
        led_controller.turn_on(x - 1)
        time.sleep(2)
        led_controller.turn_off(x - 1)
    elif x == 9:
        led_controller.turn_on(7)
        led_controller.turn_on(0)
        time.sleep(2)
        led_controller.turn_off(7)
        led_controller.turn_off(0)
    elif x == 0:
        for i in range(8):
            led_controller.turn_on(i)
        time.sleep(2)
        for i in range(8):
            led_controller.turn_off(i)