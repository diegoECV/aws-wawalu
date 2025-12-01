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
    profile_image_data MEDIUMBLOB,
    profile_image_type VARCHAR(50),
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
    is_approved BOOLEAN DEFAULT FALSE -- Por defecto requiere aprobación del administrador
);

-- ========================================
-- TABLA DE ADMISIONES
-- ========================================

CREATE TABLE IF NOT EXISTS admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_name VARCHAR(100) NOT NULL,
    parent_lastname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    doc_type VARCHAR(20) NOT NULL,
    doc_number VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    parent_dob DATE,
    program VARCHAR(100) NOT NULL,
    message TEXT,
    child_name VARCHAR(100) NOT NULL,
    child_lastname VARCHAR(100) NOT NULL,
    child_dob DATE NOT NULL,
    child_gender ENUM('M', 'F', 'Other') NOT NULL,
    allergies VARCHAR(255),
    medical_observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    user_id INT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_email (email),
    INDEX idx_doc_number (doc_number)
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
    image_data MEDIUMBLOB,
    image_type VARCHAR(50),
    category VARCHAR(50),
    stock INT DEFAULT 0,
    material VARCHAR(50),
    usage_info TEXT,
    dimensions TEXT,
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

CREATE TABLE IF NOT EXISTS galery_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    image_url VARCHAR(255) NOT NULL,
    image_data MEDIUMBLOB,
    image_type VARCHAR(50),
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
    image_data MEDIUMBLOB,
    image_type VARCHAR(50),
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

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    meal_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE REPORTES DE ESTUDIANTES
-- ========================================

CREATE TABLE IF NOT EXISTS student_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL, 
    user_id INT NOT NULL, 
    title VARCHAR(100) NOT NULL,
    content TEXT,
    file_url VARCHAR(255), -- For PDF reports
    file_data MEDIUMBLOB,
    file_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- ========================================
-- TABLA DE PROGRAMAS ACADÉMICOS
-- ========================================

CREATE TABLE IF NOT EXISTS programs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    age_range VARCHAR(50), -- e.g. "3-4 años"
    academic_year YEAR NOT NULL,
    registration_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    monthly_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    capacity INT NOT NULL DEFAULT 20,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- TABLA DE PEDIDOS (ORDERS)
-- ========================================

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'completed', 'cancelled') DEFAULT 'pending',
    payment_method ENUM('yape', 'transfer', 'cash') NOT NULL,
    shipping_address TEXT NOT NULL,
    shipping_phone VARCHAR(20) NOT NULL,
    shipping_name VARCHAR(100) NOT NULL,
    shipping_lastname VARCHAR(100) NOT NULL,
    shipping_email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE ITEMS DEL PEDIDO (ORDER ITEMS)
-- ========================================

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- ========================================
-- TABLA DE ESTUDIANTES (STUDENTS)
-- ========================================

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parent_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    allergies TEXT,
    medical_info TEXT,
    -- Documentos requeridos
    parent_id_front VARCHAR(255),  -- Foto DNI padre/madre (frontal)
    parent_id_front_data MEDIUMBLOB,
    parent_id_front_type VARCHAR(50),
    parent_id_back VARCHAR(255),   -- Foto DNI padre/madre (reverso)
    parent_id_back_data MEDIUMBLOB,
    parent_id_back_type VARCHAR(50),
    birth_certificate VARCHAR(255), -- Certificado de nacimiento
    birth_certificate_data MEDIUMBLOB,
    birth_certificate_type VARCHAR(50),
    student_photo VARCHAR(255),     -- Foto del estudiante
    student_photo_data MEDIUMBLOB,
    student_photo_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_parent (parent_id)
);


-- ========================================
-- TABLA DE MATRÍCULAS (ENROLLMENTS)
-- ========================================

CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    program_id INT NOT NULL,
    enrollment_year INT NOT NULL,
    enrollment_period VARCHAR(20) DEFAULT 'Anual',
    status ENUM('pending', 'active', 'inactive', 'rejected') DEFAULT 'pending',
    observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE RESTRICT,
    INDEX idx_student (student_id),
    INDEX idx_program (program_id),
    INDEX idx_status (status)
);

-- ========================================
-- TABLA DE CURSOS (PHASE 1)
-- ========================================
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    teacher_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE NOTAS (PHASE 1)
-- ========================================
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL,
    course_id INT NOT NULL,
    period VARCHAR(20) NOT NULL, -- e.g., 'Bimestre 1', 'Bimestre 2'
    grade DECIMAL(5, 2),
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE ASISTENCIA (PHASE 1)
-- ========================================
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'excused') NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance (enrollment_id, date)
);

