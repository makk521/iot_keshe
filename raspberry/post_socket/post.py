import socket
import sys

send_data = str((1,'2022.12',1))
def sock_client_data():
    # 连接
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))

    while True:
        # 发
        data = input("input data:")  # 输入要传输的数据
        if not data:
            break
        s.send(send_data.encode('utf-8'))  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
        print(type(send_data.encode('utf-8')))
        # # 收
        # data = s.recv(BUFSIZ)
        # if not data:
        #     break
        # print(data.decode('utf-8'))
    # 关闭socket
    s.close()


if __name__ == '__main__':
    # 初始化
    HOST = '124.223.76.58'  # 比如 99.100.101.102是你的服务器的公网IP
    PORT = 7789  # IP开放的socket端口
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    sock_client_data()

