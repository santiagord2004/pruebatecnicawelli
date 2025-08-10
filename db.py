import mysql.connector

db_config = {
    'user': 'welli',
    'password': 'Welli123.',
    'host': '127.0.0.1', 
    'database': 'LIBRARY'
}

def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None
