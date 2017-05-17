#!/usr/bin/env python
"""
py to.exe:

pyinstaller yourprogram.py
"""

import socket
import subprocess
import os
from subprocess import call
import smtplib
from time import gmtime, strftime

TCP_IP = '127.0.0.1'
TCP_PORT = 5022
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
MESSAGE_OFF_PC = "b'OffPC'"
MESSAGE_KILL = "b'a'"
MESSAGE_START = "b'b'"
MESSAGE_START_T = "b'c'"
MESSAGE_KILL_T = "b'd'"

SERVER_TO_KILL = "a1"
SERVER_TO_START = "a2"
T_TO_KILL = "a3"
T_TO_START = "a4"

message_accept_off_pc = "Se apaga el pc correctamente."
message_accept_kill_process = "Se ha eliminado el proceso."

extension_exe = ".exe"

def start_process(name_process):
    os.system(name_process)
    #subprocess.call(name_process+extension_exe)
    return 0

def kill_process(name_process):
    string_code = "taskkill /f /im "
    error = os.system(string_code+name_process+extension_exe)
    return error

def send_email():
    time = strftime("%Y-%m-%d  %H:%M:%S", gmtime())
    from_addr = 'r@gmail.com'
    to_addr_list = ['x@gmail.com']
    cc_addr_list = ['a@gmail.com']
    subject = 'Apagando pc el dia y hora: [' + str(time) + ']'
    message = 'Se apaga el pc correctamente'
    login = 'r@gmail.com'
    password = 'ccccccc'

    header = 'From: %s' % from_addr
    header += ' \nSubject: {}\n\n{}'.format(subject, message)
    message = header + message

    smtpserver = 'smtp.gmail.com:587'
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def shutdown_pc():
    print("%%%%%%%%%%")
    print("BAT FILE")
    print("%%%%%%%%%%")
    # subprocess.call(["shutdown", "-f", "-s", "-t", "6"])
    print("%%%%%%%%%%")
    problems = send_email()
    print("Problems")
    print(str(problems))
    if len(str(problems)) > 2:
        print("Error al enviar mail, reintente otra vez.  ")
    else:
        print("Se ha enviado email correctamente")


def connect_server(socket):
    conn, addr = socket.accept()
    print('Connection address:', addr)
    data = conn.recv(BUFFER_SIZE)
    print('Se ha recibido:')
    print(str(data))
    print("--------------")
    if str(data) == MESSAGE_OFF_PC:
        print("Aceptado Apagar PC")
        shutdown_pc()
        conn.send(message_accept_off_pc.encode())  # echo
    elif str(data) == MESSAGE_KILL:
        print("Aceptado Matar Proceso ")
        info = kill_process(SERVER_TO_KILL)
        if info == 0:
            to_send = "Proceso: " + SERVER_TO_KILL + " eliminado!"
            print("Info--> " + str(info))
            print(to_send)
        else:
            to_send = "Error al eliminar proceso, crack"
        conn.send(to_send.encode())  # echo
    elif str(data) == MESSAGE_START:
        print("Aceptado Arrancar Servidor ")
        info = start_process(SERVER_TO_START)
        if info == 0:
            to_send = "Proceso: " + SERVER_TO_START + " arrancado!"
            print("Info--> " + str(info))
            print(to_send)
            conn.send(to_send.encode())  # echo
    elif str(data) == MESSAGE_START_T:
        print("Aceptado Arrancar TUNNGLE")
        info = start_process(T_TO_START)
        if info == 0:
            to_send = "Proceso: " + T_TO_START + " arrancado!"
            print("Info--> " + str(info))
            print(to_send)
            conn.send(to_send.encode())  # echo
    elif str(data) == MESSAGE_KILL_T:
        print("Aceptado Matar TUNNGLE")
        info = kill_process(T_TO_KILL)
        if info == 0:
            to_send = "Proceso: " + T_TO_KILL + " eliminado!"
            print("Info--> " + str(info))
            print(to_send)
            conn.send(to_send.encode())  # echo
    else:
        conn.close()
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    connect_server(socket=socket)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((TCP_IP, TCP_PORT))
socket.listen(1)
print("SERVER STARTED!")
connect_server(socket)
