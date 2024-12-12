import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clases.post import Post
from auxiliares.url import Variables_fijas
from datos.database import DatabaseManager
from .encriptacion import EncriptacionService
from .api_service import APIService

db = DatabaseManager()

encriptacion_service = EncriptacionService()
api_service = APIService()

def obtener_todos_posts():
    try:
        response = requests.get(Variables_fijas.URL_Post)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener los posts: {e}")
        return []

def leer_post_por_id(post_id):
    try:
        if post_id <= 100:
            print("Buscando post en la API...")
            response = requests.get(f"{Variables_fijas.URL_Post}/{post_id}")
            response.raise_for_status()
            data = response.json()

            return Post(
                id=data['id'],
                title=data['title'],
                body=data['body'],
                userId=data['userId']
            )
        else:
            print("Buscando post en la base de datos local...")
            post_data = db.get_post(post_id)
            if post_data:
                return Post(
                    id=post_data[0],
                    title=post_data[1],
                    body=post_data[2],
                    userId=post_data[3]
                )
            print(f"No se encontró un post local con ID {post_id}")
            return None

    except requests.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
            print(f"Error: No existe un post con el ID {post_id}")
        else:
            print(f"Error al obtener el post: {e}")
        return None
def crear_post():
    title = input("Ingresa el título del post: ")
    body = input("Ingresa el contenido del post: ")
    user_id = input("Ingresa el ID del usuario: ")

    post = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    db_manager = DatabaseManager()
    post_id = db_manager.insert_post(post)
    if post_id:
        print(f"Post creado con ID: {post_id}")
    else:
        print("Error al crear el post en la base de datos.")
    db_manager.close_connection()    

def actualizar_post(post_id):
    if post_id <= 100:
        print("Error: No se pueden modificar los posts de JSONPlaceholder (IDs 1-100)")
        return None
    
    post_local = db.get_post(post_id)
    if not post_local:
        print(f"Error: No se encontró un post local con ID {post_id}")
        return None

    try:
        titulo = input("Ingrese el nuevo título del post: ")
        contenido = input("Ingrese el nuevo contenido del post: ")
        user_id = int(input("Ingrese el nuevo ID del usuario (1-10): "))
        
        if not 1 <= user_id <= 10:
            print("Error: El ID de usuario debe estar entre 1 y 10")
            return None

        post = Post(
            id=post_id,
            title=titulo,
            body=contenido,
            userId=user_id
        )
        
        if db.update_post(post):
            print(f"Post {post_id} actualizado exitosamente")
            return post
        return None
        
    except ValueError:
        print("Error: El ID de usuario debe ser un número")
        return None

def eliminar_post(post_id):
    if post_id <= 100:
        print("Error: No se pueden eliminar los posts de JSONPlaceholder (IDs 1-100)")
        return False
    
    post_local = db.get_post(post_id)
    if not post_local:
        print(f"Error: No se encontró un post local con ID {post_id}")
        return False

    try:
        if db.delete_post(post_id):
            print(f"Post {post_id} eliminado exitosamente")
            return True
        return False
        
    except Exception as e:
        print(f"Error al eliminar el post: {e}")
        return False

def encriptar_password(password):
    return encriptacion_service.encriptar(password)

def desencriptar_password(password_encriptada):
    return encriptacion_service.desencriptar(password_encriptada)

def cargar_datos_api(tipo_dato):
    return api_service.cargar_datos_api(tipo_dato)

def guardar_datos_api(datos, tipo):
    return api_service.guardar_datos_api(datos, tipo)

def buscar_google(query, tipo="search"):
    return api_service.buscar_google(query, tipo)

