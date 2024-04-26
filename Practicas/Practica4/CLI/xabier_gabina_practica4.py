"""
Autor: Xabier Gabiña Barañano
Asignatura y grupo: Sistemas Web, Grupo 01
Fecha: 26/04/2024
Nombre de la tarea: Actividad 4 - 
Descripción: Programa que integra eGela con Dropbox para subir archivos a Dropbox automáticamente.
"""

# Librerias

import requests
import json
import webbrowser
from socket import socket, AF_INET, SOCK_STREAM
import urllib.parse
import bs4
import tqdm

# Variables globales

asignatura = "Sistemas Web"

# Dropbox OAuth

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

# Egela Auth

def login(username, ldapuser, ldappass):
    """
    Realiza el proceso de inicio de sesión en el sitio web eGela.

    Parámetros:
    - username (str): El nombre de usuario para autenticarse.
    - ldapuser (str): El nombre de usuario LDAP para autenticarse.
    - ldappass (str): La contraseña LDAP para autenticarse.

    Retorna:
    - MoodleSessionegela (str): El valor de la cookie MoodleSessionegela, que se utiliza para mantener la sesión.

    """
    # Primera peticion - Obtener MoodleSessionegela y logintoken
    metodo = 'GET'
    uri = "https://egela.ehu.eus/login/index.php"
    respuesta1=requests.request(metodo, uri, allow_redirects=False, timeout=60)
    
    print(f'Solicitud1:\n\t{metodo} {uri}')
    print(f'Respuesta1:\n\t{respuesta1.status_code} {respuesta1.reason}')

    if respuesta1.status_code == 200:
        ## Obtenemos la MoodleSessionegela y el logintoken
        ### Cabecera SetCookie: MoodleSessionegela
        MoodleSessionegela = respuesta1.headers['Set-Cookie'].split('MoodleSessionegela=')[1].split(';')[0]
        ### logintoken campo input del fomulario
        logintoken = respuesta1.text.split('logintoken" value="')[1].split('"')[0]
    else:
        print("Error al obtener MoodleSessionegela y logintoken.")
        print(respuesta1.status_code)
        exit(1)
    
    # Segunda peticion - Autenticacion
    metodo = 'POST'
    uri = "https://egela.ehu.eus/login/index.php"
    cabeceras = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
    }
    cuerpo = {
        'username': ldapuser,
        'password': ldappass,
        'logintoken': logintoken
    }
    respuesta2 = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

    print('==================================================')
    print(f'Solicitud2:\n\t{metodo} {uri}')
    print(f'\t{cuerpo}')
    print(f'Respuesta2:\n\t{respuesta2.status_code} {respuesta2.reason}')
    print(f'\t{respuesta2.headers["Location"]}\n\t{respuesta2.headers["Set-Cookie"]}')

    if respuesta2.status_code == 303:
        # Obtenemos la cabecera Location
        location = respuesta2.headers['Location']
        MoodleSessionegela = respuesta2.headers['Set-Cookie'].split('MoodleSessionegela=')[1].split(';')[0]
    else:
        print("Error al autenticarse. Revisa tus credenciales.")
        print(respuesta2.status_code)
        exit(1)
    
    # Tercera peticion - Validar la sesion
    metodo = 'GET'
    uri = location
    cabeceras = {
        'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
    }
    respuesta3 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

    print('==================================================')
    print(f'Solicitud3:\n\t{metodo} {uri}')
    print(f'Respuesta3:\n\t{respuesta3.status_code} {respuesta3.reason}')
    print(f'\t{respuesta3.headers["Location"]}')

    if respuesta3.status_code != 303:
        print("Error al autenticarse. Revisa tus credenciales.")
        print(respuesta3.status_code)
        #print(respuesta3.text)
        exit(1)
    else:
        # Obtenemos la cabecera Location
        location = respuesta3.headers['Location']
    
    # Cuarta peticion - Acceder a eGela y buscar mi nombre
    metodo = 'GET'
    uri = location
    cabeceras = {
        'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
    }
    respuesta4 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

    print('==================================================')
    print(f'Solicitud4:\n\t{metodo} {uri}')
    print(f'Respuesta4:\n\t{respuesta4.status_code} {respuesta4.reason}')

    if respuesta4.status_code == 200:
        # Buscamos mi nombre dentro del div class="logininfo"
        if username in respuesta4.text:
            print("Autenticacion correcta.")
            input()
        else:
            print("Error al buscar el nombre. ¿Has escrito correctamente tu nombre?")
            exit(1)
    return MoodleSessionegela

