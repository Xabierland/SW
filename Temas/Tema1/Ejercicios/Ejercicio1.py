import requests

nombre = input("Ingrese un nombre o apellido: ")
url = 'https://www.ehu.eus/bilatu/buscar/sbilatu.php?lang=es1'
data = {
    'bidali': 'BUSCAR',
    'abi_ize': nombre,
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

response = requests.post(url, data=data)
with open('Ejercicio1.html', 'w') as file:
    file.write(response.text)