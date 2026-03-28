from machine import Pin
import time

led = Pin(2, Pin.OUT)                            # 板载 LED

while True:
    led.value(1)
    print("灯亮")
    time.sleep(1)
    led.value(0)
    print("灯灭")
    time.sleep(1)
