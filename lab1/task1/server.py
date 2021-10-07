#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import socket
from datetime import datetime, date, time

host = '127.0.0.1'
port = 9999

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((host, port))

i = 0

while i < 3:
    serversocket.listen(5)
    print('Server is waiting!\n')

    clientsocket, addr = serversocket.accept()

    clientsocket.send('Input message?'.encode('utf-8'))

    client_message = clientsocket.recv(1024).decode('utf-8')
    current_time = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

    print('[' + current_time + '] :' + client_message)
    clientsocket.close()
    print('\n')
    i += 1
