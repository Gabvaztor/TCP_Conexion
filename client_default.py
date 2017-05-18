#!/usr/bin/env python

"""
py to .exe:

pyinstaller yourprogram.py
"""

import socket

def print_bar():
	print("------------------------------")
def ask_question():
	MESSAGE_1 = "a"
	MESSAGE_2 = "b"
	MESSAGE_3 = "c"
	MESSAGE_4 = "d"
	MESSAGE_5 = "e"
	print_bar()
	s = input("\nIntroduce:\n\n*1, 2, 3, 4 or 5 *TU OPCION*-->")
	print_bar()
	if (s == '1'):
		value = MESSAGE_1
	elif (s == '2'):
		value = MESSAGE_2
	elif (s == '3'):
		value = MESSAGE_3
	elif (s == '4'):
		value = MESSAGE_4
	elif (s == '5'):
		value = MESSAGE_5
	else:
		print_bar()
		print("Introduce un valor válido")
		print_bar()
		value = ask_question()
	return value


def main():
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5020
	BUFFER_SIZE = 1024

	answer = ask_question()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(answer.encode())
	data = s.recv(BUFFER_SIZE)
	s.close()
	print(data)
	print_bar()
	to_restart = input("\nPulsa: \n*1 para reiniciar la operación \n*Otra tecla para salir \n*TU OPCION-->")
	print_bar()
	if to_restart == '1':
		main()
main()

