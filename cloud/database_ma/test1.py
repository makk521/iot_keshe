import sqlite3
import os
import time

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
    date_time_str = now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    c.execute("INSERT INTO data VALUES(:Id,  :date_time, :device_id)",
            {'Id': None,  'date_time': date_time_str,  'device_id': int(device_id)})
    conn.commit()
    c.close()
    conn.close()


date_save(3)
date_save(2)
date_save(1)


# 查询
conn = sqlite3.connect('data.db')
c = conn.cursor()
max_id = c.execute("SELECT MAX(rowid) FROM data ").fetchone()
sql = "SELECT * FROM data "
c.execute(sql)  #最新一条

row1 = c.fetchone()
print(row1,max_id)