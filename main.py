import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import createUsers
import bookCreate
from db import connect_to_db
from users import User
from books import Book
from loans import makeLoan, returnBook, extendLoan
from shop import purchase
from fines import lostBook, putFines
from stock import manageStock, autoReorder
from reports import mostPopularBooks, usersWithMostFines, salesByCategory, mostPurchasingUsers, mostReservingUsers

def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_choice():
    return input("Selecciona una opción: ").strip()

def initialize_data():
    clear_screen()
    print("\n--- Inicializar Datos ---")
    print("1. Crear usuarios de prueba")
    print("2. Crear libros de prueba")
    print("0. Volver al menú principal")
    
    choice = get_user_choice()
    
    if choice == '1':
        createUsers.create()
        print("Usuarios de prueba creados con éxito.")
    elif choice == '2':
        bookCreate.create() 
        print("Libros de prueba creados con éxito.")
    elif choice == '0':
        pass
    else:
        print("Opción no válida. Intenta de nuevo.")
        
    input("\nPresiona Enter para continuar...")

def run_tests():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Inicializar datos de usuarios y libros")
        print("2. Gestión de Préstamos")
        print("3. Gestión de Compras")
        print("4. Gestión de Stock")
        print("5. Generar Reportes")
        print("0. Salir")
        
        choice = get_user_choice()

        if choice == '1':
            initialize_data()
        elif choice == '2':
            loan_menu()
        elif choice == '3':
            shop_menu()
        elif choice == '4':
            stock_menu()
        elif choice == '5':
            report_menu()
        elif choice == '0':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def loan_menu():
    while True:
        clear_screen()
        print("\n--- Gestión de Préstamos ---")
        print("1. Realizar un préstamo")
        print("2. Devolver un libro")
        print("3. Extender un préstamo (Profesor)")
        print("4. Reportar un libro como perdido")
        print("0. Volver al menú principal")
        
        choice = get_user_choice()
        
        if choice == '1':
            user_id = int(input("ID del usuario: "))
            book_id = int(input("ID del libro: "))
            makeLoan(user_id, book_id)
        elif choice == '2':
            loan_id = int(input("ID del préstamo a devolver: "))
            returnBook(loan_id)
        elif choice == '3':
            loan_id = int(input("ID del préstamo a extender: "))
            extendLoan(loan_id)
        elif choice == '4':
            loan_id = int(input("ID del préstamo perdido: "))
            lostBook(loan_id)
        elif choice == '0':
            break
        else:
            print("Opción no válida.")
        
        input("\nPresiona Enter para continuar...")

def shop_menu():
    while True:
        clear_screen()
        print("\n--- Gestión de Compras ---")
        print("1. Realizar una compra")
        print("0. Volver al menú principal")
        
        choice = get_user_choice()
        
        if choice == '1':
            user_id = int(input("ID del usuario: "))
            
            items_to_buy = []
            while True:
                book_id = int(input("ID del libro (o 0 para terminar): "))
                if book_id == 0:
                    break
                quantity = int(input("Cantidad: "))
                book_type = input("Tipo de libro (Physical/Digital): ")
                
                items_to_buy.append({
                    'book_id': book_id,
                    'quantity': quantity,
                    'book_type': book_type
                })
            
            if items_to_buy:
                purchase(user_id, items_to_buy)
        
        elif choice == '0':
            break
        else:
            print("Opción no válida.")
            
        input("\nPresiona Enter para continuar...")

def stock_menu():
    while True:
        clear_screen()
        print("\n--- Gestión de Stock ---")
        print("1. Ejecutar gestión automática de stock")
        print("2. Verificar auto-reorden de stock")
        print("0. Volver al menú principal")
        
        choice = get_user_choice()
        
        if choice == '1':
            manageStock()
        elif choice == '2':
            autoReorder()
        elif choice == '0':
            break
        else:
            print("Opción no válida.")
            
        input("\nPresiona Enter para continuar...")

def report_menu():
    while True:
        clear_screen()
        print("\n--- Reportes ---")
        print("1. Libros más populares")
        print("2. Usuarios con más multas")
        print("3. Ventas por categoría")
        print("4. Tipo de usuario que más compra")
        print("5. Tipo de usuario que más reserva")
        print("0. Volver al menú principal")
        
        choice = get_user_choice()
        
        if choice == '1':
            mostPopularBooks()
        elif choice == '2':
            usersWithMostFines()
        elif choice == '3':
            salesByCategory()
        elif choice == '4':
            mostPurchasingUsers()
        elif choice == '5':
            mostReservingUsers()
        elif choice == '0':
            break
        else:
            print("Opción no válida.")
            
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    run_tests()