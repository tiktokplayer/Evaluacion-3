import mysql.connector
from mysql.connector import Error
import os

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

    def create_tables(self):
        conn = self.create_connection()
        if conn is not None:
            try:
                with open(self.schema_file, 'r') as sql_file:
                    sql_script = sql_file.read()
                conn.executescript(sql_script)
                conn.commit()
            except Error as e:
                print(f"Error al crear las tablas: {e}")
            finally:
                conn.close()

    def insert_post(self, post):
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT MAX(id) FROM posts')
                max_id = cursor.fetchone()[0]
                
                next_id = 101 if max_id is None else max_id + 1
                
                cursor.execute('''
                    INSERT INTO posts (id, title, body, userId)
                    VALUES (?, ?, ?, ?)
                ''', (next_id, post.title, post.body, post.userId))
                conn.commit()
                return next_id
            except Error as e:
                print(f"Error al insertar el post: {e}")
                return None
            finally:
                conn.close()

    def get_post(self, post_id):
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                print(f"Error al obtener el post: {e}")
                return None
            finally:
                conn.close()

    def update_post(self, post):
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE posts 
                    SET title = ?, body = ?, userId = ?
                    WHERE id = ?
                ''', (post.title, post.body, post.userId, post.id))
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error al actualizar el post: {e}")
                return False
            finally:
                conn.close()

    def delete_post(self, post_id):
        conn = self.create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                print(f"Error al eliminar el post: {e}")
                return False
            finally:
                conn.close() 