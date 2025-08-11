from users import User
from books import Book
from db import connect_to_db
import datetime

def verifyFines(user):
    return user.pending_fines <= 20000

def hasBorrowed(user_id, book_id):

    connection = connect_to_db()
    if connection is None:
        return True
    
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM loans WHERE user_id = %s AND book_id = %s AND status = 'Loaned'"
    cursor.execute(query, (user_id, book_id))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0

def reserve_stock(book_id, quantity):

    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    reservation_time = datetime.now()
    
    query = "INSERT INTO stock_reservations (book_id, quantity, reservation_time) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (book_id, quantity, reservation_time))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error al reservar stock: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def release_expired_reservations():
    connection = connect_to_db()
    if connection is None:
        return
    
    cursor = connection.cursor()
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    query = "SELECT book_id, quantity FROM stock_reservations WHERE reservation_time <= %s"
    cursor.execute(query, (ten_minutes_ago,))
    
    expired_reservations = cursor.fetchall()
    
    if expired_reservations:
        for book_id, quantity in expired_reservations:
            delete_query = "DELETE FROM stock_reservations WHERE book_id = %s AND quantity = %s AND reservation_time <= %s"
            cursor.execute(delete_query, (book_id, quantity, ten_minutes_ago))
        
            update_stock_query = "UPDATE books SET store_physical_stock = store_physical_stock + %s WHERE id = %s"
            cursor.execute(update_stock_query, (quantity, book_id))
        
        connection.commit()
        print(f"Se han liberado {len(expired_reservations)} reservas de stock.")

    cursor.close()
    connection.close()

def purchase(user_id, book_id, quantity, book_type):
    user = User.get_by_id(user_id)
    book = Book.get_by_id(book_id)

    if book is None:
        print("Error: Libro no encontrado.")
        return False

    if user is None:
        print ("Error: Usuario no encontrado")
        return False
    
    if not verifyFines(user):
        print("Error: El Usuario tiene pendiente el pago de multas de más de $20.000, no se puede realizar la compra")
        return False

    if hasBorrowed(user_id, book_id):
        print("Error: Actualmente tienes este libro prestado, no puedes comprarlo")
        return False

    if book_type == 'Digital':
        price =book.price_digital
    elif book_type == 'Physical':
        if book.store_physical_stock < quantity:
            print("Error: No hay suficientes copias de este libro. Cantidad disponible: {book.store_physical_stock}.")    
            return False

        reservation_id = reserve_stock(book_id, quantity)
        if not reservation_id:
            return False
            
        price = book.physical_price
    else:
        print("Error: Tipo de libro no válido.")
        return False  

    totalPrice = price * quantity
    final_discount = 0
    if quantity>5:
        final_discount += 0.15
    elif quantity>3:
        final_discount += 0.10

    if user.user_type == 'Professor' and book.category == 'Academic':
        final_discount += 0.20
    elif user.user_type == 'Student' and book_type == 'Digital':
        final_discount += 0.15
    finalPrice = totalPrice * (1 - final_discount)      

    connection = connect_to_db()
    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        purchase_query = "INSERT INTO purchases (user_id, purchase_date, total_paid) VALUES (%s, %s, %s)"
        cursor.execute(purchase_query, (user_id, datetime.date.today(), final_price))
        purchase_id = cursor.lastrowid

        details_query = "INSERT INTO purchase_details (purchase_id, book_id, book_type, quantity, unit_price, discount) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(details_query, (purchase_id, book_id, book_type, quantity, price, discount_amount))
        
        if book_type == 'Physical':
            update_stock_query = "UPDATE books SET store_physical_stock = store_physical_stock - %s WHERE id = %s"
            cursor.execute(update_stock_query, (quantity, book_id))
            delete_reserve_query = "DELETE FROM stock_reservations WHERE id = %s"
            cursor.execute(delete_reserve_query, (reservation_id,))
        
        connection.commit()
        print(f"Compra realizada con éxito. Total pagado: ${final_price:.2f}.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al registrar la compra: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()