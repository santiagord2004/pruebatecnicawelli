# test_loans.py

from users import User
from books import Book
from loans import makeLoan, returnBook, extendLoan
from db import connect_to_db

def run_tests():
    print("Iniciando pruebas del módulo de préstamos...\n")

    # --- SETUP: CREAR USUARIOS Y LIBROS ---
    print("Paso 1: Creando usuarios y libros de prueba.")
    user_student = User.create("Test Student", "Estudiante")
    user_professor = User.create("Test Professor", "Profesor")
    book1 = Book.create("Libro de Prueba 1", "Ficción", 5, 10, 100, 2, 25.0, 15.0)
    book2 = Book.create("Libro de Prueba 2", "Académico", 2, 5, 50, 1, 30.0, 20.0)
    book3 = Book.create("Libro de Prueba 3", "Ficción", 1, 2, 20, 1, 10.0, 5.0)

    # --- PRUEBA 1: PRÉSTAMO EXITOSO ---
    print("\nPrueba 1: Préstamo exitoso a un estudiante.")
    result = makeLoan(user_student.id, book1.id)
    if result:
        print("✅ Éxito: El préstamo fue exitoso.")
    else:
        print("❌ Fallo: El préstamo debería haber sido exitoso.")

    # --- PRUEBA 2: PRÉSTAMO FALLIDO POR LÍMITE DE LIBROS (para un estudiante) ---
    print("\nPrueba 2: Préstamo fallido por límite de libros.")
    makeLoan(user_student.id, book2.id)
    makeLoan(user_student.id, book3.id)
    result = makeLoan(user_student.id, book1.id) # Intento de prestar un 4to libro
    if not result:
        print("✅ Éxito: El préstamo fue rechazado correctamente por el límite.")
    else:
        print("❌ Fallo: El préstamo debería haber sido rechazado.")

    # --- PRUEBA 3: EXTENSIÓN DE PRÉSTAMO (para un profesor) ---
    print("\nPrueba 3: Extensión de préstamo para un profesor.")
    loan_id = get_last_loan_id_by_user(user_professor.id) # Tendrías que implementar esta función
    if loan_id:
        result = extendLoan(loan_id)
        if result:
            print("✅ Éxito: La extensión del préstamo fue exitosa.")
        else:
            print("❌ Fallo: La extensión del préstamo debería haber sido exitosa.")

    print("\nPruebas finalizadas.")

def get_last_loan_id_by_user(user_id):
    # Función auxiliar para obtener el ID del último préstamo de un usuario
    pass

if __name__ == "__main__":
    run_tests()