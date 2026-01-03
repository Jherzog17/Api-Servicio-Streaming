#!/usr/bin/env python3
"""
Script interactivo para probar los endpoints de la API de Streaming.
Ejecuta: python test_api.py
Asegúrate de que el servidor Flask esté corriendo en http://127.0.0.1:5000
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Variables globales para mantener estado entre pruebas
token = None
last_user_id = None


def print_response(response):
    """Imprime la respuesta de manera formateada."""
    print(f"\n{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*50}\n")


def get_input(prompt, default=None):
    """Obtiene input del usuario con valor por defecto opcional."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def get_auth_headers():
    """Devuelve los headers de autorización si hay token."""
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# ================= USUARIOS =================

def test_register_user():
    """POST /usuarios/register - Registrar usuario"""
    print("\n--- Registrar Usuario ---")
    nickname = get_input("Nickname", "test_user")
    password = get_input("Password", "test123")
    
    response = requests.post(
        f"{BASE_URL}/usuarios/register",
        json={"nickname": nickname, "password": password}
    )
    print_response(response)


def test_login_user():
    """POST /usuarios/login - Iniciar sesión"""
    global token
    print("\n--- Login Usuario ---")
    nickname = get_input("Nickname", "test_user")
    password = get_input("Password", "test123")
    
    response = requests.post(
        f"{BASE_URL}/usuarios/login",
        json={"nickname": nickname, "password": password}
    )
    print_response(response)
    
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"✅ Token guardado para futuras peticiones")


def test_get_users():
    """GET /usuarios/ - Obtener todos los usuarios"""
    global last_user_id
    print("\n--- Obtener Usuarios ---")
    
    response = requests.get(f"{BASE_URL}/usuarios/")
    print_response(response)
    
    if response.status_code == 200 and response.json():
        last_user_id = list(response.json().keys())[0]
        print(f"📌 ID del primer usuario guardado: {last_user_id}")


