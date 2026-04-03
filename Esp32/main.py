from machine import Pin
import time

led = Pin(2, Pin.OUT, value=0)                            
led2 = Pin(19,Pin.OUT, value=0)

led2.value(1)
print("蜂鸣器输出")
time.sleep(5)
led2.value(0)

while True:
    led.value(1)
    print("灯亮")
    time.sleep(5)
    led.value(0)
    print("灯灭")
    time.sleep(2)