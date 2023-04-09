import os
from datetime import datetime

log_date = str(datetime.now())
document_name = "event-" + log_date + ".log"

with open(document_name, "w") as file:	#w sobreescribe contenido en cada llamada, a(append) agrega
	file.write("Se ha producido una intrusion!\n")
	file.write("Hora del evento " + log_date + "\n")

while True:
  #Presentacion de una shell real (no es adecuado)
	os.system(input("$ "))
