import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg):
   print("Recibido: " + str(msg.payload.decode('utf-8')) + " del topic: " + str(msg.topic))

mqttBroker = "192.168.56.105"                   #IP o URL del servidor MQTT

client = mqtt.Client("Sniffer")         #Nombre del cliente suscriptor
client.connect(mqttBroker)                      #Realiza la conexion con el servidor MQTT

client.loop_start()

client.subscribe("maquinaria/prensa_hidraulica")        #Se suscribe al topic

#La siguiente linea se encarga de mostrar el mensaje recibido
client.on_message=on_message

time.sleep(30)
client.loop_stop()
                     
