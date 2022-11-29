import json,requests

def main():
    body = {
    "usuario": "robert",
    }
    url ='http://127.0.0.1:5000/api/venta'
    metodo = "GET"
    encabezado = {'Content-Type': 'application/json'}
    response = requests.get(
                url, data=json.dumps(body),
                headers=encabezado
                )
    print(response)
    data = response.json()
    print(data)
if __name__ == '__main__':
    main()