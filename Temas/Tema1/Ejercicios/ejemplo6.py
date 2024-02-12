import requests
import sys
import zlib

def print_response(response):
    i=0
    print("Status: " + str(response.status_code))
    print("Reason: " + response.reason)
    for cabecera in response.headers:
        i+=1
        print(str(i)+ " " + cabecera + ": " + response.headers[cabecera])
        
metodo="GET"
uri="https://www.google.es/"
cabeceras={'Host': 'www.google.es'}
compressed = False
if len(sys.argv) == 1:
    cabeceras['Accept-Encoding'] = 'identity'
elif sys.argv[1] == "compress":
    cabeceras['Accept-Encoding'] = 'gzip'
    compressed = True

respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False, stream=True)

print_response(respuesta)
print(str(len(respuesta.raw.data)) + " bytes received")
if compressed:
    print(str(len(zlib.decompress(respuesta.raw.data, 16+zlib.MAX_WBITS))) + " bytes decompressed")