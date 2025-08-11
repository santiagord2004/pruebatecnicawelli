-- Crea la base de datos LIBRARY si no existe
CREATE DATABASE IF NOT EXISTS LIBRARY;

-- Selecciona la base de datos
USE LIBRARY;

-- Tabla para gestionar a los usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_type ENUM('Student', 'Professor', 'Visitor') NOT NULL,
    pending_fines DECIMAL(10, 2) DEFAULT 0.00
);

-- Tabla para gestionar los libros y su inventario
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category ENUM('Fiction', 'Academic', 'Reference', 'Research') NOT NULL,
    loanable_physical_copies INT NOT NULL,
    store_physical_stock INT NOT NULL,
    store_digital_stock INT NOT NULL,
    minimum_stock INT NOT NULL,
    physical_price DECIMAL(10, 2) NOT NULL,
    digital_price DECIMAL(10, 2) NOT NULL,
    status ENUM('Available', 'Maintenance') NOT NULL DEFAULT 'Available'
);

-- Tabla para registrar los préstamos de libros
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    loan_date DATE NOT NULL,
    expected_return_date DATE NOT NULL,
    actual_return_date DATE,
    status ENUM('Loaned', 'Returned', 'Overdue', 'Lost') NOT NULL,
    extension_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Tabla para almacenar los detalles de las compras de la tienda
CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    purchase_date DATE NOT NULL,
    total_paid DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla para el detalle de cada compra (qué libros se compraron)
CREATE TABLE purchase_details (
    purchase_id INT NOT NULL,
    book_id INT NOT NULL,
    book_type ENUM('Physical', 'Digital') NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (purchase_id) REFERENCES purchases(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Tabla para registrar las multas de los usuarios
CREATE TABLE fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    loan_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    reason VARCHAR(255) NOT NULL,
    creation_date DATE NOT NULL,
    paid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (loan_id) REFERENCES loans(id)
);

-- Tabla para gestionar las reservas de libros
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    status ENUM('Active', 'Completed', 'Canceled') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Tabla para gestionar las reservas temporales de stock para compras
CREATE TABLE stock_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    quantity INT NOT NULL,
    reservation_time DATETIME NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id)
);