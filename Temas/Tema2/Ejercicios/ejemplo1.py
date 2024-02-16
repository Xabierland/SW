import requests
from bs4 import BeautifulSoup

response = requests.get('http://www.google.com')

if response.status_code == 200:
    html = BeautifulSoup(response.content, 'html.parser')
    
    # Imprime la cabecera de la página
    #print(html.head)
    #for tag in html.head:
    #    print(tag)
    
    # Imprime el cuerpo de la página
    #print(html.body)
    
    # Imprime el título de la página
    #print(html.head.title)
    #print(html.head.title.string)
    
    # Imprime todos los enlaces de la página
    #for enlace in html.find_all('a'):
    #    print(enlace.get('href'))
    #    print("")
      
    # Imprime todos los divs de la página  
    #for div in html.find_all('div'):
    #    print(div)
    #    print("")
    
    # Imprime todos los divs de la página con atributo class
    for div in html.find_all('div', class_=''):
        print(div)
        print("")