"""
用法：直接运行即可
现象：见云端主函数
总结：做的事就是一直等云端发送数据，如果是发过来了'1'，表示开灯。同时按键也被检测着，一旦被按下则触发中断（另一个线程），灯也亮起。
数据发送：每次灯亮发送一次，灯灭发送一次，发送的数据格式为(device_id,time_from_rasp,led_status)，对应云端数据库。
"""

import RPi.GPIO as GPIO
import socket
import sys
import time

HOST = '124.223.76.58'  # 服务器的公网IP
PORT = 7789             # IP开放的socket端口
BUFSIZ = 1024           # socket缓冲区大小
ADDR = (HOST, PORT)
led_delay_time = 5      # led的持续亮起时间

turn_on  =  1
turn_off =  0
web_submit_status = turn_off  # 网页端按下submit(选择了开灯)，则发送过来 '1'

# 初始化端口
GPIO.setmode(GPIO.BCM) 
SOUND_SENSOR = 22
LIGHT_SENSOR = 23
LED = 27
button = 17                    # 后期换成传感器

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SOUND_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIGHT_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                  
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # 引脚默认高电平（拉高），按下后接地引脚电平被拉低
GPIO.output(LED,GPIO.LOW)

# 发送的数据格式：(device_id,time_from_rasp,led_status)，对应云端数据库
def send_data(device_id,time_from_rasp,led_status):
    data_send = str((device_id,time_from_rasp,led_status))  
    s.send(data_send.encode('utf-8'))

# 亮起发送一次，灭掉发送一次数据到云端（没调用，后续便于扩展）
def control_led():
    send_data(1,data,1)           # 发送数据（状态为亮起）
    GPIO.output(LED,GPIO.HIGH)

    time.sleep(led_delay_time)

    send_data(1,data,0)           # 发送数据（状态为灭掉）
    GPIO.output(LED,GPIO.LOW)

# 回调函数，按下按键的中断执行函数，现象为灯亮起且发送两次数据给云端
def my_callback(button):
    if(GPIO.input(LIGHT_SENSOR)==True):
        time.sleep(0.4)
        if(GPIO.input(LIGHT_SENSOR)==True):
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  raspberry'      # 当前时间
            print('按键按下')

            send_data(1,data,1)           # 发送数据（状态为亮起）
            GPIO.output(LED,GPIO.HIGH)

            time.sleep(led_delay_time)

            send_data(1,data,0)           # 发送数据（状态为灭掉）
            GPIO.output(LED,GPIO.LOW)
     


GPIO.add_event_detect(SOUND_SENSOR, GPIO.RISING, callback=my_callback, bouncetime=400)    # 检测button的中断函数


if __name__ == '__main__':
    # 建立连接，建议不要做成函数（s需要是全局变量）
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    # 树莓派主函数就是接受云端是否发来开灯指令，所以需要一直接收着（后面扩展的话可以参考云端的index.py双线程）
    while(True):
        web_submit_status = int(s.recv(BUFSIZ).decode('utf-8'))   # 一直等着收，收着了才继续向下运行，云端发送过来的是'1'
        if(web_submit_status == turn_on ):
            web_submit_status = turn_off    # 标志位，也可以不加，问题应该不大（但云端发送不只一种指令时必须加，如后面控制多个家居）
            data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            send_data(1,data,1)
            GPIO.output(LED,GPIO.HIGH)

            time.sleep(led_delay_time)

            send_data(1,data,0)
            GPIO.output(LED,GPIO.LOW)

            