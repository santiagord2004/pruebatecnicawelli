import mysql.connector
from db import connect_to_db
from datetime import datetime, timedelta

def usersWithMostFines():

    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT name, user_type, pending_fines
    FROM users
    WHERE pending_fines > 0
    ORDER BY pending_fines DESC
    """
    cursor.execute(query)
    
    users_fines = cursor.fetchall()
    
    print("\n--- Reporte de Usuarios con Más Multas Pendientes ---")
    if users_fines:
        for user in users_fines:
            print(f"Nombre: {user['name']}, Tipo: {user['user_type']}, Multa: ${user['pending_fines']:.2f}")
    else:
        print("No hay multas pendientes.")
    
    cursor.close()
    connection.close()

def mostPopularBooks(period_in_months=3):

    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    start_date = datetime.now() - timedelta(days=30 * period_in_months)
    
    query = """
    SELECT b.title, b.category, COUNT(l.book_id) AS loan_count
    FROM loans l
    JOIN books b ON l.book_id = b.id
    WHERE l.loan_date >= %s
    GROUP BY l.book_id
    ORDER BY loan_count DESC
    """
    cursor.execute(query, (start_date.date(),))
    
    popular_books = cursor.fetchall()
    
    print(f"\n--- Reporte de Libros Más Populares (Últimos {period_in_months} meses) ---")
    if popular_books:
        for book in popular_books:
            print(f"Título: {book['title']}, Categoría: {book['category']}, Préstamos: {book['loan_count']}")
    else:
        print("No se encontraron préstamos en este período.")

    cursor.close()
    connection.close()

def salesByCategory():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT b.category, SUM(pd.quantity) AS total_sold, SUM(pd.unit_price * pd.quantity) AS total_revenue
    FROM purchase_details pd
    JOIN books b ON pd.book_id = b.id
    GROUP BY b.category
    ORDER BY total_revenue DESC
    """
    cursor.execute(query)
    
    sales_data = cursor.fetchall()
    
    print("\n--- Reporte de Ventas por Categoría ---")
    if sales_data:
        for sale in sales_data:
            print(f"Categoría: {sale['category']}, Total Vendido: {sale['total_sold']}, Ingresos Totales: ${sale['total_revenue']:.2f}")
    else:
        print("No se encontraron ventas.")
    
    cursor.close()
    connection.close()

def mostPurchasingUsers():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT u.user_type, COUNT(p.id) AS total_purchases
    FROM purchases p
    JOIN users u ON p.user_id = u.id
    GROUP BY u.user_type
    ORDER BY total_purchases DESC
    """
    try:
        cursor.execute(query)
        purchasing_users = cursor.fetchall()
        
        print("\n--- Reporte: Tipo de Usuario que Más Compra Libros ---")
        if purchasing_users:
            for user in purchasing_users:
                print(f"Tipo de Usuario: {user['user_type']}, Total de Compras: {user['total_purchases']}")
        else:
            print("No se encontraron compras.")
    except mysql.connector.Error as err:
        print(f"Error al generar el reporte: {err}")
    finally:
        cursor.close()
        connection.close()

def mostReservingUsers():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT u.user_type, COUNT(r.id) AS total_reservations
    FROM reservations r
    JOIN users u ON r.user_id = u.id
    GROUP BY u.user_type
    ORDER BY total_reservations DESC
    """
    try:
        cursor.execute(query)
        reserving_users = cursor.fetchall()
        
        print("\n--- Reporte: Tipo de Usuario que Más Reserva Libros ---")
        if reserving_users:
            for user in reserving_users:
                print(f"Tipo de Usuario: {user['user_type']}, Total de Reservas: {user['total_reservations']}")
        else:
            print("No se encontraron reservas.")
    except mysql.connector.Error as err:
        print(f"Error al generar el reporte: {err}")
    finally:
        cursor.close()
        connection.close()

