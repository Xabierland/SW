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

fichero = open("ejemplo1.jpg", "wb")
fichero.write(response.content)
fichero.close()