import mysql.connector
from db import connect_to_db

class User:
    def __init__(self, id, name, user_type, pending_fines):
        self.id = id
        self.name = name
        self.user_type = user_type
        self.pending_fines = pending_fines

    @staticmethod
    def get_by_id(user_id):
        connection = connect_to_db()
        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return User(**user_data)
        return None

    def update_fines(self, new_fines):
        connection = connect_to_db()
        if connection is None:
            return False

        cursor = connection.cursor()
        query = "UPDATE users SET pending_fines = %s WHERE id = %s"
        try:
            cursor.execute(query, (new_fines, self.id))
            connection.commit()
            self.pending_fines = new_fines
            return True
        except mysql.connector.Error as err:
            print(f"Error al actualizar multas: {err}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()

    def create(name, user_type):
        connection = connect_to_db()
        if not connection:
            return None

        cursor = connection.cursor()
        query = "INSERT INTO users (name, user_type) VALUES (%s, %s)"
        try:
            cursor.execute(query, (name, user_type))
            connection.commit()
            user_id = cursor.lastrowid
            print(f"Usuario '{name}' creado con éxito. ID: {user_id}")
            return User(user_id, name, user_type, pending_fines=0.00)
        except mysql.connector.Error as err:
            print(f"Error al crear el usuario: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()