# -*- coding: utf-8 -*-
"""
Este archivo contiene un programa que realiza una búsqueda en el sitio web 
'https://www.ehu.eus/bilatu/buscar/sbilatu.php?lang=es1'
utilizando el método 'POST' y los parámetros proporcionados en el cuerpo de
la solicitud.
El programa recibe un nombre o apellido como argumento en la línea de comandos
, o solicita al usuario que ingrese uno si no se proporciona.
Luego, envía una solicitud HTTP al sitio web con los parámetros proporcionados
y guarda la respuesta en un archivo llamado 'Ejercicio1.html'.
"""

import sys
import requests
from bs4 import BeautifulSoup

def get_nombre_from_args():
    """
    Obtiene el nombre pasado como argumento en la línea de comandos.

    Returns:
        str: El nombre pasado como argumento si existe, None en caso contrario.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]
    return None

def print_request_info(response):
    """
    Imprime la información de una solicitud HTTP.

    Args:
        response: La respuesta de la solicitud HTTP.

    Returns:
        None
    """
    print(f"Request URL: {response.url}")
    print(f"Request code: {response.status_code}")
    print(f"Request reason: {response.reason}")
    for head in response.headers:
        print(f"Header: {head}: {response.headers[head]}")
    print(f"Request content: {response.text}")

def bilatu(p_nombre, print_info=True):
    """
    Esta función realiza una búsqueda en el sitio web 
    'https://www.ehu.eus/bilatu/buscar/sbilatu.php?lang=es1'
    utilizando el método 'POST' y los parámetros proporcionados
    en el cuerpo de la solicitud.
    
    Parámetros:
        - p_nombre: El nombre o apellido a buscar.
        - print_info: Un valor booleano que indica si se debe imprimir información adicional. 
                      Por defecto, es True.
    
    La función envía una solicitud HTTP al sitio web con los parámetros
    proporcionados y devuelve la respuesta.
    Además, guarda la respuesta en un archivo llamado 'Ejercicio1.html'.
    """
    if not p_nombre:
        p_nombre = input("Ingrese un nombre o apellido: ")
    metodo='POST'
    url = 'https://www.ehu.eus/bilatu/buscar/sbilatu.php?lang=es1'
    cabecera = {
        'Host': 'www.ehu.eus',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cuerpo = {
        'bidali': 'BUSCAR',
        'abi_ize': p_nombre,
        'ize': '',
        'abi1': '',
        'abi2': '',
        'tlf': '',
        'email': '',
        'a01': '',
        'a02': '',
        'a03': '',
        'a04': '',
        'a07': '',
        'a08': '',
        'a10': ''
    }

    response = requests.request(metodo, url, headers=cabecera, data=cuerpo, timeout=60)
    if print_info:
        print_request_info(response)
        with open('Ejercicio1.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
            file.close()
    return response

def sacarNombres(html):
    """
    Esta función recibe el contenido de un archivo HTML y extrae los nombres
    y apellidos de las personas encontradas en la búsqueda.
    """
    documento = BeautifulSoup(html, 'html.parser')
    lista_nombres = documento.find_all('td', {'class': 'fondo_listado'})
    for nombre in lista_nombres:
        print(nombre.text + "\t" + "https://www.ehu.eus" + nombre.a['href'])

if __name__ == '__main__':
    nombre=get_nombre_from_args()
    respuesta=bilatu(nombre, False)
    sacarNombres(respuesta.text)
    