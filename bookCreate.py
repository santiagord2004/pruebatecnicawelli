from books import Book

def create():
    libro_ejemplo = Book.create(
        title="Harry Potter y La Camara Secreta",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo2 = Book.create(
        title="Harry Potter y El Prisionero de Azakaban",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo3 = Book.create(
        title="Harry Potter y el Caliz de fuego",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo4 = Book.create(
        title="Harry Potter y La Orden del Fenix",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo5 = Book.create(
        title="Harry Potter y El Misterio del Principe",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo6 = Book.create(
        title="Harry Potter y Las Reliquias de La Muerte",
        category="Fiction",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=1000,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo7 = Book.create(
        title="El Olvido que Seremos",
        category="Academic",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=10,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo8 = Book.create(
        title="Nacho lee",
        category="Academic",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=10,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

    libro_ejemplo9 = Book.create(
        title="Algebra Baldor",
        category="Academic",
        loanable_physical_copies=3,
        store_physical_stock=20,
        store_digital_stock=10,
        minimum_stock=5,
        physical_price=40000.00,
        digital_price=30000.00,
        status="Available"  
    )

if __name__ == '__main__':
    create()