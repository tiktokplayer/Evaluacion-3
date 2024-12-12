from servicios.negocio import (
    encriptar_password,
    desencriptar_password,
    cargar_datos_api,
    guardar_datos_api,
    buscar_google,
    crear_post
)

def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN ===")
    print("1. Encriptación de contraseña")
    print("2. Solicitar datos desde la API")
    print("3. Búsqueda en Google (API Serper)")
    print("4. Crear un nuevo post") 
    print("5. Salir")
    print("================================")

def mostrar_datos_obtenidos(datos, tipo):
    """Muestra los datos obtenidos según su tipo"""
    if not datos:
        return
    
    print(f"\nMostrando los primeros 5 {tipo} obtenidos:")
    for i, dato in enumerate(datos[:5], 1):
        print(f"\n--- {tipo.upper()} #{i} ---")
        if tipo == "posts":
            print(f"ID: {dato['id']}")
            print(f"Título: {dato['title']}")
            print(f"Contenido: {dato['body'][:100]}...")
            print(f"Usuario ID: {dato['userId']}")
        elif tipo == "comentarios":
            print(f"ID: {dato['id']}")
            print(f"Post ID: {dato['postId']}")
            print(f"Nombre: {dato['name']}")
            print(f"Email: {dato['email']}")
            print(f"Comentario: {dato['body'][:100]}...")
        elif tipo == "usuarios":
            print(f"ID: {dato['id']}")
            print(f"Nombre: {dato['name']}")
            print(f"Usuario: {dato['username']}")
            print(f"Email: {dato['email']}")
            print(f"Ciudad: {dato['address']['city']}")

def menu_api():
    while True:
        print("\n=== SOLICITUD DE DATOS DESDE API ===")
        print("1. Obtener Posts")
        print("2. Obtener Comentarios")
        print("3. Obtener Usuarios")
        print("4. Volver al menú principal")
        
        opcion = input("\nSeleccione el tipo de datos a obtener (1-4): ")
        
        if opcion in ["1", "2", "3"]:
            tipo_datos = {
                "1": "posts",
                "2": "comentarios",
                "3": "usuarios"
            }[opcion]
            
            print(f"\nObteniendo {tipo_datos} desde JSONPlaceholder...")
            datos = cargar_datos_api(opcion)
            
            if datos:
                print(f"\n¡Datos obtenidos exitosamente!")
                print(f"Se obtuvieron {len(datos)} {tipo_datos}")
                print(f"Guardando datos en la base de datos local...")
                
                guardados = guardar_datos_api(datos, tipo_datos)
                
                if guardados:
                    print(f"\n¡Datos guardados exitosamente en la base de datos!")
                    print(f"Consultando datos guardados...")
                    mostrar_datos_obtenidos(datos, tipo_datos)
                else:
                    print("Error al guardar los datos en la base de datos.")
            else:
                print("Error al obtener los datos de la API.")
                
        elif opcion == "4":
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 4.")
        
        input("\nPresione Enter para continuar...")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == "1":
            print("\n=== ENCRIPTACIÓN DE CONTRASEÑA ===")
            password = input("Ingrese la contraseña a encriptar: ")
            print(f"\nString ingresado: {password}")
            
            password_encriptada = encriptar_password(password)
            print(f"\nContraseña encriptada: {password_encriptada}")
            
            password_desencriptada = desencriptar_password(password_encriptada)
            print(f"\nContraseña desencriptada: {password_desencriptada}")
            
            if password == password_desencriptada:
                print("\nVERIFICACIÓN EXITOSA:")
                print(f"String original: {password}")
                print(f"String desencriptado: {password_desencriptada}")
                print("Los strings coinciden correctamente.")
            else:
                print("\nERROR EN LA VERIFICACIÓN:")
                print(f"String original: {password}")
                print(f"String desencriptado: {password_desencriptada}")
                print("Los strings no coinciden.")
        elif opcion == "2":
            menu_api()
        elif opcion == "3":
            print("\n=== BÚSQUEDA EN GOOGLE ===")
            print("1. Búsqueda general")
            print("2. Búsqueda de imágenes")
            tipo_busqueda = input("\nSeleccione el tipo de búsqueda (1-2): ")
            
            query = input("Ingrese su búsqueda: ")
            
            if tipo_busqueda == "1":
                resultados = buscar_google(query, "search")
                if resultados:
                    print("\nResultados de la búsqueda:")
                    for i, resultado in enumerate(resultados[:5], 1):
                        print(f"\n{i}. {resultado['title']}")
                        print(f"URL: {resultado['link']}")
                        print(f"Descripción: {resultado['snippet']}")
            
            elif tipo_busqueda == "2":
                resultados = buscar_google(query, "images")
                if resultados:
                    print("\nResultados de la búsqueda de imágenes:")
                    for i, imagen in enumerate(resultados[:5], 1):
                        print(f"\n{i}. {imagen['title']}")
                        print(f"URL de la imagen: {imagen['imageUrl']}")
        elif opcion == "4":
            crear_post()  # Llamamos a la función para crear un post
        elif opcion == "5":
            print("\n¡Gracias por usar el sistema! Hasta pronto.")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 5.")

        if opcion != "2":  # Los submenús ya tienen su propio "presione Enter"
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
