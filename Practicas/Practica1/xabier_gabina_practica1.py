# -*- coding: utf-8 -*-
"""
Nombre y apellidos: Xabier Gabiña Barañano
Asignatura y grupo: Sistemas Web, Grupo 01
Fecha: 12/02/2024
Nombre de la tarea: Práctica 1 | IoT con ThingSpeak

La practica tiene 4 partes.
    1. La primera acción que realizará el cliente será crear un canal con dos campos de
    datos: %CPU y %RAM. El cliente almacenará el identificador y la clave escritura del
    canal en un fichero de texto
    
    2. En el caso de que el canal registrado en el cliente ya exista en ThingSpeak, no se
    creará un nuevo canal, sino que se seguirá utilizando el existente. Por otra parte, si
    a la hora de crear el canal se detecta que se ha superado el número máximo de
    canales permitidos por cuenta de usuario, el cliente deberá informar de dicha
    circunstancia de forma que el usuario pueda resolver el problema manualmente y
    el cliente pueda continuar con el proceso de creación del canal
    
    3. Una vez creado el canal, el cliente subirá los datos %CPU y %RAM del ordenador a
    ThingSpeak cada 15 segundos. Los datos se obtendrán utilizando la librería psutil

    4. El usuario pulsará Ctrl+C para cerrar el cliente. Éste gestionará esta señal de
    interrupción realizando un backup local de las últimas 100 muestras de los datos
    almacenados en el canal en un fichero CSV. A continuación, el cliente vaciará el canal
    (es decir, borrará los datos existentes en el canal, pero sin eliminarlo) y terminará
    su ejecución de forma ordenada
"""

# Librerias
import os
import signal
import sys
import time
import urllib
import requests
import psutil

# Variables globales
user_api_key= "VUC6R34M4NQ9AR8O"
id = ""
name = ""
write_api_key = ""
read_api_key = ""
i=0

# Funciones
def signal_handler(signal, frame):
    """
    Maneja la señal de interrupción y finaliza la ejecución del programa.
    
    Parámetros:
    - signal: la señal recibida.
    - frame: el marco de ejecución actual.
    """
    descargar_datos()
    vaciar_canal()
    print("Terminando la ejecución...")
    sys.exit(0)

def crear_canal():
    """
    Crea un canal en ThingSpeak con dos campos de datos: %CPU y %RAM.
    Almacena el identificador y las claves de API en un archivo de texto.
    """
    
    print("Creando canal...")
    metodo = 'POST'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {
        'Host': 'api.thingspeak.com',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    cuerpo = {
        'api_key': user_api_key,
        'name': 'xg_sw_practica1',
        'field1': "%CPU",
        'field2': "%RAM"
        }
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,data=cuerpo_encoded, allow_redirects=False)
    
    if respuesta.status_code==200:
        print("Canal creado.")
        response_json = respuesta.json()
        id = response_json['id']
        name= response_json['name']
        channel_keys = response_json['api_keys']
        for key in channel_keys:
            if key['write_flag']:
                write_api_key = key['api_key']
            else:
                read_api_key = key['api_key'] 
        escribir_canal_data(id, name, write_api_key, read_api_key)
    elif respuesta.status_code == 402:
        print("Se requiere pago o borrado de un canal desde la web.")
        sys.exit(1)
    else:
        print("Algo ha salido mal...")
        print(respuesta.status_code)
        sys.exit(1)

def escribir_canal_data(p_id, p_name, p_write_api_key, p_read_api_key):
    """
    Escribe la ID, el nombre y las claves de API en un documento.

    Parámetros:
    - id (str): Identificador del canal.
    - name (str): Nombre del canal.
    - write_api_key (str): Clave de API de escritura del canal.
    - read_api_key (str): Clave de API de lectura del canal.
    """
    with open("data.txt", "w") as file:
        file.write(f"ID={p_id}\n")
        file.write(f"NAME={p_name}\n")
        file.write(f"WRITE_API_KEY={p_write_api_key}\n")
        file.write(f"READ_API_KEY={p_read_api_key}\n")

def comprobar_canal_data():
    """
    Comprueba si el canal de datos es accesible mediante la API de ThingSpeak.

    Returns:
        bool: True si el canal es accesible, False en caso contrario.
    """
    with open("data.txt", "r") as file:
        lines = file.readlines()
        id = lines[0].split("=")[1].strip()
        read_api_key = lines[3].split("=")[1].strip()
    metodo = 'GET'
    uri = f"https://api.thingspeak.com/channels/{id}/status.json?api_key={read_api_key}"
    respuesta=requests.request(metodo, uri, allow_redirects=False)
    
    if respuesta.status_code == 200:
        return True
    else:
        return False

