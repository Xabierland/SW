# 1. Tema 1

- [1. Tema 1](#1-tema-1)
  - [1.1. Teoria](#11-teoria)
  - [1.2. Ejercicios](#12-ejercicios)
    - [1.2.1. Burpsuite Repeater](#121-burpsuite-repeater)
    - [1.2.2. Python](#122-python)

## 1.1. Teoria

## 1.2. Ejercicios

### 1.2.1. Burpsuite Repeater

#### Obtener el directorio raíz de un servidor web <!-- omit from toc -->

```http
GET / HTTP/1.1
Host: www.ehu.eus


```

#### Obtener el svg de twitter <!-- omit from toc -->

```http
GET /o/upv-ehu-campusa-theme/images/custom/campusa/ic-twitter.svg HTTP/1.1
Host: www.ehu.eus


```

#### Mandar formulario con GET <!-- omit from toc -->

```http
GET /processForm?dni=11111111 HTTP/1.1
Host: gae-sw-2017.appspot.com

```

#### Mandar formulario con POST <!-- omit from toc -->

```http
POST /processForm HTTP/1.1
Host: gae-sw-2017.appspot.com
Content-Length: 12

dni=11111111
```

#### Login en egela <!-- omit from toc -->

```http
GET /login/index.php HTTP/1.1
host: egela.ehu.eus


```

```http
POST /login/index.php HTTP/1.1
Host: egela.ehu.eus
Content-Type: application/x-www-form-urlencoded
Cookie: MoodleSessionegela=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

username=alumno&password=alumno&logintoken=XXXXXXXX
```

```http
GET /login/index.php?testsession=XXXXX HTTP/1.1
host: egela.ehu.eus
cookie: MoodleSessionegela=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


```

```http
GET / HTTP/1.1
host: egela.ehu.eus
cookie: MoodleSessionegela=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


```

### 1.2.2. Python

#### Obtener el aspx de Chunked <!-- omit from toc -->

```python
import requests

metodo="GET"
uri="https://www.httpwatch.com/httpgallery/chunked/chunkedimage.aspx"
cabeceras={'Host': 'www.httpwatch.com'}
cuerpo=""
response = requests.request(metodo, uri, headers=cabeceras, data=cuerpo)

i=0
print("Status: " + str(response.status_code))
print("Reason: " + response.reason)
for cabecera in response.headers:
    i+=1
    print(str(i)+ " " + cabecera + ": " + response.headers[cabecera])

fichero = open("imagen.jpg", "wb")
fichero.write(response.content)
fichero.close()
```

#### Seguir redirecciones manualmente <!-- omit from toc -->

```python
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
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

print(respuesta.status_code)
print(respuesta.headers)
i=0
for cabeceras in respuesta.headers:
    i += 1
    print(i, cabeceras, respuesta.headers[cabeceras])
print(respuesta.text)

print("===TERCERA RESPUESTA===")
metodo = "GET"
uri = respuesta.headers['Location']
cabeceras = {'Host' : uri.split('/')[2]}
cuerpo = ""
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

print(respuesta.status_code)
print(respuesta.headers)
i=0
for cabeceras in respuesta.headers:
    i += 1
    print(i, cabeceras, respuesta.headers[cabeceras])
print(respuesta.text)

fichero = open("ejemplo2.html", "wb")
fichero.write(respuesta.content)
fichero.close()
```

#### Obtener la letra del DNI con GET <!-- omit from toc -->

```python
import requests

numero = input("Ingrese un número: ")
metodo="GET"
uri="http://gae-sw-2017.appspot.com/processForm?dni="+numero
cabecera={"Host": "gae-sw-2017.appspot.com", "Content-Lenght": "12"}
cuerpo=""

respuesta = requests.request(metodo, uri, headers=cabecera, data=cuerpo, allow_redirects=False)

print("DNI: " + respuesta.text)
```

#### Obtener la letra del DNI con POST <!-- omit from toc -->

```python
import requests

numero = input("Ingrese un número: ")
metodo="POST"
uri="http://gae-sw-2017.appspot.com/processForm"
cabecera={"Host": "gae-sw-2017.appspot.com", "Content-Lenght": "12", "Content-Type": "application/x-www-form-urlencoded"}
cuerpo="dni="+numero

respuesta = requests.request(metodo, uri, headers=cabecera, data=cuerpo, allow_redirects=False)

print("DNI: " + respuesta.text)
```
