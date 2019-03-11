# -*- coding: utf-8 -*-
import socket
import struct
import threading
import time
import sys

# HOST = '192.168.2.68'
# PORT = 60000
BUFFER_SIZE = 1024
HEAD_STRUCT = 'q'  # Structure of file head
lst = 50
success_num = 0  # connect success number
error_num = 0  # connect error number
moment_recv_size = 0  # 2s accept data
all_recv_size = 0  # all success data
e = ''
mu = threading.Lock()


def jonnyS(client_socket):
    global e
    global BUFFER_SIZE
    global success_num
    global error_num
    global HEAD_STRUCT
    global all_recv_size
    global moment_recv_size
    recv_size = 0
    info_struct = struct.calcsize(HEAD_STRUCT)
    file_info = client_socket.recv(info_struct)
    data_size = struct.unpack(HEAD_STRUCT, file_info)[0]
    # data_size: type(tuple)
    try:
        while recv_size < data_size:
            if data_size - recv_size < BUFFER_SIZE:
                file_data = client_socket.recv(data_size - recv_size)
            else:
                file_data = client_socket.recv(BUFFER_SIZE)
            recv_size += len(file_data)
            moment_recv_size += len(file_data)
            if file_data < 0 or file_data == 0:
                all_recv_size += data_size
                break
        if recv_size == data_size:
            all_recv_size += data_size
            mu.acquire()
            success_num += 1
            mu.release()
        else:
            mu.acquire()
            error_num += 1
            mu.release()
    except Exception as e:
        mu.acquire()
        error_num += 1
        mu.release()
    client_socket.close()


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
    global e
    time.sleep(2)
    print "Pressed Ctrl+C flush data"
    print "success_sum: %s" % success_num
    print "error_num: %s" % error_num
    print "each_recv_size: %s" % moment_recv_size
    print "all_recv_size: %s" % all_recv_size
    print "error message: %s" % e
    print "-" * 30
    moment_recv_size = 0


if __name__ == '__main__':
    recv_file_thread = threading.Thread(target=recv_file, args=(sys.argv,))
    recv_file_thread.start()
    while True:
        try:
            monitor()
        except KeyboardInterrupt:
            # cmd press Ctrl + C
            error_num = success_num = moment_recv_size = all_recv_size = 0
            e = ''
