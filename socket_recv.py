# -*- coding: utf-8 -*-
import socket
import struct
import threading
import time
import sys
import json

# HOST = '192.168.2.68'
# PORT = 60000
BUFFER_SIZE = 1024 * 1024 * 60
HEAD_STRUCT = 'q'  # Structure of file head
lst = 50
success_num = 0  # connect success number
error_num = 0  # connect error number
moment_recv_size = 0  # 2s accept data
all_recv_size = 0  # all success data
mu = threading.Lock()
TIME_PRINT = 1
Transmitting = 0

def jonnyS(client_socket):
    global Transmitting
    global BUFFER_SIZE
    global success_num
    global error_num
    global HEAD_STRUCT
    global all_recv_size
    global moment_recv_size
    mu.acquire()
    Transmitting += 1
    mu.release()
    recv_size = 0
    info_struct = struct.calcsize(HEAD_STRUCT)

    while True:
        file_info = client_socket.recv(info_struct)
        if len(file_info) == 8:
            data_size = struct.unpack(HEAD_STRUCT, file_info)[0]
            break
        # data_size: type(tuple)
    try:
        while recv_size < data_size:
            if data_size - recv_size < BUFFER_SIZE:
                file_data = client_socket.recv(data_size - recv_size)
            else:
                file_data = client_socket.recv(BUFFER_SIZE)
            recv_size += len(file_data)
            mu.acquire()
            moment_recv_size += len(file_data)
            mu.release()
            if file_data < 0 or file_data == 0:
                mu.acquire()
                all_recv_size += data_size
                mu.release()
                break
        if recv_size == data_size:
            mu.acquire()
            all_recv_size += data_size
            success_num += 1
            mu.release()
        else:
            mu.acquire()
            error_num += 1
            mu.release()
    except Exception as e:
        mu.acquire()
        print e
        error_num += 1
        mu.release()
    client_socket.close()
    mu.acquire()
    Transmitting -= 1
    mu.release()

def recv_file(args):
    _, HOST, PORT = args
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, int(PORT))
    sock.bind(server_address)
    sock.listen(lst)
    while True:
        client_socket, client_address = sock.accept()
        thread = threading.Thread(target=jonnyS, args=(client_socket,))
        thread.start()


def monitor():
    global success_num
    global error_num
    global all_recv_size
    global moment_recv_size
    global TIME_PRINT
    global Transmitting
    s_num = success_num
    e_num = error_num
    a_r_s = all_recv_size
    m_r_s = moment_recv_size
    time.sleep(2)
    dic = {"success_num": success_num, "error_num": error_num, "all_recv_size": all_recv_size,
           "moment_recv_size": moment_recv_size, "online_threading":Transmitting,"time": time.strftime("%Y-%m-%d %H-%M-%S")}
    f.write(json.dumps(dic))
    f.write('\n')
    if success_num == s_num and error_num == e_num and all_recv_size == a_r_s and moment_recv_size == m_r_s:
        if TIME_PRINT:
            # print "The last time {}".format(time.strftime("%Y-%m-%d %H-%M-%S"))
            mu.acquire()
            TIME_PRINT = 0
            mu.release()
    else:
        print "{}".format(time.strftime("%Y-%m-%d %H-%M-%S"))
        print "Pressed Ctrl+C flush data"
        print "success_sum: %s" % success_num
        print "error_num: %s" % error_num
        print "each_recv_size: %s" % moment_recv_size
        print "all_recv_size: %s" % all_recv_size
        print "online_threading: %s" % Transmitting
        print "-" * 30

        moment_recv_size = 0
        if not TIME_PRINT:
            mu.acquire()
            TIME_PRINT = 1
            mu.release()


if __name__ == '__main__':
    recv_file_thread = threading.Thread(target=recv_file, args=(sys.argv,))
    recv_file_thread.start()
    f = open('log', 'w+')
    while True:
        try:
            monitor()
        except KeyboardInterrupt:
            # cmd press Ctrl + C
            error_num = success_num = moment_recv_size = all_recv_size = 0
            e = ''
