import socket
import sys


def socket_service_data():
    # 连接
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(ADDR)  # 在不同主机或者同一主机的不同系统下使用实际ip
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Wait for Connection..................")

    sock, addr = s.accept()
    
    while True:
        # # 收
        # buf = sock.recv(BUFSIZ)  # 接收数据
        # buf1 = buf.decode('utf-8')  # 解码
        # if not buf:
        #     break
        # print('Received message:', buf1)
        # # return buf
        # 发
        buf = input("input data:")  # 输入要传输的数据
        if not buf:
            break
        sock.send(buf.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
    # 关闭socket
    sock.close()


if __name__ == '__main__':
    # 初始化
    name = socket.gethostname()
    HOST = socket.gethostbyname('10.0.12.13')  # 获取阿里云服务器私网IP，使用ifconfig可查询
    PORT = 7789
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    socket_service_data()