def cargar_canal_data():
    """
    Lee los datos del archivo 'data.txt' y asigna los valores de id, name, write_api_key y read_api_key a variables globales.
    """
    global id, name, write_api_key, read_api_key
    with open("data.txt", "r") as file:
        lines = file.readlines()
        id = lines[0].split("=")[1].strip()
        name = lines[1].split("=")[1].strip()
        write_api_key = lines[2].split("=")[1].strip()
        read_api_key = lines[3].split("=")[1].strip()

def vaciar_canal():
    """
    Vacía el canal de ThingSpeak eliminando todos los feeds.

    Utiliza el método DELETE de la API de ThingSpeak para eliminar todos los feeds del canal.
    Se requiere proporcionar la clave de API del usuario para autenticarse.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """
    print("Vaciando canal...")
    metodo='DELETE'
    url=f"https://api.thingspeak.com/channels/{id}/feeds.json"
    cabeceras = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cuerpo = {
        'api_key': user_api_key
    }
    respuesta = requests.request(metodo, url, headers=cabeceras, data=cuerpo, allow_redirects=False)
    
    if respuesta.status_code == 200:
        print("Canal vaciado.")
    else:
        print("Error al vaciar el canal.")
        print(respuesta.status_code)

def obtener_cpu_and_ram():
    """
    Obtiene el porcentaje de uso de la CPU y de la memoria RAM.

    Returns:
        tuple: Una tupla que contiene el porcentaje de uso de la CPU y de la memoria RAM.
    """
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    return cpu_percent, ram_percent   

def subir_datos():
    """
    Sube los datos de CPU y RAM a la plataforma ThingSpeak.

    Parámetros:
    - write_api_key (str): Clave de API para acceder al canal de ThingSpeak.
    """
    global i
    i=i+1
    print(f"{i}: Subiendo datos")
    cpu, ram = obtener_cpu_and_ram()
    metodo = 'POST'
    uri = "https://api.thingspeak.com/update.json"
    cabeceras = {
        'Host': 'api.thingspeak.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cuerpo = {
        'api_key': write_api_key,
        'field1': cpu,
        'field2': ram
    }
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    requests.request(metodo, uri, headers=cabeceras, data=cuerpo_encoded, allow_redirects=False, timeout=60)

def descargar_datos():
    """
    Descarga los 100 ultimos datos a un archivo csv con las columnas timestamp, cpu y ram desde ThingSpeak.
    
    Returns:
        None
    """
    print("Descargando datos...")
    metodo = 'GET'
    uri = f"https://api.thingspeak.com/channels/{id}/feeds.json?api_key={read_api_key}&results=100"
    respuesta=requests.request(metodo, uri, allow_redirects=False, timeout=60)
    
    if respuesta.status_code == 200:
        response_json = respuesta.json()
        feeds = response_json['feeds']
        csv_data = "timestamp,cpu,ram\n"
        for feed in feeds:
            timestamp = feed['created_at']
            cpu = feed['field1']
            ram = feed['field2']
            csv_data += f"{timestamp},{cpu},{ram}\n"
        with open("data.csv", "w", encoding="UTF-8") as file:
            file.write(csv_data)
    else:
        print("Error al descargar los datos.")

# Programa principal
if __name__ == "__main__":
    if not os.path.exists("data.txt"):
        print("No se han encontrado datos guardados.")
        crear_canal()
        cargar_canal_data()
    else:
        print("Comprobando datos guardados...")
        if comprobar_canal_data():
            print("Usando canal creado previamente...")
            cargar_canal_data()
        else:
            print("Datos incorrectos.")
            print("Deseas borrar el datos.txt [Y/N]")
            respuesta = input()
            if respuesta.lower() == "y":
                os.remove("data.txt")
                print("Archivo 'data.txt' eliminado.")
                print("Deseas crear un nuevo canal [Y/N]")
                respuesta = input()
                if respuesta.lower() == "y":
                    crear_canal()
                    cargar_canal_data()
                else:
                    sys.exit(1)
            else:
                sys.exit(1)
    print("Iniciando subida de datos...")
    print("Pulsa Ctrl+C para terminar el programa.")
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        subir_datos()
        time.sleep(15)
