from threading import Thread
import time
# def func1():
#     while(1):
#         print('1')
#         time.sleep(1)

# def func2():
#     while(1):
#         print("2")
#         time.sleep(1)

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()