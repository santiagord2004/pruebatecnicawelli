import mysql.connector
from db import connect_to_db
import datetime

def putFines(user_id, loan_id, amount, reason):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor()

    query = "INSERT INTO fines (user_id, loan_id, monto, razon, fecha_creacion) VALUES (%s, %s, %s, %s, %s)"
    user_update_query = "UPDATE users SET pending_fines = pending_fines + %s WHERE id = %s"
    today = datetime.date.today()

    try:
        cursor.execute(query, (user_id, loan_id, amount, reason, today))
        cursor.execute(user_update_query, (amount, user_id))
        connection.commit()
        print(f"Multa de ${amount} aplicada al usuario {user_id} por {reason}.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al aplicar la multa: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()

def lostBook(loan_id):
    connection = connect_to_db()
    if connection is None:
        return False
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT user_id, book_id FROM loans WHERE id = %s AND status = 'Loaned'"
    cursor.execute(query, (loan_id,))
    loan_info = cursor.fetchone()

    if not loan_info:
        print("Error: Préstamo no encontrado o ya no está activo.")
        return False

    fine_amount = 5000 
    putFines(loan_info['user_id'], loan_id, fine_amount, "Pérdida de libro prestado")
    
    update_loan_query = "UPDATE loans SET status = 'Lost' WHERE id = %s"
    update_book_query = "UPDATE books SET status = 'Mantenimiento' WHERE id = %s" 
    
    try:
        cursor.execute(update_loan_query, (loan_id,))
        cursor.execute(update_book_query, (loan_info['book_id'],))
        connection.commit()
        print(f"Se ha registrado la pérdida del libro y aplicado una multa de ${fine_amount}.")
        return True
    except mysql.connector.Error as err:
        print(f"Error al registrar la pérdida: {err}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()
