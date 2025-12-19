import requests
from flask_jwt_extended import create_access_token

acces_token = None

def registrar_usuario(user,passw):
    response = requests.post('http://localhost:5000/register', json={"usuario": user, "contrasena": passw})
    return response.json()

def hacer_login(user,passw):
    response = requests.post('http://localhost:5000/login', json={"usuario": user, "contrasena": passw})
    if response.status_code == 200:
        global acces_token
        acces_token = response.json()["token"]
    return response.json()

def consultar_users():
    response = requests.get('http://localhost:5000/users', headers={"Authorization": f"Bearer {acces_token}"})
    return response.json()

def get_mensajes():
    response = requests.get('http://localhost:5000/messages', headers={"Authorization": f"Bearer {acces_token}"})
    return response.json()

def post_mensaje(mensaje):
    response = requests.post('http://localhost:5000/send', json={"message": mensaje})
    return response.json()

def modificar_mensaje(payload):
    response = requests.put('http://localhost:5000/modify', json=payload)
    return response.json()

def eliminar_mensaje(id):
    response = requests.delete('http://localhost:5000/delete', json={"id": id})
    return response.json()  

if __name__ == '__main__':
    # print(registrar_usuario("user1", "1234hola"))
    print(hacer_login("user1", "1234hola"))
    print(consultar_users())
    # print("Llamando a la función de post_mensaje")
    # print(post_mensaje("Hola 1"))
    # print(post_mensaje("Hola 2"))
    # print(post_mensaje("Hola 3"))
    # print(post_mensaje("Hola 4"))
    # print("Llamando a la función de get_mensajes")
    # print(get_mensajes())
    
    # print("Llamando a la función de modificar_mensaje")
    # modificar_mensaje({"id": "0743f268e94847639ce82a02dfcab974", "message": "Hola 2"})
    # print("Llamando a la función de eliminar_mensaje")
    # eliminar_mensaje("1")
    
    
