from flask import Flask,render_template,request
import socket
import sys
import sqlite3
import os
import time
import asyncio

name = socket.gethostname()
HOST = socket.gethostbyname('10.0.12.13')  # 获取阿里云服务器私网IP，使用ifconfig可查询
PORT = 7789
BUFSIZ = 1024
ADDR = (HOST, PORT)

if not os.path.isfile('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE data (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time text, 
        device_id integer
        )""")
    conn.commit()
    conn.close()

def date_save(device_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    date_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c.execute("INSERT INTO data VALUES(:Id,  :date_time, :device_id)",
            {'Id': None,  'date_time': date_time_str,  'device_id': int(device_id)})
    conn.commit()
    c.close()
    conn.close()

def date_save_rasp(device_id,time_from_rasp):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES(:Id,  :date_time, :device_id)",
            {'Id': None,  'date_time': time_from_rasp,  'device_id': int(device_id)})
    conn.commit()
    c.close()
    conn.close()

def date_check():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    max_id = c.execute("SELECT MAX(ID) FROM data ").fetchone()
    # 注意，查询出来的数据皆为元组类型
    sql = "SELECT * FROM data where ID = %s"%max_id[0]
    c.execute(sql)  #最新一条
    return c.fetchone()


 


app = Flask(__name__)

@app.route("/index", methods=['GET', "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        led_statue = request.form.get("led_statue")
        # 发送数据
        sock.send(led_statue.encode())
        # 将时间存入
        date_save(1)
        print(led_statue)
        
        # 后面换成index
        return render_template("index.html")

@app.route("/message", methods=['GET', "POST"])
def message():
    buf = sock.recv(BUFSIZ)  # 接收数据
    time_from_raspberry = buf.decode('utf-8')  # 解码
    date_save_rasp(1,time_from_raspberry)
    new = date_check()
    return render_template("message.html",led_on_time=new[1])

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

    # asyncio.run(receive_socket_run())
    print(111111)
    app.run(host='0.0.0.0')
    print(222222)