-- ========================================
-- TABLA DE HORARIO (PHASE 1)
-- ========================================
CREATE TABLE IF NOT EXISTS class_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    day_of_week ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE PENSIONES (PHASE 2)
-- ========================================
CREATE TABLE IF NOT EXISTS pensions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_id INT NOT NULL,
    month VARCHAR(20) NOT NULL, -- e.g., 'Marzo', 'Abril'
    amount DECIMAL(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('pending', 'paid', 'overdue') DEFAULT 'pending',
    payment_date DATE,
    receipt_url VARCHAR(255),
    receipt_data MEDIUMBLOB,
    receipt_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enrollment_id) REFERENCES enrollments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_pension (enrollment_id, month, due_date)
);

-- ========================================
-- TABLA DE DOCUMENTOS DEL ESTUDIANTE (PHASE 2)
-- ========================================
CREATE TABLE IF NOT EXISTS student_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    title VARCHAR(100) NOT NULL, -- e.g., 'Constancia de Estudios', 'Certificado de Notas'
    description TEXT,
    file_url VARCHAR(255) NOT NULL,
    file_data MEDIUMBLOB,
    file_type VARCHAR(50),
    document_type ENUM('certificate', 'report', 'administrative') NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE TAREAS (PHASE 3)
-- ========================================
CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATETIME,
    file_url VARCHAR(255),
    file_data MEDIUMBLOB,
    file_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE ENTREGAS (PHASE 3)
-- ========================================
CREATE TABLE IF NOT EXISTS submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    student_id INT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_url VARCHAR(255),
    file_data MEDIUMBLOB,
    file_type VARCHAR(50),
    comments TEXT,
    grade DECIMAL(5, 2),
    status ENUM('submitted', 'graded', 'late') DEFAULT 'submitted',
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ========================================
-- TABLA DE MENSAJES INTERNOS (PHASE 3)
-- ========================================
CREATE TABLE IF NOT EXISTS internal_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
);

COMMIT;

-- ========================================
-- DATOS INICIALES (SEMILLA)
-- ========================================

-- Usuario Admin (Password: admin123)
-- Nota: El hash puede variar, se recomienda cambiar la contraseña al primer inicio o generar uno nuevo.
INSERT INTO users (name, email, password, role, is_admin, is_active, email_verified)
VALUES ('Administrador', 'admin@wawalu.edu.pe', 'scrypt:32768:8:1$SesahuA98bZekZ$f31ce9996461f0777eec1e8a15dbabaf', 'admin', TRUE, TRUE, TRUE);

-- Programas
INSERT INTO programs (name, description, age_range, academic_year, registration_fee, monthly_fee, capacity) VALUES 
('Nido (2 años)', 'Programa de estimulación temprana y socialización.', '2 años', 2025, 350.00, 450.00, 15),
('Pre-Kinder (3 años)', 'Desarrollo de habilidades motoras y cognitivas.', '3 años', 2025, 350.00, 480.00, 18),
('Kinder (4 años)', 'Preparación pre-escolar y lectoescritura.', '4 años', 2025, 350.00, 500.00, 20),
('Pre-School (5 años)', 'Consolidación de habilidades para primaria.', '5 años', 2025, 350.00, 520.00, 20);

-- Noticias de Ejemplo
INSERT INTO news (title, content) VALUES 
('¡Bienvenidos al Año Escolar 2025!', 'Estamos muy emocionados de iniciar un nuevo año lleno de aprendizaje y diversión. Las clases inician el 1 de Marzo.'),
('Feria de Ciencias', 'Nuestros pequeños científicos presentarán sus proyectos este viernes en el patio principal.');

-- Productos de Ejemplo
INSERT INTO products (name, description, price, category, stock, material) VALUES 
('Uniforme de Verano - Polo', 'Polo de algodón pima con logo bordado.', 45.00, 'Uniformes', 100, 'Algodón'),
('Uniforme de Verano - Short', 'Short azul marino resistente.', 35.00, 'Uniformes', 100, 'Drill'),
('Pack de Útiles Nido', 'Lista completa de útiles para el aula de 2 años.', 250.00, 'Útiles', 50, 'Varios');

-- Galería de Ejemplo
INSERT INTO galery_items (title, category, description, image_url) VALUES 
('Día del Logro', 'Eventos', 'Nuestros alumnos demostrando lo aprendido.', 'default_gallery.png'),
('Visita al Zoológico', 'Salidas', 'Un día divertido conociendo a los animales.', 'default_gallery.png');

