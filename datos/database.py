import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbev3'
            )
            if connection.is_connected():
                print("Conexión exitosa a la base de datos")
                return connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def create_tables(self):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                with open('schema.sql', 'r') as sql_file:
                    sql_script = sql_file.read()
                cursor.execute(sql_script)
                self.connection.commit()
                print("Tablas creadas exitosamente")
            except Error as e:
                print(f"Error al crear las tablas: {e}")
            finally:
                cursor.close()

    def insert_post(self, post):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute('SELECT MAX(id) FROM posts')
                max_id = cursor.fetchone()[0]
                
                next_id = 101 if max_id is None else max_id + 1

                cursor.execute('''
                    INSERT INTO posts (id, title, body, userId)
                    VALUES (%s, %s, %s, %s)
                ''', (next_id, post['title'], post['body'], post['userId']))
                self.connection.commit()
                return next_id
            except Error as e:
                print(f"Error al insertar el post: {e}")
                return None
            finally:
                cursor.close()

    def get_post(self, post_id):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                print(f"Error al obtener el post: {e}")
                return None
            finally:
                cursor.close()

    def update_post(self, post):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute('''
                    UPDATE posts 
                    SET title = %s, body = %s, userId = %s
                    WHERE id = %s
                ''', (post['title'], post['body'], post['userId'], post['id']))
                self.connection.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error al actualizar el post: {e}")
                return False
            finally:
                cursor.close()

    def delete_post(self, post_id):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))
                self.connection.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error al eliminar el post: {e}")
                return False
            finally:
                cursor.close()
