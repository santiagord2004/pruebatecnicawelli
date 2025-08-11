from users import User
from books import Book
from db import connect_to_db
import mysql.connector
import datetime
from decimal import Decimal

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
    reservation_time = datetime.datetime.now()
    
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

def purchase(user_id, items_to_buy):
    user = User.get_by_id(user_id)
    if user is None:
        print("Error: Usuario no encontrado.")
        return False
    
    if not verifyFines(user):
        print("Error: El usuario tiene multas pendientes de más de $20.000 y no puede comprar.")
        return False

    total_purchase_price = Decimal('0')
    purchase_details_list = []
    

    for item in items_to_buy:
        book_id = item['book_id']
        quantity = item['quantity']
        book_type = item['book_type']

        book = Book.get_by_id(book_id)
        if book is None:
            print(f"Error: Libro con ID {book_id} no encontrado.")
            return False
            
        if hasBorrowed(user_id, book_id):
            print(f"Error: No puedes comprar el libro '{book.title}' porque lo tienes prestado.")
            return False
        if book_type == 'Digital':
            base_price = book.digital_price
        elif book_type == 'Physical':
            if book.store_physical_stock < quantity:
                print(f"Error: Stock físico insuficiente para el libro '{book.title}'. Disponible: {book.store_physical_stock}.")
                return False
            base_price = book.physical_price
        else:
            print(f"Error: Tipo de libro no válido para '{book.title}'.")
            return False
        

        discount_amount = Decimal('0')
        if user.user_type == 'Professor' and book.category == 'Academic':
            discount_amount += base_price * Decimal('0.20')
        elif user.user_type == 'Student' and book_type == 'Digital':
            discount_amount += base_price * Decimal('0.15')

        final_item_price = (base_price - discount_amount) * Decimal(str(quantity))
        total_purchase_price += final_item_price

        purchase_details_list.append({
            'book_id': book_id,
            'book_type': book_type,
            'quantity': quantity,
            'unit_price': base_price,
            'discount': discount_amount,
            'final_price': final_item_price
        })
    total_quantity_of_books = sum(item['quantity'] for item in items_to_buy)    
    
    volume_discount = Decimal('0')
    if total_quantity_of_books > 5:
        volume_discount = total_purchase_price * Decimal('0.15')
    elif total_quantity_of_books  > 3:
        volume_discount = total_purchase_price * Decimal('0.10')

    final_total_price = total_purchase_price - volume_discount
    
    connection = connect_to_db()
    if connection is None:
        return False
    cursor = connection.cursor()

    try:

        purchase_query = "INSERT INTO purchases (user_id, purchase_date, total_paid) VALUES (%s, %s, %s)"
        cursor.execute(purchase_query, (user_id, datetime.date.today(), final_total_price))
        purchase_id = cursor.lastrowid

        for item in purchase_details_list:
            details_query = "INSERT INTO purchase_details (purchase_id, book_id, book_type, quantity, unit_price, discount) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(details_query, (purchase_id, item['book_id'], item['book_type'], item['quantity'], item['unit_price'], item['discount']))
            if item['book_type'] == 'Physical':
                update_stock_query = "UPDATE books SET store_physical_stock = store_physical_stock - %s WHERE id = %s"
                cursor.execute(update_stock_query, (item['quantity'], item['book_id']))
        
        connection.commit()
        print(f"Compra realizada con éxito. Total pagado: ${final_total_price:.2f}.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al registrar la compra: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()