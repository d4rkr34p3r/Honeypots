import socket
import sys
from threading import Thread
import MQTT_decoder
from MQTT_packet_handler import packet_router
import time
from MQTT_control_packets import PUBLISH
import MQTT_packet_handler

from datetime import datetime


HOST = "192.168.56.105"
PORT = 1883

whitelist = ["192.168.56.101", "192.168.56.104"]
connected_clients = []


def main():
	start_broker()


def start_broker():
    #Create server socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind socket to port
	try:
		server_socket.bind((HOST, PORT))
		print(f"Binding server socket to host: {HOST} and port: {PORT}")
	except:
		print(f"Bind failed. \nError: {str(sys.exc_info())}")
		sys.exit()

    #Enable passive listening sockets
	server_socket.listen(5)

    #Periodically jump out of accept waiting process to receive keyboard interrupt commnad
	server_socket.settimeout(0.5)


	while True:
		client_socket = None

		try:
	 	   #Wait and accept incoming connection
			(client_socket, address) = server_socket.accept()
			ip, port = str(address[0]), str(address[1])
			print(f"Connection from {ip}:{port} has been established.")

			try:
				Thread(target=client_thread, args=(client_socket, ip, port)).start()
				print(f"Client thread for {ip}:{port} has been created.")
			except:
				print(f"Client thread for {ip}:{port} did not create")
		except socket.timeout:
			pass
		except KeyboardInterrupt:
			sys.exit()


def client_thread(client_socket, ip, port):

	global connected_clients

	client_ID = ""

	while True:
		try:
	            #Listen to incoming data
			try:
				data = client_socket.recv(1024)
			except:
				print(f'Client ({client_ID}) unexpected disconnect.')
				connected_clients = [client for client in connected_clients if client_ID not in client]
				sys.exit()

			if not data:
				time.sleep(0.5)
				print(f"Client ({client_ID}) went to sleep")
				break

	            #Decode incoming packet
			incoming_packet = MQTT_decoder.decode(data)

			if incoming_packet.get("Packet type") == "CONNECT":
				client_ID = incoming_packet.get("Payload")
				connected_clients.append((client_ID, client_socket))
				print()

				for i in connected_clients:
					h_IP = i[1].getpeername()[0]

					intrusion = True
					for j in whitelist:
						if(h_IP == j):
							intrusion = False	#Entonces la IP esta en la whitelist
							break
						else:
							pass

					if(intrusion == True):
						print("Intrusion detectada con la IP: " + str(h_IP))
						print("Creando un log del evento...")
						print()
					   #Aqui ahora se crea el log
						event_hour = str(datetime.now())
						logname = str(h_IP) + "-" + event_hour

						with open(logname, "w") as f:
							f.write("Nuevo evento, detectada una intrusion!!\n")
							f.write("\n")
							f.write("\n")
							f.write("Desglose del evento:\n")
							f.write("	IP:" + str(h_IP) +"\n")
							f.write("	Acciones: Intento de conexion\n")
							f.write("\n")

			if incoming_packet.get("Packet type") == "DISCONNECT":
				connected_clients = [client for client in connected_clients if client_ID not in client]

		    #Do events & encode outgoing packet
			outgoing_packet = packet_router.route_packet(incoming_packet, client_ID)

		    #Send outgoing packet
			if incoming_packet.get("Packet type") == "PUBLISH":
				send_to_all_connected(outgoing_packet)
			else:
				client_socket.send(outgoing_packet)

		    #Send publish packet that has been retained to new subscribers
			if incoming_packet.get("Packet type") == "SUBSCRIBE":
				topic = incoming_packet.get('Topics')[0]
				topic = next(iter(topic))

		except KeyboardInterrupt:
			client_socket.close()
			sys.exit()


def send_to_all_connected(packet: bytes):
	global connected_clients

	for client in connected_clients:
		client_ID, client_socket = client
		client_socket.send(packet)

if __name__ == "__main__":
	main()
