"""
Autor: Xabier Gabiña Barañano
Fecha: 25/04/2024
Descripción: Programar una aplicación que permita al usuario autenticarse en Dropbox para realizar diferentes operaciones.
"""

import requests
import json
import webbrowser
from socket import socket, AF_INET, SOCK_STREAM
import urllib.parse

# OAuth

def get_dropbox_auth_flow():
    """
    Crea el servidor web de autenticación de Dropbox y devuelve el flujo de autenticación utilizando unicamente peticiones HTTP con request.
    """
    
    # Obtiene la URL de autorización de Dropbox
    url = f"https://www.dropbox.com/oauth2/authorize?response_type=code&client_id={app_key}&redirect_uri={urllib.parse.quote(redirect_uri)}"
    
    # Crea el servidor web
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("localhost", 8090))
    server.listen(1)
    
    # Abre el navegador web para que el usuario pueda autenticarse
    webbrowser.open(url)
    
    # Recibir la solicitude 302 del navegador
    ## FALTA CÓDIGO
    client_connection, client_address = server.accept()
    peticion = client_connection.recv(1024)

    # Buscar en la petición el "auth_code"
    ## FALTA CÓDIGO
    primera_liena = peticion.decode('UTF8').split('\n')[0]
    aux_auth_code = primera_liena.split(' ')[1]
    auth_code = aux_auth_code[7:].split('&')[0]

    # Devolver una respuesta al usuario
    http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                    "<html>" \
                    "<head><title>Prueba</title></head>" \
                    "<body>The authentication flow has completed. Close this window.</body>" \
                    "</html>"
    client_connection.sendall(http_response.encode(encoding="utf-8"))
    client_connection.close()
    server.close()
    
    return auth_code

def get_access_token(auth_code):
    params = {
        'code': auth_code,
        'grant_type': 'authorization_code',
        'client_id': app_key,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri
    }
    cabeceras={
        'User-Agent': 'Python Client',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    uri = 'https://api.dropboxapi.com/oauth2/token'
    response = requests.post(uri, data=params, headers=cabeceras)
    json_response = json.loads(response.content)
    access_token = json_response['access_token']
    return access_token

# Menu de acciones

def menu(access_token):
    print("\033[H\033[J")
    while True:
        print("\n\n=== Menú de acciones ===")
        print("1. Listar archivos")
        print("2. Subir archivo")
        print("3. Descargar archivo")
        print("4. Salir")
        
        opcion = input("Introduce una opción: ")
        
        if opcion == "1":
            listar_archivos(access_token)
        elif opcion == "2":
            subir_archivos(access_token)
        elif opcion == "3":
            descargar_archivos(access_token)
        elif opcion == "4":
            break
        else:
            print("Opción incorrecta")

def listar_archivos(access_token):
    """
    Listar los archivos y carpetas de la raiz de Dropbox.
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.dropboxapi.com/2/files/list_folder'
    data = {
        'path': '',
        'recursive': False,
        'include_media_info': False,
        'include_deleted': False,
        'include_has_explicit_shared_members': False,
        'include_mounted_folders': True,
        'include_non_downloadable_files': True
    }
    response = requests.post(url, headers=headers, json=data)
    json_response = json.loads(response.content)
    for entry in json_response['entries']:
        print("\t- "+entry['name'])

def subir_archivos(access_token):
    """
    Listo los elementos de la carpeta actual y sube un archivo.
    """
    file_path = input("Introduce la ruta del archivo que deseas subir: ")
    
    upload_url = 'https://content.dropboxapi.com/2/files/upload'
    upload_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': json.dumps({'path': file_path})
    }
    
    try:
        with open(file_path, 'rb') as f:
            upload_response = requests.post(upload_url, headers=upload_headers, data=f)
        
        if upload_response.status_code == 200:
            print("Archivo subido exitosamente.")
        else:
            print("Error al subir el archivo.")
    except FileNotFoundError:
        print("Archivo no encontrado.")

def descargar_archivos(access_token):
    """
    Muestra los archivos y despues de elegir uno lo descarga.
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.dropboxapi.com/2/files/list_folder'
    data = {
        'path': '',
        'recursive': False,
        'include_media_info': False,
        'include_deleted': False,
        'include_has_explicit_shared_members': False,
        'include_mounted_folders': True,
        'include_non_downloadable_files': True
    }
    response = requests.post(url, headers=headers, json=data)
    json_response = json.loads(response.content)
    for i, entry in enumerate(json_response['entries']):
        print(f"{i+1}. {entry['name']}")
    
    opcion = input("Selecciona el número del archivo que deseas descargar: ")
    try:
        opcion = int(opcion)
        if opcion < 1 or opcion > len(json_response['entries']):
            print("Opción inválida")
            return
    except ValueError:
        print("Opción inválida")
        return
    
    selected_file = json_response['entries'][opcion-1]
    file_path = selected_file['path_display']
    
    download_url = 'https://content.dropboxapi.com/2/files/download'
    download_headers = {
        'Authorization': f'Bearer {access_token}',
        'Dropbox-API-Arg': json.dumps({'path': file_path})
    }
    download_response = requests.post(download_url, headers=download_headers)
    
    if download_response.status_code == 200:
        with open(selected_file['name'], 'wb') as f:
            f.write(download_response.content)
        print(f"Archivo '{selected_file['name']}' descargado exitosamente.")
    else:
        print("Error al descargar el archivo.")

# Main

if __name__ == "__main__":
    # Lee las credenciales del secret.json
    with open("secret.json") as f:
        secret = json.load(f)
        app_key = secret["app_key"]
        app_secret = secret["app_secret"]
        redirect_uri = secret["redirect_uri"]
    
    # Flujo de autenticación
    auth_code = get_dropbox_auth_flow()
    
    print(f"Token de acceso: {auth_code}")
    
    access_token = get_access_token(auth_code)
    
    print(f"Token de acceso: {access_token}")
    
    # Iniciamos el menu de acciones
    menu(access_token)