# -*- coding: utf-8 -*-
import struct
import socket
import sys
import threading
import time
import random


HEAD_STRUCT = 'q'
FIXED_FILE_LIST = ['1' * 1024, '2' * 1024, '3' * 1024, '4' * 1024, '5' * 1024]
BUFFER_SIZE = 1024
mu = threading.Lock()
count = 0

def func():
    for i in range(n/5):
        send_file(sys.argv)


def send_file(args):
    fixed_size = 1024  #  1KB
    _, host, port, n, file_size = args  # file_size 为发送多少kb
    global count
    port = int(port)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    file_size = eval(file_size)
    fixed_file = random.choice(FIXED_FILE_LIST)
    file_head = struct.pack(HEAD_STRUCT, file_size * fixed_size)
    try:
        sk.connect((host, port))
        sk.send(file_head)
        while True:
            if file_size - BUFFER_SIZE > 0:
                sk.send(BUFFER_SIZE * fixed_file)
                file_size -= BUFFER_SIZE
            else:
                sk.send(file_size * fixed_file)
                break
    except Exception as e:
        print 'error is {}'.format(e)
    finally:
        sk.close()
        mu.acquire()
        count += 1
        mu.release()


if __name__ == '__main__':
    start = time.time()
    n = eval(sys.argv[3])
    for i in range(5):
        send_thread = threading.Thread(target=func)
        send_thread.start()
        send_thread.join()
        # send_file(sys.argv)  # 串行发送时使用

    send_end = time.time()
    print "cost {} seconds".format(send_end - start)
    # 执行命令为 python2 c4.py HOST, PORT, 发送次数(只支持两数相乘， 如 1024*1024)， 发送的数据（单位为kb，只支持两数相乘， 如 1024*1024）
