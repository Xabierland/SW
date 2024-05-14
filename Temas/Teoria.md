<!--markdownlint-disable-file MD041-->
# Teoria Sistemas Web <!-- omit from toc -->

> [!WARNING]
> Me voy a tomar licencias creativas para explicar las cosas ya que no me gusta mucho como esta explicado en las diapositivas.

- [1. HTTP](#1-http)
  - [1.1. Teoria](#11-teoria)
  - [1.2. Ejercicios](#12-ejercicios)
    - [1.2.1. Burp Suite](#121-burp-suite)
    - [1.2.2. Python](#122-python)
- [2. Web Scraping](#2-web-scraping)

# 1. HTTP

## 1.1. Teoria

La web se basa en el intercambio de información.
Hay diferentes formas de intercambiar información pero la que nos atañe es HTTP.

HTTP es un protocolo de la capa de aplicación que busca obtener información en forma de hipertexto (recursos de la web) para mostrarlos en la aplicación que lo integra (navegadores normalmente).

HTTP sigue el modelo petición-respuesta. Un cliente hace una petición a un servidor y el servidor le responde.
La petición mas común coje dos parametros, el metodo y la URI.

- Metodos:
  - Los metodos más comunes son:
    - GET: Para obtener información
    - POST: Para enviar información
    - PUT: Para modificar información
    - DELETE: Para borrar información
- URI:
  - Ahora para explicar que es la URI tenemos que explicar primero que es la URL y URN.
    - La URL (Uniform Resource Locator) indica la ubicación de un recurso en la web y el protocolo que se va a usar para acceder a el.
      - Ejemplo: <https://www.ehu.eus>
    - La URN (Uniform Resource Name) es un nombre único para un recurso en la web.
      - Ejemplo: <www.ehu.eus/index.html>
    - La URI (Uniform Resource Identifier) es una combinación de URL y URN.
      - Ejemplo: <https://www.ehu.eus/index.html>
      - ![URI](.img/uri.png)
      - La URI puede tener varios campos y su sintaxis es la siguiente:
        - `scheme:[//host[:port]][/]path[?query][#fragment]`
        - `scheme`: El protocolo que se va a usar.
        - `host`: El servidor al que se va a acceder.
        - `port`: El puerto por el que se va a acceder.
        - `path`: La ruta del recurso.
        - `query`: Los parametros de la petición.
        - `fragment`: La parte del recurso que se va a mostrar.

HTTP ha pasado por varias versiones cuyas especificaciones se guardan en los memorandos de la IETF (Internet Engineering Task Force) llamados RFC (Request For Comments).

- HTTP/0.9: La primera versión de HTTP que solo permitía el metodo GET y no tenia cabeceras.
- HTTP/1.0: La segunda versión de HTTP que permitía varios metodos y cabeceras.
- HTTP/1.1: La tercera versión de HTTP que permitía conexiones persistentes y compresión de datos.
- HTTP/2: La cuarta versión de HTTP que permitía multiplexación de conexiones y compresión de cabeceras.
- HTTP/3: La quinta versión de HTTP que permitía conexiones seguras y multiplexación de conexiones.

Ahora voy a explicar el funcionamiento de una petición HTTP con un ejemplo en profundidad.

1. El cliente quiere acceder a un recurso de la web.
2. Introduce la URI en el la aplicación (navegador).
3. La aplicación crea una petición HTTP con el metodo GET y la URI.
    1. La URI se divide en varios campos.
        1. El campo scheme indicara el protocolo que se va a usar.
           1. Por defecto supondremos que es HTTP.
        2. El campo host indicara el servidor al que se va a acceder.
            1. Como el host no es una IP que nuestro ordenador pueda entender, se tiene que traducir a una IP.
            2. Para ello se usa el DNS (Domain Name System) que traduce el host a una IP.
                1. El DNS puede estar en el router, en el ISP, en un servidor DNS o cacheado en el ordenador.
        3. El campo port indicara el puerto por el que se va a acceder.
            1. Si no se especifica el puerto se usara el puerto 80 por defecto.
        4. El campo path indicara la ruta del recurso.
        5. El campo query indicara los parametros de la petición.
        6. El campo fragment indicara la parte del recurso que se va a mostrar.
4. La aplicación establece una conexión TCP/IP con el servidor.
    1. TCP (Transmission Control Protocol) es un protocolo de transporte confiable que garantiza la entrega ordenada y sin errores de los datos.
    2. IP (Internet Protocol) es un protocolo de red que se encarga de enrutar los paquetes de datos a través de la red.
5. Después de establecer la conexión, la aplicación envía la petición HTTP al servidor a través de la conexión TCP/IP.
6. El servidor recibe la petición y la procesa.
    1. Si el servidor no puede procesar la petición, devolverá un error.
    2. Si el servidor puede procesar la petición, devolverá un recurso.
7. El servidor crea una respuesta HTTP con el código de estado y el recurso.
8. La aplicación recibe la respuesta a través de la conexión TCP/IP y la muestra al usuario.
    1. Si el código de estado es 200, se mostrará el recurso.
    2. Si el código de estado es 300, se redirigirá a otra URI.
    3. Si el código de estado es 400, habrá un error en la petición.
    4. Si el código de estado es 500, habrá un error en el servidor.
9. El usuario ve el recurso y puede interactuar con él.

## 1.2. Ejercicios

### 1.2.1. Burp Suite

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

# 2. Web Scraping
