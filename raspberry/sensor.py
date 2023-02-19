'''
调试传感器使用
'''
import RPi.GPIO as GPIO
import time

SOUND_SENSOR = 22
LIGHT_SENSOR = 23
LED = 27
led_delay_time = 5

GPIO.setmode(GPIO.BCM) 
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SOUND_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIGHT_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def my_callback(SOUND_SENSOR):
    if(GPIO.input(LIGHT_SENSOR)==True):
        time.sleep(0.4)
        if(GPIO.input(LIGHT_SENSOR)==True):
            GPIO.output(LED,GPIO.HIGH)
            time.sleep(led_delay_time)
            GPIO.output(LED,GPIO.LOW)

GPIO.add_event_detect(SOUND_SENSOR, GPIO.RISING, callback=my_callback, bouncetime=500)    # 检测button的中断函数

if __name__ == '__main__':
    while(True):
        if(1 == 2):
            print(1)