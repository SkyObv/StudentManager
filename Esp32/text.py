from machine import Pin
import time

led = Pin(18, Pin.OUT, value=0)

# 针脚测试
led.value(1)
time.sleep(3)
led.value(0)
