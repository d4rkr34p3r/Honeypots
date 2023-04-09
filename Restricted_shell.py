#Este es un intento de restricted shell, esta muy lejos de estar finalizado pero lo he dejado aqui como un backup personal...

import getpass, os
import socket


blacklist = []
folder = "secure_container"
user = getpass.getuser()
hostname = socket.gethostname()

print(hostname)

if(not os.path.exists(folder)):
        os.system("mkdir " + folder)
        #Tengo que agregar el resto para hacerlo ver como el directorio normal de un sistema

os.chdir(folder)
ruta_base = os.getcwd()

def calcula_ruta():
        ruta_real = os.getcwd()
        mi_ruta = ruta_real.replace(ruta_base, "")
        print(mi_ruta)
#       return mi_ruta

#terminal = user + "@" + hostname + ":" + os.getcwd() + "# "
#print(terminal)

#print("root@")


calcula_ruta()



#os.system("pwd")


#print(whoami)
#print(os.getcwd())
