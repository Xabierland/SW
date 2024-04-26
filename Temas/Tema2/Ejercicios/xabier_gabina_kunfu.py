# -*- coding: utf-8 -*-
"""
Autor: Xabier Gabiña
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request

def kunfu():
    """
    Manda usando requests una petición POST a la url.
    La pagina web es un formulario que al responder correctamente (a, b y c) nos redirige a una nueva página.
    Esta pagina renderiza una imagen con javascript.
    Debe descargar la imagen y guardarla como "kunfu.jpg".
    Para ello se debe usar selenium para renderizar la pagina web.

    url = 'https://ws-repasohttp.appspot.com/html/inprimakia.html'
    """
    
    # Enviar una petición POST al formulario
    metodo='POST'
    url = 'https://ws-repasohttp.appspot.com/processForm'
    cabecera = {
        'Host': 'ws-repasohttp.appspot.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    cuerpo = {
        'erantzuna': ['a', 'b', 'c']
    }
    response = requests.request(metodo, url, headers=cabecera, data=cuerpo, allow_redirects=False)
    
    if response.status_code == 302:
        # Obtener del campo location la url a la que se redirige
        redirected_url = response.headers['Location']
        
        # Iniciar el navegador web con Selenium
        driver = webdriver.Firefox()
        
        # Cargar la página redirigida en el navegador
        driver.get("https://ws-repasohttp.appspot.com"+redirected_url)
        
        # Esperar a que la página se cargue completamente
        time.sleep(5)
        
        # Obtener la URL de la imagen
        image_element = driver.find_element(By.TAG_NAME, 'img')
        image_url = image_element.get_attribute('src')
        
        # Descargar la imagen y guardarla como "kunfu.jpg"
        urllib.request.urlretrieve(image_url, "kunfu.jpg")
        
        # Cerrar el navegador
        driver.quit()
    
if __name__ == "__main__":
    kunfu()