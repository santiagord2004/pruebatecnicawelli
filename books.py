import mysql.connector
from db import connect_to_db

class Book:
    def __init__(self, id, title, category, loanable_physical_copies, store_physical_stock, store_digital_stock, minimum_stock, physical_price, digital_price):
        self.id = id
        self.title = title
        self.category = category
        self.loanable_physical_copies = loanable_physical_copies
        self.store_physical_stock = store_physical_stock
        self.store_digital_stock = store_digital_stock
        self.minimum_stock = minimum_stock
        self.physical_price = physical_price
        self.digital_price = digital_price
    @staticmethod
    def get_by_id(book_id):
        connection = connect_to_db()
        if connection is None:
            return None
        
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM books WHERE id = %s"
        cursor.execute(query, (book_id,))
        book_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if book_data:
            return Book(**book_data)
        return None

    @staticmethod
    def create(title, category, loanable_physical_copies, store_physical_stock, store_digital_stock, minimum_stock, physical_price, digital_price):
        connection = connect_to_db()
        if connection is None:
            return None
        
        cursor = connection.cursor()
        query = """INSERT INTO books (title, category, loanable_physical_copies, store_physical_stock, store_digital_stock, minimum_stock, physical_price, digital_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            cursor.execute(query, (title, category, loanable_physical_copies, store_physical_stock, store_digital_stock, minimum_stock, physical_price, digital_price))
            connection.commit()
            book_id = cursor.lastrowid
            print(f"El libro '{title}' creado con éxito. ID: {book_id}")
            return Book(book_id, title, category, loanable_physical_copies, store_physical_stock, store_digital_stock, minimum_stock, physical_price, digital_price)
        except mysql.connector.Error as err:
            print(f"Error al crear el libro: {err}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()