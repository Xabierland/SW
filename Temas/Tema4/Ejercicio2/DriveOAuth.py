#-*- coding: utf-8 -*-
import urllib.parse
import requests
import webbrowser
import time
from socket import AF_INET, socket, SOCK_STREAM
import json

def get_oauth():
    uri = "https://accounts.google.com/o/oauth2/v2/auth"
    datos = {
        "client_id": client_id,
        "redirect_uri": "http://localhost:8090",
        "response_type": "code",
        "scope": scope
    }
    datos_encode = urllib.parse.urlencode(datos)

    print("\tOpenning browser...")
    webbrowser.open_new(uri + "?" + datos_encode)
    print("\Creando servidor en localhost:8090")
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', 8090))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()
    peticion = client_socket.recv(1024)
    
    print("\Recibimos el codigo de autenticacion:")
    primera_linea = peticion.decode('UTF8').split('\n')[0]
    aux_auth_code = primera_linea.split(' ')[1]
    auth_code = aux_auth_code[7:].split('&')[0]
    print ("\t"+auth_code)

    # Devolver una respuesta al usuario y cerrar conexion y sockets
    http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                    "<html>" \
                    "<head><title>Prueba</title></head>" \
                    "<body>The authentication flow has completed. Close this window.</body>" \
                    "</html>"
    client_socket.sendall(http_response.encode('UTF8'))
    time.sleep(1)
    client_socket.close()
    server_socket.close()
    return auth_code
    
def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": auth_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost:8090",
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    return response.json()["access_token"]

def create_folder(folder_name):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    data = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    response = requests.post("https://www.googleapis.com/drive/v3/files", headers=headers, json=data)
    if response.status_code == 200:
        folder_id = response.json()["id"]
        print("\tCarpeta creada. Folder ID:", folder_id)
        return folder_id
    else:
        print("\tFallo al crear la carpeta.")
        return None

def create_text_file(folder_id, file_name):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    data = {
        "name": file_name,
        "parents": [folder_id],
        "mimeType": "text/plain"
    }
    response = requests.post("https://www.googleapis.com/drive/v3/files", headers=headers, json=data)
    if response.status_code == 200:
        file_id = response.json()["id"]
        print("\tArchivo creado con éxito. File ID:", file_id)
        return file_id
    else:
        print("\tFallo al crear el archivo.")
        return None

def download_file(file_id, file_name):
    """Descargar un archivo de una carpeta de google drive"""
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    params = {
        "alt": "media"
    }
    response = requests.get(f"https://www.googleapis.com/drive/v3/files/{file_id}", headers=headers, params=params)

    if response.status_code == 200:
        with open(file_name+".txt", "wb") as f:
            f.write(response.content)
        print("\tFile downloaded successfully.")
    else:
        print("\tFailed to download file.")
        print(response.text)

def share_file(file_id, mail):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    data = {
        "role": "writer",
        "type": "user",
        "emailAddress": mail
    }
    response = requests.post(f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions", headers=headers, json=data)
    if response.status_code == 200:
        print("\tFile shared successfully.")
    else:
        print("\tFailed to share file.")
        print(response.text)

def list_file(folder_id):
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    params = {
        "q": f"'{folder_id}' in parents",
        "fields": "files(name)"
    }
    response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
    if response.status_code == 200:
        files = response.json()["files"]
        print("\tArchivos en la carpeta:")
        for file in files:
            print("\t- " + file["name"])
    else:
        print("\tError al lista archivos.")
        print(response.text)

def delete_file(folder_id):
    # Lista los archivos de la carpeta
    list_file(folder_id)
    file_name_to_delete = input("Introduce el nombre del archivo que quieres eliminar: ")
    # Una vez metido un nombre de archivo conseguir su id y lo eliminamos
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    params = {
        "q": f"'{folder_id}' in parents and name='{file_name_to_delete}'",
        "fields": "files(id)"
    }
    response = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers, params=params)
    if response.status_code == 200:
        files = response.json()["files"]
        if len(files) > 0:
            file_id_to_delete = files[0]["id"]
            # Eliminar el archivo con el id
            response = requests.delete(f"https://www.googleapis.com/drive/v3/files/{file_id_to_delete}", headers=headers)
            if response.status_code == 204:
                print("\tArchivo eliminado con éxito.")
            else:
                print("\tFallo al eliminar el archivo.")
                print(response.text)
        else:
            print("\tNo se encontró ningún archivo con ese nombre en la carpeta.")
    else:
        print("\tError al listar archivos.")
        print(response.text)
    # Eliminar el archivo con el id