def explorar_eGela(MoodleSessionegela):
    """
    Explora eGela y obtén los enlaces a las secciones.

    Args:
        MoodleSessionegela (str): El ID de sesión de Moodle.

    Returns:
        dict: Un diccionario que contiene los enlaces a las secciones, con el título de la sección como clave y el enlace como valor.
    """
    # Quinta petición - Buscar el enlace a SW
    metodo = 'GET'
    uri = "https://egela.ehu.eus"
    cabeceras = {
        'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
    }
    respuesta4 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    if respuesta4.status_code == 200:
        # Buscamos el enlace a SW
        soup = bs4.BeautifulSoup(respuesta4.text, 'html.parser')
        enlaces = soup.find_all('a')
        for enlace in enlaces:
            if asignatura in enlace.text:
                link_asignatura=enlace.get('href')
    # Sexta petición - Acceder a SW y obtener todos los enlaces a secciones
    metodo = 'GET'
    uri = link_asignatura+'&section=0'
    cabeceras = {
        'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
    }
    secciones = {}  # Define la variable "secciones"
    respuesta6 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    if respuesta6.status_code == 200:
        # Obtenemos los elementos li dentro de la clase ul "nav nav-tabs mb-3"
        # De cada li obtenemos el href y su title del elemento a
        # El resultado se añadira en el diccionario "secciones" con el title del a como clave y el enlace a la seccion como valor
        # Si el a es de la clase "nav-link active" se añade a "secciones" con el title del a como clave y el enlace sw como valor
        soup = bs4.BeautifulSoup(respuesta6.text, 'html.parser')
        if soup.find('ul', class_='nav nav-tabs mb-3') is None:
            secciones[asignatura] = link_asignatura
        else:
            ul = soup.find('ul', class_='nav nav-tabs mb-3')
            lis = ul.find_all('li')
            for li in lis:
                a = li.find('a')
                if a.has_attr('href'):
                    secciones[a['title']] = a['href']
                else:
                    secciones[a['title']] = link_asignatura+'&section=0#tabs-tree-start'
    return secciones

def listar_pdfs(secciones, MoodleSessionegela):
    i=0
    for key, value in tqdm(secciones.items(), desc="Descargando archivos PDF"):
        metodo = 'GET'
        uri = value
        cabeceras = {
            'Cookie': f'MoodleSessionegela={MoodleSessionegela}'
        }
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
        if respuesta.status_code == 200:
            # Buscamos el ul con clase "section img-text"
            # Dentro del ul nos quedamos con los li de clase "activity resource modtype_resource"
            # De esos li elegimos los que en img tienen src "pdf"
            # De esos li que tenga un enlace a un archivo PDF cogemos el href del a y el span con el nombre del archivo
            # Como nos hace una redireccion cogemos el Location de la cabecera que sera el enlace al PDF
            soup = bs4.BeautifulSoup(respuesta.text, 'html.parser')
            ul = soup.find('ul', class_='topics')
            lis = ul.find_all('li', class_='activity resource modtype_resource')
            for li in lis:
                img = li.find('img')
                if 'pdf' in img['src']:
                    a = li.find('a')
                    pdf = a['href']
                    name = a.find('span').text.replace('/', ' ')
                    i+=1
                    print(f'{i}. {name} | {pdf}')

if __name__ == "__main__":
    # Cargamos las credenciales de Dropbox
    # Lee las credenciales del secret.json
    with open("dropbox_secret.json") as f:
        secret = json.load(f)
        app_key = secret["app_key"]
        app_secret = secret["app_secret"]
        redirect_uri = secret["redirect_uri"]
    # Lee las credenciales de eGela
    with open("egela_secret.json") as f:
        secret = json.load(f)
        username = secret["username"].upper()
        ldapuser = secret["ldapuser"]
        ldappass = secret["ldappass"]
        
    # Autenticación en Dropbox
    auth_code = get_dropbox_auth_flow()
    access_token = get_access_token(auth_code)
    
    # Autenticación en eGela
    MoodleSessionegela = login(username, ldapuser, ldappass)
    
    # Mostar el listado de pdfs de eGela
    secciones = explorar_eGela(MoodleSessionegela)
    
    listar_pdfs(secciones, MoodleSessionegela)