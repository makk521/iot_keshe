"""
数据：网页表单上获得的点灯指令需要发送到树莓派上，所有数据库的数据都来自树莓派
运行：直接运行即可。先运行后再运行树莓派上的
"""
from flask_socketio import SocketIO
from flask import Flask,render_template,request
import socket
import sys
import sqlite3
import os
import time
from threading import Thread,Lock
from datetime import datetime
from random import random

thread = None
thread_lock = Lock()
ind = 10
name = socket.gethostname()
HOST = socket.gethostbyname('10.0.12.13')  
PORT = 7789     # socket通信端口
BUFSIZ = 1024
ADDR = (HOST, PORT)

led_status_on  = 1
led_status_off = 0
led_status = led_status_off

# 若没有则创建名为data的数据库。并添加名为data的table。每一行为：ID，date_time，device_id，led_status  
if not os.path.isfile('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE data (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time text, 
        device_id integer,
        led_status integer
        )""")
    conn.commit()
    conn.close()

# 保存来自树莓派发送过来的数据
def date_save_rasp(device_id,time_from_rasp,led_status):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES(:Id,  :date_time, :device_id, :led_status)",
            {'Id': None,  'date_time': time_from_rasp,  'device_id': int(device_id),  'led_status': int(led_status)})
    conn.commit()
    c.close()
    conn.close()

# 接收来自树莓派发送过来的数据。同样，需要在单独的线程中一直运行。
def receive_from_rasp():
    while(True):
        print('start')
        buf = sock.recv(BUFSIZ)  # 接收数据
        print('received')
        data_from_raspberry = eval(buf.decode('utf-8'))  # 很重要！经测试只能传输字符串类型，用eval转换成tuple。得到(device_id,time_from_rasp,led_status)
        date_save_rasp(data_from_raspberry[0],data_from_raspberry[1],data_from_raspberry[2])

# 查询数据库最新的一条（行）
def date_check():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    max_id = c.execute("SELECT MAX(ID) FROM data ").fetchone() # max_id = (0,)，注意查询出来的都是tuple类型
    sql = "SELECT * FROM data where ID = %s"%max_id[0]
    c.execute(sql)  
    return c.fetchone()

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread():
    
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        # print(type(dummy_sensor_value))
        # dummy_sensor_value = date_select(1)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/index", methods=['GET', "POST"])
def index():     
    return render_template("index.html")

@app.route("/refresh", methods=['GET', "POST"])
def refresh():     
    return render_template("refresh.html")

# 查看最新的亮灯时间
@app.route("/message", methods=['GET', "POST"])
def message():
    new = date_check()
    if new[3] == 1:
        led_status = 'on'
    else:
        led_status = 'off'
    
    return render_template("message.html",led_on_time= new[1],led_status = led_status)

@app.route("/control", methods=['GET', "POST"])
def control():
    if request.method == "GET":
        return render_template("control.html")
    else:
        led_status_control = request.form.get("led_status_control")  # 在网页表单上获取led_status_control
        sock.send(led_status_control.encode('utf-8'))                # 将获取的状态值发到树莓派
        print('指令已发送')
        return render_template("index.html")

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)


if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(ADDR)  # 在不同主机或者同一主机的不同系统下使用实际ip
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    sock, addr = s.accept()

    Thread(target = receive_from_rasp).start()
    Thread(target = socketio.run(app,host='0.0.0.0')).start()
        
    


