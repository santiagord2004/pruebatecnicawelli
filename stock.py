import mysql.connector
from db import connect_to_db
from datetime import datetime, timedelta

def manageStock():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()

    print("Verificando libros populares...")
    popular_books_query = """
    SELECT book_id, COUNT(*) as loan_count
    FROM loans
    WHERE loan_date >= %s
    GROUP BY book_id
    HAVING loan_count > 10
    """
    one_month_ago = datetime.now() - timedelta(days=30)
    cursor.execute(popular_books_query, (one_month_ago.date(),))
    
    popular_books = cursor.fetchall()
    if popular_books:
        for book_id, _ in popular_books:
            update_query = "UPDATE books SET minimum_stock = minimum_stock + 1 WHERE id = %s"
            cursor.execute(update_query, (book_id,))
            connection.commit()
            print(f"Stock mínimo del libro ID {book_id} aumentado por popularidad.")
    else:
        print("No se encontraron libros populares.")

    print("Verificando libros sin movimiento...")
    unmoved_books_query = """
    SELECT b.id
    FROM books b
    LEFT JOIN loans l ON b.id = l.book_id
    WHERE l.loan_date IS NULL OR l.loan_date < %s
    GROUP BY b.id
    """
    six_months_ago = datetime.now() - timedelta(days=180)
    cursor.execute(unmoved_books_query, (six_months_ago.date(),))

    unmoved_books = cursor.fetchall()
    if unmoved_books:
        for book_id, in unmoved_books:
            update_query = "UPDATE books SET minimum_stock = minimum_stock - 1 WHERE id = %s AND minimum_stock > 1"
            cursor.execute(update_query, (book_id,))
            connection.commit()
            print(f"Stock mínimo del libro ID {book_id} reducido por falta de movimiento.")
    else:
        print("No se encontraron libros sin movimiento.")
    
    cursor.close()
    connection.close()


def autoReorder():
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor(dictionary=True)
    query = "SELECT id, title, store_physical_stock, minimum_stock FROM books WHERE store_physical_stock < minimum_stock"
    cursor.execute(query)
    
    books_to_reorder = cursor.fetchall()
    if books_to_reorder:
        print("\n--- Alerta: Se necesita reabastecimiento de stock ---")
        for book in books_to_reorder:
            print(f"Libro: '{book['title']}' (ID: {book['id']})")
            print(f"  Stock actual: {book['store_physical_stock']}")
            print(f"  Stock mínimo: {book['minimum_stock']}")
            print("  -> Orden de reabastecimiento generada.")
    else:
        print("\nTodos los libros tienen stock suficiente.")
    
    cursor.close()
    connection.close()