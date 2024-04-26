# -*- coding: utf-8 -*-
"""
Nombre y apellidos: Xabier Gabiña Barañano
Asignatura y grupo: Sistemas Web, Grupo 01
Fecha: 11/03/2024
Nombre de la tarea: Práctica 2 | Buscar Información en eGela

La practica consiste en descargar los archivos con formato PDF de la asignatura de Sistemas Web del moodle de la UPV/EHU.
"""
import requests
import bs4
import getpass
import os
import sys
from tqdm import tqdm

asignatura = "Sistemas Web"

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

def download_all_pdf(cookie, secciones):
    """
    Descarga todos los archivos PDF de las secciones especificadas.

    Args:
        cookie (str): La cookie de autenticación para realizar las peticiones.
        secciones (dict): Un diccionario que contiene las secciones como claves y los enlaces a las secciones como valores.

    Returns:
        None
    """
    
    # Por cada elemento del diccionario "secciones" hacemos una peticion para obtener los enlaces a los archivos PDF
    # Creamos una carpeta con el nombre de la clave del diccionario "secciones"
    # Por cada enlace a un archivo PDF hacemos una peticion para descargarlo

    for key, value in tqdm(secciones.items(), desc="Descargando archivos PDF"):
        os.makedirs(asignatura+"/"+key, exist_ok=True)
        metodo = 'GET'
        uri = value
        cabeceras = {
            'Cookie': f'MoodleSessionegela={cookie}'
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
                    # Descargamos el archivo PDF
                    pdf_response = requests.request('GET', pdf, headers=cabeceras, allow_redirects=False)
                    pdf_link = requests.request('GET', pdf_response.headers['Location'], headers=cabeceras, allow_redirects=False)
                    if pdf_response.status_code == 303 and pdf_link.status_code == 200:
                        with open(f"{asignatura}/{key}/{name}.pdf", 'wb') as f:
                            f.write(pdf_link.content)  # Write the response content as binary data
                    else:
                        print(f"Error al descargar {pdf}")

def listar_tareas(cookie, secciones):
    # Crear un documento csv con todas las tareas a realizar en el curso.
    # Seccion | Titulo | Fecha de entrega | Enlace

    with open(asignatura+'/tareas.csv', 'w', encoding='utf-8') as f:
        f.write('Seccion,Titulo,Fecha de entrega,Enlace\n')
        for key, value in tqdm(secciones.items(), desc="Guardando tareas"):
            metodo = 'GET'
            uri = value
            cabeceras = {
                'Cookie': f'MoodleSessionegela={cookie}'
            }
            respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
            if respuesta.status_code == 200:
                soup = bs4.BeautifulSoup(respuesta.text, 'html.parser')
                ul = soup.find('ul', class_='topics')
                lis = ul.find_all('li', class_='activity assign modtype_assign')
                for li in lis:
                    if li.find('a'):
                        a = li.find('a')
                        tarea = a['href']
                        name = a.find('span').text
                        tarea_response = requests.request('GET', tarea, headers=cabeceras, allow_redirects=False)
                        if tarea_response.status_code == 200:
                            tarea_soup = bs4.BeautifulSoup(tarea_response.text, 'html.parser')
                            tr = tarea_soup.find_all('tr')
                            for t in tr:
                                th = t.find('th')
                                if th.text == 'Fecha de entrega':
                                    fecha = t.find('td').text.replace(',', '')
                                    f.write(f'{key},{name},{fecha},{tarea}\n')

if __name__ == "__main__":
    
    ldapuser = sys.argv[1]
    ldappass = getpass.getpass('Introduce tu contraseña LDAP: ')
    username = sys.argv[2]

    # Iniciamos sesion en eGela
    try:
        print("\n- Iniciando sesion en eGela...")
        MoodleSessionegela=login(username.upper(), ldapuser, ldappass)
    except:
        print("Error al iniciar sesion.")
        exit(1)

    # Exploramos eGela y obtenemos los enlaces a las secciones
    try:
        print("- Explorando eGela...")
        secciones=explorar_eGela(MoodleSessionegela)
        # Imprimimos las secciones línea a línea
        for section, link in secciones.items():
            print(f"\t{section.ljust(15)} -> {link}")
    except Exception as e:
        print("Error al explorar eGela.")
        print(e)
        exit(1)

    # Creamos la carpeta
    os.makedirs(asignatura, exist_ok=True)

    # Descargamos todos los archivos PDF de las secciones
    try:
        print("\n- Iniciando descarga de archivos PDF...")
        download_all_pdf(MoodleSessionegela, secciones)
        print("Descarga de archivos completada.")
    except KeyboardInterrupt:
        print("Descarga de archivos cancelada.")
        exit(0)
    except Exception as e:
        print("Error al descargar archivos PDF.")
        print(e)
        exit(1)

    # Listamos las tareas a realizar en el curso
    try:
        print("\n- Guardando tareas a realizar en el curso...")
        listar_tareas(MoodleSessionegela, secciones)
        print("Listado de tareas guardado.")
    except KeyboardInterrupt:
        print("Guardado de tareas cancelado.")
        exit(0)
    except Exception as e:
        print("Error al guardar tareas.")
        print(e)
        exit(1)
