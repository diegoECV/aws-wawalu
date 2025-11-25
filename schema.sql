CREATE DATABASE IF NOT EXISTS wawalu_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE wawalu_db;

-- Configurar el motor de base de datos
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET AUTOCOMMIT = 0;
START TRANSACTION;

-- ========================================
-- TABLA DE USUARIOS (BASE)
-- ========================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('padre', 'madre', 'tutor', 'staff', 'admin') NOT NULL DEFAULT 'padre',
    is_admin BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20),
    address TEXT,
    profile_image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    last_login TIMESTAMP NULL,
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_active (is_active)
);

-- ========================================
-- TABLA DE COMENTARIOS (TESTIMONIOS)
-- ========================================

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    relation VARCHAR(100) NOT NULL, -- Ej: Mamá de..., Papá de...
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT TRUE -- Por defecto aprobados para que se muestren, se puede cambiar a FALSE si se requiere moderación
);

-- ========================================
-- TABLA DE ADMISIONES
-- ========================================

CREATE TABLE IF NOT EXISTS admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    parent_dob DATE,
    program VARCHAR(100) NOT NULL,
    message TEXT,
    child_name VARCHAR(100) NOT NULL,
    child_lastname VARCHAR(100) NOT NULL,
    child_dob DATE NOT NULL,
    allergies VARCHAR(255),
    medical_observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'reviewed', 'accepted', 'rejected') DEFAULT 'pending'
);

-- ========================================
-- TABLA DE MENSAJES (CONTACTO)
-- ========================================

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

-- ========================================
-- TABLA DE RECLAMACIONES
-- ========================================

CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    doc_type VARCHAR(20) NOT NULL,
    document_number VARCHAR(20) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    good_type ENUM('producto', 'servicio') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    good_description TEXT NOT NULL,
    claim_type ENUM('reclamo', 'queja') NOT NULL,
    claim_detail TEXT NOT NULL,
    consumer_request TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'in_process', 'resolved') DEFAULT 'pending'
);

-- ========================================
-- TABLA DE PRODUCTOS (TIENDA)
-- ========================================

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255),
    category VARCHAR(50),
    stock INT DEFAULT 0,
    material VARCHAR(50),
    usage_info TEXT,
    dimensions Text,
    sizes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE EVENTOS (CALENDARIO)
-- ========================================

CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    type ENUM('academic', 'holiday', 'activity') DEFAULT 'activity',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE GALERÍA
-- ========================================

CREATE TABLE IF NOT EXISTS gallery_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    image_url VARCHAR(255) NOT NULL,
    category VARCHAR(50), -- e.g., 'deportes', 'salidas', 'promos'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE NOTICIAS
-- ========================================

CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE MENÚS (ALIMENTOS)
-- ========================================

CREATE TABLE IF NOT EXISTS menus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    meal_description TEXT NOT NULL,
    type ENUM('breakfast', 'lunch', 'snack') DEFAULT 'lunch',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE REPORTES DE ESTUDIANTES
-- ========================================

CREATE TABLE IF NOT EXISTS student_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL, -- Link to a student (could be a user or a separate student table if we had one, for now linking to users table if students are users, or just storing name)
    -- Assuming for now reports are linked to the parent's account or a specific child record. 
    -- Let's link to the parent user_id for simplicity in this phase, or we might need a 'students' table later.
    user_id INT NOT NULL, 
    title VARCHAR(100) NOT NULL,
    content TEXT,
    file_url VARCHAR(255), -- For PDF reports
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

COMMIT;