def test_edit_user():
    """PUT /usuarios/<id_usuario> - Editar usuario [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Editar Usuario [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    print("Deja vacío si no quieres cambiar el campo:")
    nickname = get_input("Nuevo nickname (vacío para no cambiar)", "")
    password = get_input("Nueva password (vacío para no cambiar)", "")
    
    data = {}
    if nickname:
        data["nickname"] = nickname
    if password:
        data["password"] = password
    
    if not data:
        print("❌ Debes proporcionar al menos un campo para cambiar")
        return
    
    response = requests.put(
        f"{BASE_URL}/usuarios/{user_id}",
        json=data,
        headers=get_auth_headers()
    )
    print_response(response)


def test_delete_user():
    """DELETE /usuarios/<id_usuario> - Eliminar usuario [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Eliminar Usuario [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario a eliminar", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    confirm = get_input(f"¿Seguro que quieres eliminar el usuario {user_id}? (s/n)", "n")
    if confirm.lower() != 's':
        print("Operación cancelada")
        return
    
    response = requests.delete(
        f"{BASE_URL}/usuarios/{user_id}",
        headers=get_auth_headers()
    )
    print_response(response)


# ================= MEDIOS DE STREAMING =================

def test_reproducir_medio():
    """GET /medio_de_streaming/<id> - Reproducir medio [🔐 Requiere Token]"""
    global token
    print("\n--- Reproducir Medio de Streaming [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    medio_id = get_input("ID del medio", "1")
    
    response = requests.get(
        f"{BASE_URL}/medio_de_streaming/{medio_id}",
        headers=get_auth_headers()
    )
    print_response(response)


def test_list_all_medios():
    """GET /medio_de_streaming/ - Listar todos los medios"""
    print("\n--- Listar Todos los Medios ---")
    response = requests.get(f"{BASE_URL}/medio_de_streaming/")
    print_response(response)


def test_list_medios_con_filtros():
    """GET /medio_de_streaming/?<params> - Listar medios con filtros"""
    print("\n--- Listar Medios con Filtros ---")
    print("Deja vacío el campo si no quieres filtrar por él.")
    pais = get_input("País", "")
    fecha = get_input("Fecha de subida (YYYY-MM-DD)", "")
    num_items = get_input("Número máximo de items", "")
    
    params = {}
    if pais:
        params["pais"] = pais
    if fecha:
        params["fecha_subida"] = fecha
    if num_items:
        params["num_items"] = num_items
        
    if not params:
        print("⚠️  No has seleccionado ningún filtro, se listarán todos.")
    
    response = requests.get(f"{BASE_URL}/medio_de_streaming/", params=params)
    print_response(response)





def test_add_medio():
    """POST /medio_de_streaming/anadir_medio - Añadir medio de streaming"""
    print("\n--- Añadir Medio de Streaming ---")
    
    id_medio_streaming = get_input("ID numérico del medio", "1")
    pais = get_input("País", "España")
    fecha = get_input("Fecha de subida (YYYY-MM-DD)", "2024-01-15")
    
    response = requests.post(
        f"{BASE_URL}/medio_de_streaming/anadir_medio",
        json={
            "id_medio_de_streaming": int(id_medio_streaming),
            "pais": pais,
            "fecha_de_subida": fecha
        }
    )
    print_response(response)


def test_delete_medio():
    """DELETE /medio_de_streaming/<id> - Eliminar medio de streaming"""
    print("\n--- Eliminar Medio de Streaming ---")
    medio_id = get_input("ID del medio a eliminar", "1")
    
    confirm = get_input(f"¿Seguro que quieres eliminar el medio {medio_id}? (s/n)", "n")
    if confirm.lower() != 's':
        print("Operación cancelada")
        return
    
    response = requests.delete(f"{BASE_URL}/medio_de_streaming/{medio_id}")
    print_response(response)


def test_edit_medio():
    """PUT /medio_de_streaming/<id> - Editar medio de streaming"""
    print("\n--- Editar Medio de Streaming ---")
    medio_id = get_input("ID del medio a editar", "1")
    
    id_medio_streaming = get_input("Nuevo ID numérico del medio", "1")
    pais = get_input("Nuevo país", "México")
    fecha = get_input("Nueva fecha de subida (YYYY-MM-DD)", "2024-02-20")
    
    response = requests.put(
        f"{BASE_URL}/medio_de_streaming/{medio_id}",
        json={
            "id_medio_de_streaming": int(id_medio_streaming),
            "pais": pais,
            "fecha_de_subida": fecha
        }
    )
    print_response(response)


# ================= HISTORIAL =================

def test_get_historial():
    """GET /usuarios/<id>/historial - Obtener historial [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Obtener Historial [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    response = requests.get(
        f"{BASE_URL}/usuarios/{user_id}/historial",
        headers=get_auth_headers()
    )
    print_response(response)


def test_add_historial():
    """POST /usuarios/<id>/historial - Añadir al historial [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Añadir al Historial [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    medio_id = get_input("ID del medio de streaming", "1")
    fecha = get_input("Fecha de visualización (YYYY-MM-DD, vacío para omitir)", "")
    
    data = {"id_medio_de_streaming": int(medio_id)}
    if fecha:
        data["fecha_visualizacion"] = fecha
    
    response = requests.post(
        f"{BASE_URL}/usuarios/{user_id}/historial",
        json=data,
        headers=get_auth_headers()
    )
    print_response(response)


# ================= SUSCRIPCIONES =================

def test_get_suscripcion():
    """GET /usuarios/<id>/suscripciones - Consultar suscripción [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Consultar Suscripción Activa [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    response = requests.get(
        f"{BASE_URL}/usuarios/{user_id}/suscripciones",
        headers=get_auth_headers()
    )
    print_response(response)


def test_pagar_suscripcion():
    """POST /usuarios/<id>/suscripciones - Pagar suscripción [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Pagar Suscripción [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    id_suscripcion = get_input("ID de suscripción", "1")
    tipo = get_input("Tipo de suscripción", "Premium")
    precio = get_input("Precio", "9.99")
    
    response = requests.post(
        f"{BASE_URL}/usuarios/{user_id}/suscripciones",
        json={
            "id_suscripcion": int(id_suscripcion),
            "tipo": tipo,
            "precio": precio
        },
        headers=get_auth_headers()
    )
    print_response(response)


def test_modificar_suscripcion():
    """PUT /usuarios/<id>/suscripciones - Modificar suscripción [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Modificar Suscripción [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    id_suscripcion = get_input("Nuevo ID de suscripción", "2")
    tipo = get_input("Nuevo tipo de suscripción", "Premium Plus")
    precio = get_input("Nuevo precio", "14.99")
    
    response = requests.put(
        f"{BASE_URL}/usuarios/{user_id}/suscripciones",
        json={
            "id_suscripcion": int(id_suscripcion),
            "tipo": tipo,
            "precio": precio
        },
        headers=get_auth_headers()
    )
    print_response(response)


def test_cancelar_suscripcion():
    """DELETE /usuarios/<id>/suscripciones - Cancelar suscripción [🔐 Requiere Token]"""
    global last_user_id, token
    print("\n--- Cancelar Suscripción [🔐 JWT] ---")
    
    if not token:
        print("⚠️  No hay token. Haz login primero.")
        return
    
    user_id = get_input("ID del usuario", last_user_id or "")
    if not user_id:
        print("❌ Debes proporcionar un ID de usuario")
        return
    
    confirm = get_input(f"¿Seguro que quieres cancelar la suscripción? (s/n)", "n")
    if confirm.lower() != 's':
        print("Operación cancelada")
        return
    
    response = requests.delete(
        f"{BASE_URL}/usuarios/{user_id}/suscripciones",
        headers=get_auth_headers()
    )
    print_response(response)


# ================= MENÚ PRINCIPAL =================

def show_main_menu():
    """Muestra el menú principal."""
    print("\n" + "="*60)
    print("       🎬 API DE STREAMING - SCRIPT DE PRUEBAS 🎬")
    print("="*60)
    print("\n¿Qué sección quieres probar?\n")
    print("  1. 👤 Usuarios")
    print("  2. 🎥 Medios de Streaming")
    print("  3. 📜 Historial")
    print("  4. 💳 Suscripciones")
    print("  0. ❌ Salir")
    print()


def show_users_menu():
    """Menú de endpoints de usuarios."""
    print("\n--- 👤 ENDPOINTS DE USUARIOS ---\n")
    print("  1. Registrar usuario (POST /usuarios/register)")
    print("  2. Login (POST /usuarios/login)")
    print("  3. Obtener usuarios (GET /usuarios/)")
    print("  4. Editar usuario (PUT /usuarios/<id>)")
    print("  5. Eliminar usuario (DELETE /usuarios/<id>)")
    print("  0. ⬅️  Volver al menú principal")
    print()


def show_media_menu():
    """Menú de endpoints de medios."""
    print("\n--- 🎥 ENDPOINTS DE MEDIOS ---\n")
    print("  1. Reproducir medio (GET /medio_de_streaming/<id>)")
    print("  2. Listar TODOS los medios (GET /medio_de_streaming/)")
    print("  3. Listar medios con filtros (País, Fecha, Límite)")
    print("  4. Añadir medio (POST /medio_de_streaming/anadir_medio)")
    print("  5. Eliminar medio (DELETE /medio_de_streaming/<id>)")
    print("  6. Editar medio (PUT /medio_de_streaming/<id>)")
    print("  0. ⬅️  Volver al menú principal")
    print()


def show_historial_menu():
    """Menú de endpoints de historial."""
    print("\n--- 📜 ENDPOINTS DE HISTORIAL ---\n")
    print("  1. Obtener historial (GET /usuarios/<id>/historial)")
    print("  2. Añadir al historial (POST /usuarios/<id>/historial)")
    print("  0. ⬅️  Volver al menú principal")
    print()


def show_suscripciones_menu():
    """Menú de endpoints de suscripciones."""
    print("\n--- 💳 ENDPOINTS DE SUSCRIPCIONES ---\n")
    print("  1. Consultar suscripción activa (GET /usuarios/<id>/suscripciones)")
    print("  2. Pagar/Activar suscripción (POST /usuarios/<id>/suscripciones)")
    print("  3. Modificar suscripción (PUT /usuarios/<id>/suscripciones)")
    print("  4. Cancelar suscripción (DELETE /usuarios/<id>/suscripciones)")
    print("  0. ⬅️  Volver al menú principal")
    print()


def handle_users_menu():
    """Maneja la selección del menú de usuarios."""
    while True:
        show_users_menu()
        choice = get_input("Selecciona una opción", "0")
        
        if choice == "1":
            test_register_user()
        elif choice == "2":
            test_login_user()
        elif choice == "3":
            test_get_users()
        elif choice == "4":
            test_edit_user()
        elif choice == "5":
            test_delete_user()
        elif choice == "0":
            break
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")


def handle_media_menu():
    """Maneja la selección del menú de medios."""
    while True:
        show_media_menu()
        choice = get_input("Selecciona una opción", "0")
        
        if choice == "1":
            test_reproducir_medio()
        elif choice == "2":
            test_list_all_medios()
        elif choice == "3":
            test_list_medios_con_filtros()
        elif choice == "4":
            test_add_medio()
        elif choice == "5":
            test_delete_medio()
        elif choice == "6":
            test_edit_medio()
        elif choice == "0":
            break
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")


def handle_historial_menu():
    """Maneja la selección del menú de historial."""
    while True:
        show_historial_menu()
        choice = get_input("Selecciona una opción", "0")
        
        if choice == "1":
            test_get_historial()
        elif choice == "2":
            test_add_historial()
        elif choice == "0":
            break
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")


def handle_suscripciones_menu():
    """Maneja la selección del menú de suscripciones."""
    while True:
        show_suscripciones_menu()
        choice = get_input("Selecciona una opción", "0")
        
        if choice == "1":
            test_get_suscripcion()
        elif choice == "2":
            test_pagar_suscripcion()
        elif choice == "3":
            test_modificar_suscripcion()
        elif choice == "4":
            test_cancelar_suscripcion()
        elif choice == "0":
            break
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")


def main():
    """Función principal del script."""
    print("\n🚀 Asegúrate de que el servidor Flask esté corriendo en http://127.0.0.1:5000")
    print("   Ejecuta: python backend.py")
    
    while True:
        show_main_menu()
        choice = get_input("Selecciona una opción", "0")
        
        if choice == "1":
            handle_users_menu()
        elif choice == "2":
            handle_media_menu()
        elif choice == "3":
            handle_historial_menu()
        elif choice == "4":
            handle_suscripciones_menu()
        elif choice == "0":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    print("Este script fue generado con IA, siguiendo el siguiente prompt:\n")
    print("""
    quiero que hagas un script de python que al ejecutarlo vaya ejecutando 
    codigo para probar cada endopoint de la api. Para saber que funcion quieres 
    activar usar un input o similar que te permita seleccionar que seccion probar
    de la api. En resumen, lo que quiero es un script en el que pueda probar toda
    la api endpoint por endpoint y no todo de golpe.\n
    """)
    main()
