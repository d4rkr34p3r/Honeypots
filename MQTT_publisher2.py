import paho.mqtt.client as mqtt
from random import uniform
import time

mqttBroker = "127.0.0.1"                        #Se especifica direccion o la URL del Broker

client = mqtt.Client("Temperatura del horno")   #Este es el nombre que se asigna al publicador
client.connect(mqttBroker)


while True:
        temperatura = uniform(0.0, 150.0)       #Crea un aleatorio entre minimo y maximo
        client.publish("maquinaria/horno", temperatura)         #y publica el mensaje cada segundo
        print("Se ha publicado " + str(temperatura) + " en el topic maquinaria/horno")
        time.sleep(1)
