from users import User
from books import Book
from db import connect_to_db
import datetime
from fines import putFines

def verifyFines(user):
    return user.pending_fines <= 10000

def userLoans(user):
    connection = connect_to_db()

    if connection is None:
        return 0
    
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM loans WHERE user_id = %s AND status = 'Loaned'"
    cursor.execute(query, (user.id,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count

def isBookRecentlyLoanedToUser(user_id, book_id):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    query = "SELECT user_id FROM loans WHERE book_id = %s ORDER BY loan_date DESC LIMIT 1"
    cursor.execute(query, (book_id,))
    latest_loan_user_id = cursor.fetchone()
    cursor.close()
    connection.close()

    if latest_loan_user_id and latest_loan_user_id[0] == user_id:
        return True
    return False

def bookAvailability(book_id, quantity):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    query = "UPDATE books SET loanable_physical_copies = loanable_physical_copies + %s WHERE id = %s"

    try:
        cursor.execute(query, (quantity, book_id))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar la disponibilidad del libro: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def checkBookReservations(book_id):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM reservations WHERE book_id = %s AND status = 'Active'"
    cursor.execute(query, (book_id,))
    reservations_count = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return reservations_count > 0

def returnBook(loan_id):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT user_id, book_id, expected_return_date FROM loans WHERE id = %s AND status = 'Loaned'"
    cursor.execute(query, (loan_id,))
    loan_info = cursor.fetchone()

    if not loan_info:
        print("Error: Préstamo no encontrado o ya ha sido devuelto.")
        cursor.close()
        connection.close()
        return False

    today = datetime.date.today()
    days_overdue = (today - loan_info['expected_return_date']).days
    
    if days_overdue > 0:
        fine_amount = days_overdue * 2000 
        if days_overdue > 30:
            fine_amount *= 2
        
        putFines(loan_info['user_id'], loan_id, fine_amount, "Retraso en la devolución")
        print(f"Se ha aplicado una multa de ${fine_amount} al usuario.")

    update_query = "UPDATE loans SET status = 'Returned', actual_return_date = %s WHERE id = %s"
    try:
        cursor.execute(update_query, (today, loan_id))
        connection.commit()
        bookAvailability(loan_info['book_id'], 1)  
        print("Devolución de libro completada con éxito.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al devolver el libro: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def extendLoan(loan_id):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT l.user_id, l.expected_return_date, l.extension_count, u.user_type FROM loans l JOIN users u ON l.user_id = u.id WHERE l.id = %s"
    cursor.execute(query, (loan_id,))
    loan_info = cursor.fetchone()

    if not loan_info:
        print("Error: Préstamo no encontrado.")
        return False

    if loan_info['user_type'] != 'Professor':
        print("Error: Solo los Profesores pueden extender préstamos.")
        return False

    if loan_info['extension_count'] >= 1:
        print("Error: Este préstamo ya ha sido extendido una vez.")
        return False

    new_return_date = loan_info['expected_return_date'] + datetime.timedelta(days=15)
    update_query = "UPDATE loans SET expected_return_date = %s, extension_count = extension_count + 1 WHERE id = %s"
    try:
        cursor.execute(update_query, (new_return_date, loan_id))
        connection.commit()
        print(f"Préstamo extendido con éxito. Nueva fecha de devolución: {new_return_date}.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al extender el préstamo: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def makeLoan(user_id, book_id):
    user = User.get_by_id(user_id)
    book = Book.get_by_id(book_id)
    if user is None:
        print ("Error: Usuario no encontrado")
        return False 
    if not book:
        print("Error: Libro no encontrado.")
        return False

    if not verifyFines(user):
        print("Error: El usuario tiene multas pendientes de más de $10.000 y no puede pedir prestado.")
        return False

    loanLimit = {
        'Student': 3,
        'Professor': 5,
        'Visitor': 1
    }

    currentLoans = userLoans(user)
    
    if currentLoans>loanLimit.get(user.user_type):
        print(f"Error: El usuario ya alcanzó su límite de préstamos ({user_loan_limit.get(user.user_type)}).")
        return False
        
    if isBookRecentlyLoanedToUser(user_id, book_id): 
        print("Error: No se puede prestar el mismo libro dos veces seguidas al mismo usuario.") 
        return False

    
    if book.loanable_physical_copies <= 0: 
        print("Error: No hay copias físicas de este libro disponibles para préstamo.") 
        return False

    if checkBookReservations(book_id): 
        print("Error: El libro tiene reservas, las cuales tienen prioridad sobre los préstamos directos.") 
        return False

    connection = connect_to_db()
    if connection is None:
        return False
    cursor = connection.cursor()
    loan_duration = {
        'Student': 14,
        'Professor': 30,
        'Visitor': 7
    }.get(user.user_type)

    loan_date = datetime.date.today()
    expected_return_date = loan_date + datetime.timedelta(days=loan_duration)

    query = """
    INSERT INTO loans (user_id, book_id, loan_date, expected_return_date, status)
    VALUES (%s, %s, %s, %s, 'Loaned')
    """
    try:
        cursor.execute(query, (user_id, book_id, loan_date, expected_return_date))
        connection.commit()
        bookAvailability(book_id, -1)
        print("Préstamo realizado con éxito.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al registrar el préstamo: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()