import requests

def print_response(response):
    i=0
    print("Status: " + str(response.status_code))
    print("Reason: " + response.reason)
    for cabecera in response.headers:
        i+=1
        print(str(i)+ " " + cabecera + ": " + response.headers[cabecera])

metodo="GET"
uri="https://www.ehu.eus/o/ehu-theme/images/custom/web-ods-16-en.png"
cabeceras={'Host': 'www.ehu.eus'}
cuerpo=""
response = requests.request(metodo, uri, headers=cabeceras, data=cuerpo)

print_response(response)

metodo="GET"
uri="https://www.ehu.eus/o/ehu-theme/images/custom/web-ods-16-en.png"
cabeceras={'Host': 'www.ehu.eus', 
           'If-Modified-Since': response.headers['Last-Modified']
           }
cuerpo=""
response1 = requests.request(metodo, uri, headers=cabeceras, data=cuerpo)

print_response(response1)
