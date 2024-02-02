import requests

print("===PRIMERA RESPUESTA===")
metodo = "GET"
uri = "http://egela.ehu.eus/"
cabeceras = {'Host' : 'egela.ehu.eus'}
cuerpo = ""
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)


print(respuesta.status_code)
print(respuesta.headers)
i=0
for cabeceras in respuesta.headers:
    i += 1
    print(i, cabeceras, respuesta.headers[cabeceras])
print(respuesta.text)

print("===SEGUNDA RESPUESTA===")
metodo = "GET"
uri = respuesta.headers['Location']
cabeceras = {'Host' : uri.split('/')[2]}
cuerpo = ""
respuesta2 = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

print(respuesta2.status_code)
print(respuesta2.headers)
i=0
for cabeceras in respuesta2.headers:
    i += 1
    print(i, cabeceras, respuesta2.headers[cabeceras])
print(respuesta2.text)
