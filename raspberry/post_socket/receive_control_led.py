# 按键按下后将数据传给云端

import RPi.GPIO as GPIO
import socket
import sys
import time

HOST = '124.223.76.58'  # 比如 99.100.101.102是你的服务器的公网IP
PORT = 7789  # IP开放的socket端口
BUFSIZ = 1024
ADDR = (HOST, PORT)
led_delay_time = 5

turn_on  =  1
turn_off =  0
RECEICVE_status = turn_off

GPIO.setmode(GPIO.BCM) 
LED = 27
GPIO.setup(LED, GPIO.OUT)
channel = 17
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(LED,GPIO.LOW)

def my_callback(channel):
    data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  raspberry'
    print('按键按下')
    # print('Edge detected on channel %s'%channel)
    s.send(data.encode('utf-8'))

    GPIO.output(LED,GPIO.HIGH)
    time.sleep(led_delay_time)
    GPIO.output(LED,GPIO.LOW)

GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=400)


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    while(1):
        RECEICVE_status = int(s.recv(BUFSIZ).decode('utf-8'))
        if(RECEICVE_status == turn_on ):
            GPIO.output(LED,GPIO.HIGH)
            RECEICVE_status = turn_off
            time.sleep(led_delay_time)
            GPIO.output(LED,GPIO.LOW)