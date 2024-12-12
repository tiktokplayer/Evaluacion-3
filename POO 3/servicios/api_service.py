import os
import json
import requests
from dotenv import load_dotenv
from auxiliares.url import Variables_fijas
from clases.post import Post
from datos.database import DatabaseManager

load_dotenv()

class APIService:
    def __init__(self):
        self.db = DatabaseManager()
        self.base_url = Variables_fijas.BASE_URL
        self.serper_api_key = os.getenv('SERPER_API_KEY')

    def cargar_datos_api(self, tipo_dato):
        endpoints = {
            "1": "/posts",
            "2": "/comments",
            "3": "/users"
        }
        
        if tipo_dato not in endpoints:
            print("Tipo de dato no válido")
            return None

        try:
            url = f"{self.base_url}{endpoints[tipo_dato]}"
            response = requests.get(url)
            response.raise_for_status()
            datos = response.json()

            return datos

        except requests.RequestException as e:
            print(f"Error al obtener datos de la API: {e}")
            return None

    def buscar_google(self, query, tipo_busqueda="search"):
        url = f"https://google.serper.dev/{tipo_busqueda}"
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            datos = response.json()
            
            if tipo_busqueda == "images":
                return datos.get('images', [])
            return datos.get('organic', [])
            
        except requests.RequestException as e:
            print(f"Error en la búsqueda: {e}")
            return None
        
    def guardar_datos_api(self, datos, tipo_datos):
        if tipo_datos == "posts":
            for dato in datos:
                try:
                    print(f"Inserting post: {dato['id']}, {dato['title']}, {dato['body']}, {dato['userId']}")
                    self.db.insert_post(Post(
                        id=dato['id'],
                        title=dato['title'],
                        body=dato['body'],
                        userId=dato['userId']
                    ))
                except Exception as e:
                    print(f"Error al insertar el post: {e}")

api_service = APIService()
cargar_datos_api = api_service.cargar_datos_api
guardar_datos_api = api_service.guardar_datos_api
buscar_google = api_service.buscar_google