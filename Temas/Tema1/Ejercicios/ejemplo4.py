import requests

numero = input("Ingrese un número: ")
metodo="POST"
uri="http://gae-sw-2017.appspot.com/processForm"
cabecera={"Host": "gae-sw-2017.appspot.com", "Content-Lenght": "12", "Content-Type": "application/x-www-form-urlencoded"}
cuerpo="dni="+numero

respuesta = requests.request(metodo, uri, headers=cabecera, data=cuerpo, allow_redirects=False)

print("DNI: " + respuesta.text)