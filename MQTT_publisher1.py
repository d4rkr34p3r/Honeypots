import paho.mqtt.client as mqtt
from random import uniform
import time

mqttBroker = "127.0.0.1"                        #Se especifica direccion o la URL del Broker

client = mqtt.Client("Presion de prensa")       #Este es el nombre que se asigna al publicador
client.connect(mqttBroker)


while True:
        presion = uniform(0.0, 12000.0)         #Crea un aleatorio entre minimo y maximo
        client.publish("maquinaria/prensa_hidraulica", presion)         #y publica el mensaje cada segundo
        print("Se ha publicado " + str(presion) + " en el topic maquinaria/prensa_hidraulica")
        time.sleep(1)
