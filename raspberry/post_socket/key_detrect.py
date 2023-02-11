import RPi.GPIO as GPIO
import socket
import sys
import time

HOST = '124.223.76.58'  # 比如 99.100.101.102是你的服务器的公网IP
PORT = 7789  # IP开放的socket端口
BUFSIZ = 1024
ADDR = (HOST, PORT)

GPIO.setmode(GPIO.BCM) 
channel = 17
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(channel):
    print('Input was HIGH')
else:
    print('Input was LOW')


def my_callback(channel):
    data = 'hello' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)
    s.send(data.encode('utf-8'))

GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=400)

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    while(1):
        if(1==2):
            print(1)