#!/usr/bin/env python3

import platform, os, time
import socket, paramiko
import sys
from datetime import datetime


def honeypot_message():
	clean()
	print("---         ----- ")
	print(" |          |     ")
	print(" |   |   |  ----- ")
	print(" |   |---|      | ")
	print("---  |   |  ----- ")

	print()
	print()

	print("Industrial honeypot [basic version] - Developed for SIND(munics)")
	print("Consider to upgrade to the premium version that offers more functionalities...")
	print()

	system_id()
	print()



def system_id():
	OS_info = platform.system()
	system_version = platform.version()
	system_release = platform.release()

	print("This program is running over: " + OS_info)
	print("	Version: " + system_version)
	print("	Release: " + system_release)
	print("\n")

def clean():
	OS = platform.system()
	if(OS == "Linux"):
		os.system('clear')
	elif(OS == "Windows"):
		os.system('cls')
	else:
		print("Unknown system, clean cannot be executed...")


def event(e, net, credentials):
	log_date = str(datetime.now())
	document_name = "event-" + log_date + ".log"

	with open(document_name, "w") as file:
		file.write("The honeypot has detected a new event!!!\n")
		file.write("\n")
		file.write("\n")
		file.write("Description of the event:\n")
		file.write("	-Date and hour: " + log_date + "\n")
		file.write("	-IP: " + str(net[0]) + "\n")
		file.write("	-Port: " + str(net[1]) + "\n")
		file.write("	-User: " + str(credentials[0]) + "\n")
		file.write("	-Password: " + str(credentials[1]) + "\n")
		file.write("	-Threat: " + str(e[0]) + "\n")
		file.write("	-Description:\n" + "		" + str(e[1]))
		file.write("\n")
		file.write("\n")


def ssh_honey(honeypot_host, honeypot_port):
	try:
		with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((honeypot_host, honeypot_port))

			print("Honeypot up and running, waiting connections...")
			print(f"Honeypot listening over: {honeypot_host, honeypot_port}")
			print()

			while True:
				try:
					s.listen()
					client, addr = s.accept()

					with client:
						print(f"Detected conection with: {addr}")

						data = client.recv(1024)

						if not data:
							pass
						else:
							data_recv = data.decode("utf-8")
							data_recv = str(data_recv)

							print("New message, received: " + data_recv)

							if("SSH" in data_recv):
								print("SSH detected, killing remote connection...")
								print()
								print()

							   #Take a new log about the event
								event(["Intrusion", {"Attempt of connection with SSH"}], addr, ["", ""])


						client.close()
						time.sleep(2)

				except Exception as e:
					print("Detected exception: " + str(e))


	except Exception as e:
		print("ERROR: " + str(e))
		s.close()
		time.sleep(2)
		sys.exit(1)

	finally:
		s.close()
		time.sleep(2)


#Test bench - Main execution of honeypot...
try:
	honeypot_message()

	IP_filename = "IP.conf"

	if os.path.exists(IP_filename):
		print("File found, reading content...")
		time.sleep(2)
		with open(IP_filename, 'r') as file:
			ip = file.read()
	else:
		print("File not found, creating a new file...")
		with open(IP_filename, 'w') as file:
			ip = input("Enter the IP to use: ")
			file.write(ip)

	cond = False
	clean()

	while(cond == False):
		resp = input("It will be used the IP: " + ip + " ¿Is alright [Y/N]?: ")
		match(resp):
			case "Y":
				cond = True
			case "N":
				print()
				print("The next interfaces are found:")
				if_ip = os.system("ifconfig")
				print(if_ip)
				print()
				ip = input("Enter the new IP: ")
				with open(IP_filename, 'w') as file:
					file.write(ip)
				clean()
			case _:
				print("ERROR: Character not recognized")
				time.sleep(2)
				clean()


	ssh_honey(ip, 22)


except KeyboardInterrupt:
	print()
	print("Exiting...")
	time.sleep(3)
	clean()
