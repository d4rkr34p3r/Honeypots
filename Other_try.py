#Este es otro codigo sin acabar, ha sido una base para el Honeypot funcional SSH que tambien se encuentra en este repositorio

#!/usr/bin/env python3

import platform, os, time
import socket, paramiko
from datetime import datetime

#from concurrent.futures import ThreadPoolExecutor

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
        print(" Version: " + system_version)
        print(" Release: " + system_release)
        print("\n")

def clean():
        OS = platform.system()
        if(OS == "Linux"):
                os.system('clear')
        elif(OS == "Windows"):
                os.system('cls')
        else:
                print("Sistema desconocido, no se puede ejecutar limpiar pantalla...")


def event(e, net, credentials):
        log_date = str(datetime.now())
        document_name = "event-" + log_date + ".log"

        with open(document_name, "w") as file:
                file.write("El honeypot ha detectado un nuevo evento!!!\n")
                file.write("\n")
                file.write("\n")
                file.write("Desglose del evento:\n")
                file.write("    -Fecha y hora del evento " + log_date + "\n")
                file.write("    -IP: " + str(net[0]) + "\n")
                file.write("    -Puerto: " + str(net[1]) + "\n")
                file.write("    -Usuario: " + str(credentials[0]) + "\n")
                file.write("    -Password: " + str(credentials[1]) + "\n")
                file.write("    -Amenaza: " + str(e[0]) + "\n")
                file.write("    -Descripcion:\n" + "            " + str(e[1]))
                file.write("\n")
                file.write("\n")


def ssh_honey(honeypot_host, honeypot_port):
#       u = "username"
#       p = "password"

#       ssh_honeypot = paramiko.SSHClient()
#       ssh_honeypot.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#       ssh_honeypot.connect(honeypot_host, honeypot_port, u, p)

        try:
                ssh_honeyp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssh_honeyp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                ssh_honeyp.bind((honeypot_host, honeypot_port))

                print("El servidor esta a la escucha de conexiones...")
                ssh_honeyp.listen()

                while True:
                        try:
                                client_socket, client_addr = ssh_honeyp.accept()
                                print(client_socket.recv(1024))
                                #thread.start_new_thread(handleConnection, (client_socket))

                        except Exception as e:
                                print("Error manejando el cliente: " + str(e))

        except Exception as e:
                print("ERROR: " + str(e))
                sys.exit(1)








def others():
        with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((honeypot_host, honeypot_port))

                while True:
                        print("Honeypot activo, esperando por conexiones entrantes...")
#                       print(f"El honeypot esta escuchando en {honeypot_host, honeypot_port}")
                        print()

                        s.listen()
                        client, addr = s.accept()

                        with client:
#                               print(f"Detectada conexion con: {addr}")
                                while True:
                                        data = client.recv(1024)
                                        if not data:
                                                break
                                        #user_ok = "False"

                                        data_recv = data.decode("utf-16")
                                        data_recv = str(data_recv)

                                        print("Nuevo mensaje recibido, se ha recibido: " + data_recv)

                                        if("SSH" in data_recv):
                                           #Se lanza el honeypot SSH
                                                msg = "SSH-2.0-OpenSSH_9.0p1 Debian\n"
                                                #s.connect(addr)
                                                client.sendall(bytes(msg, 'utf-16'))
                                                print("SSH detectado")
                                        else:
                                                #se ejecuta otro honeypot...
                                                pass

        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)


#Test bench - Main execution of honeypot...
try:
        honeypot_message()

    #Se obtiene la IP donde se ejecutara el servicio
        IP_filename = "IP.conf"

        if os.path.exists(IP_filename):
                print("Fichero encontrado, leyendo el contenido...")
                time.sleep(2)
                with open(IP_filename, 'r') as file:
                        ip = file.read()
        else:
                print("No se ha encontrado el fichero, creando uno nuevo...")
                with open(IP_filename, 'w') as file:
                        ip = input("Introduzca la IP que se utilizara: ")
                        file.write(ip)

        cond = False
        clean()

        while(cond == False):
                resp = input("Se utilizara la IP: " + ip + " ¿Es correcto [Y/N]?: ")
                match(resp):
                        case "Y":
                                cond = True
                        case "N":
                                print()
                                print("Estan disponibles las interfaces siguientes:")
                                if_ip = os.system("ifconfig")
                                print(if_ip)
                                print()
                                ip = input("Introduzca la nueva IP: ")
                                with open(IP_filename, 'w') as file:
                                        file.write(ip)
                                clean()
                        case _:
                                print("ERROR: Caracter no reconocido")
                                time.sleep(2)
                                clean()

#       executor = ThreadPoolExecutor

#       ports = range(1024)
#       print(ports)

        ssh_honey(ip, 22)

#               event(["Intrusion", {"sudo su", "cd /", "ls"}], ["122.0.0.22", "2222"], ["user", "pass"])
#               i += 1
#               time.sleep(20)

except KeyboardInterrupt:
        print()
        print("Deteniendo el programa...")
        time.sleep(3)
        clean()
