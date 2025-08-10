from users import User
from db import connect_to_db
import datetime

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
    

def makeLoan(user_id, book_id):
    user = User.get_by_id(user_id)

    if user is None:
        print ("Error: Usuario no encontrado")
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
    
    """if isBookRecentlyLoanedToUser(user, book_copy): 
        print("Error: No se puede prestar el mismo libro dos veces seguidas al mismo usuario.") 
        return False

    if book_copy.status != 'Disponible':
        print(f"Error: La copia del libro no está disponible para préstamo. Estado actual: {book_copy.status}.") 
        return False"""

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
        print("Préstamo realizado con éxito.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al registrar el préstamo: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()