# Tema 1

## Teoria

## Ejemplos

### Burpsuite Repeater

#### Obtener el directorio raíz de un servidor web

```http
GET / HTTP/1.1
Host: www.ehu.eus


```

#### Obtener el svg de twitter

```http
GET /o/upv-ehu-campusa-theme/images/custom/campusa/ic-twitter.svg HTTP/1.1
Host: www.ehu.eus


```

### Python

#### Obtener el aspx de Chunked

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

#### Redireccion automatica

```python
import requests
