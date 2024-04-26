import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

with open('dropbox_secret.json') as f:
    secrets = json.load(f)
    app_key = secrets['app_key']
    app_secret = secrets['app_secret']
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = ""
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # por el puerto 8090 esta escuchando el servidor que generamos
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # recibe la redireccio 302 del navegador
        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)

        # buscar en solicitud el "auth_code"
        primera_linea =peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]

        # devolver una respuesta al usuario
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                    "<html>" \
                    "<head><title>Prueba</title></head>" \
                    "<body>The authentication flow has completed. Close this window.</body>" \
                    "</html>"
        client_connection.sendall(http_response.encode(encoding="utf-8"))
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        # Navegador en localhost + puerto
        url = f"https://www.dropbox.com/oauth2/authorize?response_type=code&client_id={app_key}&redirect_uri={urllib.parse.quote(redirect_uri)}"
        webbrowser.open(url)
        auth_code = self.local_server()
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
        self._access_token = json_response['access_token']

        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        if self._path == "/":
            self._path = ""
        headers = {
        'Authorization': f'Bearer {self._access_token}',
        'Content-Type': 'application/json'
        }
        url = 'https://api.dropboxapi.com/2/files/list_folder'
        data = {
            'path': self._path,
            'recursive': False,
            'include_media_info': False,
            'include_deleted': False,
            'include_has_explicit_shared_members': False,
            'include_mounted_folders': True,
            'include_non_downloadable_files': True
        }
        response = requests.post(url, headers=headers, json=data)
        contenido_json = json.loads(response.content)

        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)

    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/octet-stream',
            'Dropbox-API-Arg': json.dumps({
                'path': file_path,
                'mode': 'add',
                'autorename': True,
                'mute': False
            })
        }
        response = requests.post(uri, headers=headers, data=file_data)
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print("Error uploading file.")

    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'path': file_path
        }
        response = requests.post(uri, headers=headers, json=data)
        if response.status_code == 200:
            print("File deleted successfully.")
        else:
            print("Error deleting file.")

    def create_folder(self, path):
        print("/create_folder")
        uri = 'https://api.dropboxapi.com/2/files/create_folder_v2'
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            'path': path,
            'autorename': False
        }
        response = requests.post(uri, headers=headers, json=data)
        if response.status_code == 200:
            print("Folder created successfully.")
        else:
            print("Error creating folder.")
