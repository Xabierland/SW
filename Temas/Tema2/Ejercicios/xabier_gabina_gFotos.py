# -*- coding: utf-8 -*-
"""
Autor: Xabier Gabiña
Carga google imagenes con el texto que recibe como argumento.
Descargara las primeras 50 imagenes que encuentre.
Para renderizar la pagina web se utilizara selenium.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import urllib.request

def descargarFotos(termino):
    """
    Descarga las primeras 50 imágenes relacionadas con un término de búsqueda desde Google Imágenes.

    Args:
        termino (str): El término de búsqueda para las imágenes.

    Returns:
        None
    """
    
    # Configurar el driver de Selenium
    driver = webdriver.Firefox()
    
    # Resto del código...
def descargarFotos(termino):
    
    # Configurar el driver de Selenium
    driver = webdriver.Firefox()
    
    # Rechazar las cookies
    driver.get("https://www.google.com")
    driver.find_element(By.ID, "L2AGLb").click()
    
    # Navegar a la página de búsqueda de Google Imágenes
    driver.get("https://www.google.com/search?q=" + termino + "&tbm=isch")
    
    # Desplazarse hacia abajo para cargar más imágenes
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    time.sleep(5)

    # Encontrar los elementos de las imágenes
    imagenes = driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')

    # Descargar las primeras 50 imágenes
    for i, imagen in enumerate(imagenes[:50]):
        # Obtener la URL de la imagen
        url = imagen.get_attribute("src")
        
        # Si la imagen no tiene atributo src, obtener la URL de data-src
        if not url:
            url = imagen.get_attribute("data-src")
        
        # Descargar la imagen y guardarla en la carpeta "img"
        urllib.request.urlretrieve(url, f"img/imagen{i+1}.jpg")
        
        print(f"Descargada imagen {i+1}")

    # Cerrar el driver de Selenium
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        termino = " ".join(sys.argv[1:])
        descargarFotos(termino)
    else:
        print("Debe proporcionar un término de búsqueda como argumento.")