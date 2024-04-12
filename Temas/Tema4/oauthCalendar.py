#-*- coding: utf-8 -*-
import urllib.parse
import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json


auth_code = ""
print("###################################")
print("OAuth 2.0 for Mobile & Desktop Apps")
print("###################################")
# https://developers.google.com/identity/protocols/oauth2/native-app

print("\nStep 1.- Prerequisites on Google Cloud Console") # https://developers.google.com/identity/protocols/oauth2/native-app#prerequisites



print("\tEnable APIs for your project") # https://developers.google.com/identity/protocols/oauth2/native-app#enable-apis



print("\tIdentify access scopes") # https://developers.google.com/identity/protocols/oauth2/native-app#identify-access-scopes
scope = "https://www.googleapis.com/auth/calendar.calendarlist.readonly" # Lista los calendarios de google

print("\tCreate authorization credentials")
# https://developers.google.com/identity/protocols/oauth2/native-app#creatingcred
# Read the secret.json file
with open("secret.json") as f:
    secret = json.load(f)
    client_id = secret["installed"]["client_id"]
    client_secret = secret["installed"]["client_secret"]
print("\tConfigure OAuth consent screen")
print("\tAdd access scopes and test users")

print("\nStep 2.- Send a request to Google's OAuth 2.0 server")
# https://developers.google.com/identity/protocols/oauth2/native-app#step-2:-send-a-request-to-googles-oauth-2.0-server
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

print("\nStep 3.- Google prompts user for consent")

print("\nStep 4.- Handle the OAuth 2.0 server response")
# https://developers.google.com/identity/protocols/oauth2/native-app#handlingresponse
# Crear servidor local que escucha por el puerto 8090

print("\tLocal server listening on port 8090")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localhost', 8090))
server_socket.listen(1)

# Recibir la solicitude 302 del navegador

client_socket, client_address = server_socket.accept()
peticion = client_socket.recv(1024)
print("\tRequest from the browser received at local server:")

# Buscar en la petición el "auth_code"
primera_linea = peticion.decode('UTF8').split('\n')[0]
aux_auth_code = primera_linea.split(' ')[1]
auth_code = aux_auth_code[7:].split('&')[0]
print ("\tauth_code: " + auth_code)

# Devolver una respuesta al usuario y cerrar conexion y sockets
http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                "<html>" \
                "<head><title>Prueba</title></head>" \
                "<body>The authentication flow has completed. Close this window.</body>" \
                "</html>"
client_socket.sendall(http_response.encode('UTF8'))
client_socket.close()
server_socket.close()

print("\nStep 5.- Exchange authorization code for refresh and access tokens")
# https://developers.google.com/identity/protocols/oauth2/native-app#exchange-authorization-code

token_url = "https://oauth2.googleapis.com/token"
data = {
    "code": auth_code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": "http://localhost:8090",
    "grant_type": "authorization_code"
}
response = requests.post(token_url, data=data)
tokens = response.json()
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)


input("The authentication flow has completed. Close browser window and press enter to continue...")


print("\nStep 6.- Calling Google APIs")
# Calendar API: https://developers.google.com/calendar/v3/reference
# CalendarList: https://developers.google.com/calendar/v3/reference#CalendarList
# CalendarList:list: https://developers.google.com/calendar/v3/reference/calendarList/list

# Make a request to the CalendarList API
calendar_list_url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(calendar_list_url, headers=headers)
calendar_list = response.json()

# Display the content of the CalendarList
print("Calendar List:")
for calendar in calendar_list["items"]:
    print(calendar["summary"])