def upload_file(folder_id, file_name):
    headers = {
        "Authorization": "Bearer " + access_token,
    }
    files = {
        'data': ('metadata', json.dumps({
            'name': file_name,
            'parents': [folder_id],
            "mimeType": "text/plain"
        }), 'application/json'),
        'file': open(file_name, 'rb')
    }
    response = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)
    if response.status_code == 200:
        file_id = response.json()["id"]
        print("\tArchivo subido con éxito. File ID:", file_id)
        return file_id
    else:
        print("\tFallo al subir el archivo.")
        print(response.text)
    
if __name__ == "__main__":
    # Paso 1
    print("\nPaso 1. Prerequisitos en Google Cloud Console")
    print("\Cargando datos")
    auth_code = ""
    scope = "https://www.googleapis.com/auth/drive"
    with open("secret.json") as f:
        secret = json.load(f)
        client_id = secret["installed"]["client_id"]
        client_secret = secret["installed"]["client_secret"]
    print("\tDatos cargados")
    
    # Paso 2
    print("\nPaso 2.- Obtenemos el código de autorización")
    auth_code=get_oauth()
    
    # Paso 3
    print("\nPaso 3.- Obtenemos el token de acceso")
    access_token = get_access_token()

    # Paso 4
    # Editar Google Drive
    print("\nPaso 4.- Editar Google Drive")
    folder_name = input("Introduce el nombre de la carpeta: ")
    folder_id = create_folder(folder_name)
    while True:
        respuesta=input("¿Que quieres hacer? [Listar/Subir/Crear/Eliminar/Salir]")
        if respuesta.upper() == "CREAR":
            # Crea un archivo de Google Docs dentro de la carpeta
            while True:
                file_name = input("Introduce el nombre del archivo: ")
                file_id = create_text_file(folder_id, file_name)
                
                respuesta=input("[Y/N] ¿Quieres descargar el archivo? ")
                if respuesta.upper() != "Y":
                    pass
                else:
                    # Descargamos el archivo
                    download_file(file_id, file_name)
                respuesta=input("[Y/N] ¿Quieres compartir el archivo? ")
                if respuesta.upper() != "Y":
                    pass
                else:
                    # Compartir el archivo por correo
                    mail = input("Introduce el correo al que quieres compartir el archivo: ")
                    # andergorocica@gmail.com
                    share_file(file_id, mail)
                respuesta=input("[Y/N] ¿Quieres crear otro archivo? ")
                if respuesta.upper() != "Y":
                    break
        elif respuesta.upper() == "SUBIR":
            while True:
                nombre_archivo = input("Introduce el nombre del archivo que quieres subir: ")
                file_id = upload_file(folder_id, nombre_archivo)
                respuesta=input("[Y/N] ¿Quieres compartir el archivo? ")
                if respuesta.upper() != "Y":
                    pass
                else:
                    # Compartir el archivo por correo
                    mail = input("Introduce el correo al que quieres compartir el archivo: ")
                    share_file(file_id, mail)
                respuesta=input("[Y/N] ¿Quieres subir otro archivo? ")
                if respuesta.upper() != "Y":
                    break
        elif respuesta.upper() == "LISTAR":
            list_file(folder_id)
        elif respuesta.upper() == "ELIMINAR":
            delete_file(folder_id)
        elif respuesta.upper() == "SALIR":
            print("\nFin del programa")
            exit(0)
        else: 
            print("\nOpción no válida")        
        
    
   
    
    
