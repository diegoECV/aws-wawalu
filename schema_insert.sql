-- Insert Products
INSERT INTO products (name, description, price, image_url, category, stock, material, usage_info, dimensions, sizes) VALUES
('Mandil de Arte', 'Mandil protector ideal para actividades artísticas y manualidades.', 25.00, 'apron.jpg', 'Útiles', 50, 'Poliéster impermeable', 'Uso en clases de arte y pintura', 'Talla única', NULL),
('Kit de Arte Completo', 'Set completo con todo lo necesario para la creatividad.', 85.00, 'artkit.jpg', 'Útiles', 30, 'Varios', 'Para todas las actividades creativas', NULL, NULL),
('Mochila Escolar Wawalu', 'Mochila ergonómica y resistente con diseño exclusivo.', 65.00, 'backpack.jpg', 'Accesorios', 40, 'Lona resistente', 'Uso diario escolar', '30x40x15 cm', NULL),
('Botella de Agua', 'Botella reutilizable libre de BPA.', 20.00, 'bottle.jpg', 'Accesorios', 60, 'Plástico Tritan', 'Hidratación diaria', '500ml', NULL),
('Cartuchera Organizadora', 'Cartuchera con múltiples compartimentos.', 18.00, 'case.jpg', 'Útiles', 50, 'Tela reforzada', 'Guardar lápices y útiles', '20x10x5 cm', NULL),
('Arcilla para Modelar', 'Arcilla natural no tóxica para modelado.', 12.00, 'clay.jpg', 'Materiales', 100, 'Arcilla natural', 'Clases de escultura y motricidad', '500g', NULL),
('Carpeta A4', 'Carpeta resistente para archivar trabajos.', 8.00, 'folder.jpg', 'Útiles', 100, 'Plástico duro', 'Archivar hojas de trabajo', 'A4', NULL),
('Gorro para el Sol', 'Gorro con protección UV para actividades al aire libre.', 22.00, 'hat.jpg', 'Uniforme', 45, 'Algodón y Poliéster', 'Recreo y educación física', NULL, 'S,M,L'),
('Casaca Institucional', 'Casaca abrigadora con el logo del colegio.', 90.00, 'jacket.jpg', 'Uniforme', 35, 'Polar y Taslan', 'Uso diario en invierno', NULL, '4,6,8,10,12'),
('Lonchera Térmica', 'Lonchera que mantiene la temperatura de los alimentos.', 45.00, 'lunchbox.jpg', 'Accesorios', 40, 'Interior térmico', 'Transporte de alimentos', '25x20x10 cm', NULL),
('Cuaderno Wawalu', 'Cuaderno cosido de 100 hojas con diseño institucional.', 10.00, 'notebook.jpg', 'Útiles', 200, 'Papel bond 80g', 'Cuaderno de control y tareas', 'A5', NULL),
('Set de Témperas', 'Caja de 12 témperas no tóxicas lavables.', 15.00, 'paint.jpg', 'Materiales', 80, 'Pintura al agua', 'Clases de arte', '12 colores', NULL),
('Colores Jumbo', 'Caja de 12 colores gruesos triangulares.', 18.00, 'pencils.jpg', 'Útiles', 80, 'Madera certificada', 'Dibujo y coloreado', '12 unidades', NULL),
('Polo Institucional', 'Polo de algodón piqué con bordado.', 35.00, 'polo.jpg', 'Uniforme', 100, '100% Algodón', 'Uso diario', NULL, '4,6,8,10,12'),
('Tijeras Punta Roma', 'Tijeras seguras para niños.', 5.00, 'scissors.jpg', 'Útiles', 100, 'Acero inoxidable y plástico', 'Recorte de papel', '13 cm', NULL),
('Short de Deporte', 'Short cómodo para educación física.', 30.00, 'short.jpg', 'Uniforme', 60, 'Polystel', 'Educación física y verano', NULL, '4,6,8,10,12'),
('Medias Escolares', 'Pack de 3 pares de medias blancas con logo.', 25.00, 'socks.jpg', 'Uniforme', 100, 'Algodón', 'Uso diario', NULL, '23-26, 27-30, 31-34'),
('Toalla de Mano', 'Toalla pequeña bordada para aseo personal.', 12.00, 'towels.jpg', 'Accesorios', 80, 'Algodón absorbente', 'Aseo personal', '30x30 cm', NULL),
('Uniforme Completo (Niño)', 'Set de pantalón y casaca de buzo.', 120.00, 'uniform1.jpg', 'Uniforme', 25, 'Polialgodón', 'Uniforme oficial', NULL, '4,6,8,10,12'),
('Uniforme Completo (Niña)', 'Set de pantalón y casaca de buzo.', 120.00, 'uniform2.jpg', 'Uniforme', 25, 'Polialgodón', 'Uniforme oficial', NULL, '4,6,8,10,12');

-- Insert Gallery Items
INSERT INTO galery_items (title, image_url, category) VALUES
('Clase de Arte', 'imagen1.jpg', 'Actividades'),
('Juegos en el Recreo', 'imagen2.jpg', 'Recreación'),
('Festival de Danza', 'imagen3.jpg', 'Eventos'),
('Taller de Música', 'imagen4.jpg', 'Talleres'),
('Día del Logro', 'imagen5.jpg', 'Eventos'),
('Visita al Zoológico', 'imagen6.jpg', 'Salidas'),
('Clase de Psicomotricidad', 'imagen7.jpg', 'Actividades'),
('Fiesta de Cumpleaños', 'imagen8.jpg', 'Celebraciones'),
('Taller de Cocina', 'imagen9.jpg', 'Talleres'),
('Día de la Familia', 'imagen10.jpg', 'Eventos'),
('Graduación 2024', 'imagen11.jpg', 'Eventos'),
('Feria de Ciencias', 'imagen12.jpg', 'Actividades'),
('Navidad en Wawalu', 'imagen13.jpg', 'Celebraciones');

-- Insert News
INSERT INTO news (title, content, image_url) VALUES
('Inicio del Año Escolar 2025', 'Estamos muy emocionados de dar la bienvenida a todos nuestros estudiantes para el nuevo año escolar. Hemos preparado muchas sorpresas y nuevas actividades para que este año sea inolvidable. ¡Los esperamos con los brazos abiertos!', 'imagen1.jpg'),
('Inscripciones Abiertas para Talleres de Verano', 'Ya están abiertas las inscripciones para nuestros talleres de verano "Wawalu Summer Fun". Tendremos arte, música, mini-chef, y mucho más. ¡No te quedes sin vacante!', 'imagen4.jpg'),
('Ganadores del Concurso de Dibujo', 'Felicitamos a todos los participantes de nuestro concurso anual de dibujo. El nivel de creatividad ha sido impresionante. Los ganadores serán premiados en la asamblea del lunes.', 'imagen12.jpg'),
('Mejoras en Nuestra Infraestructura', 'Durante las vacaciones hemos realizado mejoras en nuestras instalaciones, incluyendo un nuevo patio de juegos y aulas renovadas para mayor comodidad de nuestros alumnos.', 'imagen2.jpg'),
('Charla para Padres: Crianza Positiva', 'Invitamos a todos los padres de familia a nuestra próxima charla sobre crianza positiva y límites con amor, a cargo de la psicóloga educativa María Pérez. Fecha: 15 de Marzo.', 'imagen10.jpg');

-- Insert Users
INSERT INTO users (name, email, password, role, is_admin, phone, address, profile_image, is_active, email_verified) VALUES
('Admin Wawalu', 'admin@wawalu.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'admin', TRUE, '+51 999999999', 'Av. Mariscal Benavides 1365', 'admin.png', TRUE, TRUE),
('Padre Ejemplo', 'padre@wawalu.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 988888888', 'Calle Falsa 123', 'padre.png', TRUE, FALSE),
('Ana García', 'ana.garcia@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 911111111', 'Av. Arequipa 123, Lima', NULL, TRUE, TRUE),
('Carlos Mendoza', 'carlos.mendoza@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 922222222', 'Jr. Unión 456, Lima', NULL, TRUE, TRUE),
('Elena Torres', 'elena.torres@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 933333333', 'Av. Javier Prado 789, Lima', NULL, TRUE, TRUE),
('Jorge Ruiz', 'jorge.ruiz@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 944444444', 'Calle Los Pinos 321, Lima', NULL, TRUE, TRUE),
('Lucía Vargas', 'lucia.vargas@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 955555555', 'Av. La Marina 654, Lima', NULL, TRUE, TRUE),
('Miguel Castro', 'miguel.castro@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 966666666', 'Jr. Cusco 987, Lima', NULL, TRUE, TRUE),
('Patricia Flores', 'patricia.flores@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 977777777', 'Av. Brasil 159, Lima', NULL, TRUE, TRUE),
('Roberto Silva', 'roberto.silva@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 988888889', 'Calle Las Begonias 753, Lima', NULL, TRUE, TRUE),
('Sofia Morales', 'sofia.morales@test.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'padre', FALSE, '+51 999999990', 'Av. Salaverry 246, Lima', NULL, TRUE, TRUE),
('Staff Docente', 'staff@wawalu.com', 'scrypt:32768:8:1$xP3TF7XvO85bCvDx$5673fdf7aef79875319f8900c0f7628c5a992151cf9b181dc8d6a1680db4c407cfbb66e23782ac8463ba518979a5ace7bd689ff368febc8f970657f41c4d9eb8', 'staff', FALSE, '+51 910101010', 'Av. El Sol 100, Lima', 'staff.png', TRUE, TRUE);

-- Insert Programs
INSERT INTO programs (name, description, age_range, academic_year, registration_fee, monthly_fee, capacity, is_active) VALUES
('Inicial 3 años', 'Programa para niños de 3 años', '3 años', 2025, 100.00, 350.00, 20, TRUE),
('Inicial 4 años', 'Programa para niños de 4 años', '4 años', 2025, 100.00, 350.00, 20, TRUE);

-- Insert Menus
INSERT INTO menus (date, meal_description, type) VALUES
('2025-11-25', 'Arroz con pollo y ensalada', 'lunch'),
('2025-11-25', 'Fruta fresca y jugo', 'snack');

-- Insert Events
INSERT INTO events (title, description, start_date, end_date, type) VALUES
('Inicio de clases', 'Comienzo del ciclo escolar', '2025-03-01 08:00:00', NULL, 'academic'),
('Fiesta de bienvenida', 'Evento para padres y niños', '2025-03-05 10:00:00', NULL, 'activity');

-- Insert Comments
INSERT INTO comments (name, relation, comment) VALUES
('María López', 'Mamá de Juan', 'Excelente centro educativo, mi hijo está feliz.'),
('Carlos Pérez', 'Papá de Ana', 'Muy buena atención y profesores dedicados.');

-- Insert Messages
INSERT INTO messages (name, email, subject, message) VALUES
('Luis Torres', 'luis@example.com', 'Consulta de matrícula', 'Quisiera información sobre el proceso de matrícula.'),
('Ana Ruiz', 'ana@example.com', 'Horario de atención', '¿Cuál es el horario de atención en verano?');

-- Insert Complaints
INSERT INTO complaints (name, lastname, doc_type, document_number, phone, email, address, good_type, amount, good_description, claim_type, claim_detail, consumer_request) VALUES
('Pedro Gómez', 'Gómez', 'DNI', '12345678', '+51 987654321', 'pedro@example.com', 'Av. Siempre Viva 742', 'producto', 80.00, 'Mochila escolar', 'reclamo', 'La mochila llegó dañada', 'Cambio de producto');

-- Insert Students
INSERT INTO students (parent_id, first_name, last_name, dob, gender, allergies, medical_info, parent_id_front, parent_id_back, birth_certificate, student_photo) VALUES
(2, 'Juan', 'Ejemplo', '2020-05-10', 'M', 'Ninguna', 'Ninguna', 'dni_front_2_example.jpg', 'dni_back_2_example.jpg', 'birth_cert_2_example.pdf', 'student_photo_2_example.jpg'),
(2, 'Ana', 'Ejemplo', '2019-08-22', 'F', 'Polen', 'Asma leve', 'dni_front_2_example2.jpg', 'dni_back_2_example2.jpg', 'birth_cert_2_example2.pdf', 'student_photo_2_example2.jpg');

-- Insert Enrollments
INSERT INTO enrollments (student_id, program_id, enrollment_year, enrollment_period, status, observations) VALUES
(1, 1, 2025, 'Anual', 'active', 'Matrícula aprobada - Estudiante regular'),
(2, 2, 2025, 'Anual', 'pending', 'Matrícula pendiente de revisión de documentos');

-- ========================================
-- PHASE 1 DATA: ACADEMIC MANAGEMENT
-- ========================================

-- Insert Courses
INSERT INTO courses (program_id, name, description, teacher_name) VALUES
(1, 'Matemáticas Divertidas', 'Introducción a números y formas', 'Prof. María'),
(1, 'Comunicación', 'Desarrollo del lenguaje y expresión', 'Prof. Ana'),
(1, 'Psicomotricidad', 'Desarrollo motor grueso y fino', 'Prof. Carlos'),
(2, 'Pre-Matemáticas', 'Conteo, sumas simples y lógica', 'Prof. María'),
(2, 'Lectoescritura', 'Iniciación a la lectura y escritura', 'Prof. Ana'),
(2, 'Inglés Básico', 'Vocabulario y canciones en inglés', 'Teacher John');

-- Insert Class Schedule
INSERT INTO class_schedule (course_id, day_of_week, start_time, end_time, room) VALUES
(1, 'Monday', '09:00:00', '10:30:00', 'Aula 3A'),
(2, 'Tuesday', '09:00:00', '10:30:00', 'Aula 3A'),
(3, 'Wednesday', '10:00:00', '11:30:00', 'Patio'),
(4, 'Monday', '09:00:00', '10:30:00', 'Aula 4A'),
(5, 'Tuesday', '09:00:00', '10:30:00', 'Aula 4A'),
(6, 'Thursday', '11:00:00', '12:30:00', 'Aula 4A');

-- Insert Grades (for active enrollment student_id=1)
INSERT INTO grades (enrollment_id, course_id, period, grade, comments) VALUES
(1, 1, 'Bimestre 1', 18.00, 'Excelente progreso en conteo'),
(1, 2, 'Bimestre 1', 17.50, 'Participa activamente en clase'),
(1, 3, 'Bimestre 1', 19.00, 'Muy buena coordinación');

-- Insert Attendance (for active enrollment student_id=1)
INSERT INTO attendance (enrollment_id, date, status, remarks) VALUES
(1, '2025-03-01', 'present', 'Primer día de clases'),
(1, '2025-03-02', 'present', ''),
(1, '2025-03-03', 'late', 'Llegó 10 min tarde'),
(1, '2025-03-04', 'present', ''),
(1, '2025-03-05', 'absent', 'Enfermedad (Justificado)');

-- ========================================
-- PHASE 2 DATA: ADMINISTRATIVE MANAGEMENT
-- ========================================

-- Insert Pensions (for active enrollment student_id=1)
INSERT INTO pensions (enrollment_id, month, amount, due_date, status, payment_date) VALUES
(1, 'Marzo', 350.00, '2025-03-31', 'paid', '2025-03-28'),
(1, 'Abril', 350.00, '2025-04-30', 'pending', NULL),
(1, 'Mayo', 350.00, '2025-05-31', 'pending', NULL);

-- Insert Student Documents
INSERT INTO student_documents (student_id, title, description, file_url, document_type) VALUES
(1, 'Constancia de Matrícula 2025', 'Documento oficial de matrícula', 'constancia_2025.pdf', 'administrative'),
(1, 'Libreta de Notas B1', 'Reporte de notas del primer bimestre', 'libreta_b1.pdf', 'report');

-- ========================================
-- PHASE 3 DATA: INTERACTION MODULES
-- ========================================

-- Insert Assignments
INSERT INTO assignments (course_id, title, description, due_date, file_url) VALUES
(1, 'Dibujando Números', 'Dibujar y colorear los números del 1 al 5 en el cuaderno.', '2025-03-15 23:59:59', NULL),
(2, 'Mi Familia', 'Traer una foto familiar y prepararse para presentarla en clase.', '2025-03-20 23:59:59', NULL),
(4, 'Colección de Hojas', 'Recolectar 5 tipos diferentes de hojas del parque.', '2025-03-18 23:59:59', 'guia_hojas.pdf');

-- Insert Submissions (for student_id=1)
INSERT INTO submissions (assignment_id, student_id, file_url, comments, grade, status) VALUES
(1, 1, 'tarea_numeros_juan.jpg', 'Aquí está mi tarea profesora', 18.00, 'graded');

-- Insert Internal Messages
INSERT INTO internal_messages (sender_id, recipient_id, subject, content, is_read) VALUES
(1, 2, 'Bienvenida', 'Bienvenido a la plataforma Wawalu. Estamos para servirle.', FALSE),
(2, 1, 'Consulta sobre uniforme', 'Buenas tardes, ¿dónde puedo adquirir el uniforme de verano?', FALSE);

-- Insert Menu Items
INSERT INTO menu_items (day, type, meal_description) VALUES
('Lunes', 'breakfast', 'Avena con manzana y tostadas'),
('Lunes', 'lunch', 'Lentejas con arroz y ensalada fresca'),
('Lunes', 'snack', 'Yogurt con cereales'),
('Martes', 'breakfast', 'Quinoa carretillera con pan con queso'),
('Martes', 'lunch', 'Pollo al horno con puré de papas'),
('Martes', 'snack', 'Fruta picada (Papaya y Piña)'),
('Miércoles', 'breakfast', 'Jugo de papaya y sándwich de pollo'),
('Miércoles', 'lunch', 'Tallarines rojos con carne'),
('Miércoles', 'snack', 'Galletas de avena caseras'),
('Jueves', 'breakfast', 'Leche con chocolate y pan con huevo'),
('Jueves', 'lunch', 'Ají de gallina con arroz y huevo duro'),
('Jueves', 'snack', 'Mazamorra morada'),
('Viernes', 'breakfast', 'Ponche de habas y pan con palta'),
('Viernes', 'lunch', 'Pescado frito con arroz y lentejas'),
('Viernes', 'snack', 'Gelatina con leche');

-- ============================================================================
-- EJEMPLOS DE OPERACIONES CRUD (CREATE, READ, UPDATE, DELETE)
-- ============================================================================
-- Los siguientes ejemplos muestran cómo realizar operaciones comunes en la base de datos
-- ¡IMPORTANTE! Estos son ejemplos educativos. Descomenta solo las que necesites ejecutar.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- UPDATE (EDITAR) - Ejemplos de actualización de registros
-- ----------------------------------------------------------------------------

-- Ejemplo 1: Actualizar el precio de un producto específico
-- UPDATE products 
-- SET price = 45.00, stock = 100 
-- WHERE name = 'Polo Manga Corta Wawalu' AND category = 'uniforms';

-- Ejemplo 2: Actualizar múltiples productos de una categoría
-- UPDATE products 
-- SET stock = stock + 50 
-- WHERE category = 'uniforms';

-- Ejemplo 3: Cambiar la categoría de un elemento de galería
-- UPDATE galery_items 
-- SET category = 'eventos' 
-- WHERE title = 'Actividad cultural en el patio' AND category = 'facilities';

-- Ejemplo 4: Actualizar información de un usuario
-- UPDATE users 
-- SET phone = '987654321', address = 'Av. Nueva Dirección 456, Lima' 
-- WHERE email = 'padre@wawalu.com';

-- Ejemplo 5: Marcar noticias como destacadas
-- UPDATE news 
-- SET featured = TRUE 
-- WHERE title LIKE '%Inauguración%';

-- Ejemplo 6: Actualizar el estado de un programa
-- UPDATE programs 
-- SET is_active = FALSE, enrollment_end = '2024-12-31' 
-- WHERE program_name = 'Inicial 3 años' AND academic_year = '2023';

-- Ejemplo 7: Modificar el stock cuando se agota un producto
-- UPDATE products 
-- SET stock = 0, is_available = FALSE 
-- WHERE id = 5;

-- Ejemplo 8: Actualizar precio con descuento del 10%
-- UPDATE products 
-- SET price = price * 0.9 
-- WHERE category = 'supplies' AND stock > 50;

-- ----------------------------------------------------------------------------
-- DELETE (ELIMINAR) - Ejemplos de eliminación de registros
-- ----------------------------------------------------------------------------

-- Ejemplo 1: Eliminar una noticia antigua específica
-- DELETE FROM news 
-- WHERE title = 'Charla sobre Nutrición Infantil' AND created_at < '2024-01-01';

-- Ejemplo 2: Eliminar productos sin stock y no disponibles
-- DELETE FROM products 
-- WHERE stock = 0 AND is_available = FALSE;

-- Ejemplo 3: Eliminar elementos de galería de una categoría
-- DELETE FROM galery_items 
-- WHERE category = 'eventos' AND image_url LIKE '%2023%';

-- Ejemplo 4: Eliminar usuarios inactivos (sin estudiantes asociados)
-- DELETE FROM users 
-- WHERE role = 'padre' 
-- AND id NOT IN (SELECT DISTINCT parent_id FROM students WHERE parent_id IS NOT NULL);

-- Ejemplo 5: Eliminar un producto específico por ID
-- DELETE FROM products 
-- WHERE id = 15;

-- Ejemplo 6: Eliminar noticias de más de 2 años
-- DELETE FROM news 
-- WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Ejemplo 7: Eliminar menú semanal de una semana específica
-- DELETE FROM weekly_menu 
-- WHERE day = 'Lunes' AND meal_type = 'breakfast';

-- ----------------------------------------------------------------------------
-- SELECT (CONSULTAR) - Ejemplos de consultas útiles
-- ----------------------------------------------------------------------------

-- Ejemplo 1: Buscar todos los productos de una categoría
-- SELECT * FROM products WHERE category = 'uniforms' ORDER BY price ASC;

-- Ejemplo 2: Contar cuántos productos hay por categoría
-- SELECT category, COUNT(*) as total, SUM(stock) as stock_total 
-- FROM products 
-- GROUP BY category;

-- Ejemplo 3: Buscar noticias recientes con límite
-- SELECT title, content, created_at 
-- FROM news 
-- ORDER BY created_at DESC 
-- LIMIT 5;

-- Ejemplo 4: Buscar usuarios por rol
-- SELECT name, email, phone, role 
-- FROM users 
-- WHERE role = 'padre';

-- Ejemplo 5: Buscar productos con stock bajo (menos de 20)
-- SELECT name, category, stock, price 
-- FROM products 
-- WHERE stock < 20 AND is_available = TRUE 
-- ORDER BY stock ASC;

-- Ejemplo 6: Buscar elementos de galería por categoría
-- SELECT title, category, image_url 
-- FROM galery_items 
-- WHERE category = 'facilities';

-- Ejemplo 7: Buscar estudiantes con su información de padres (JOIN)
-- SELECT s.first_name, s.last_name, s.birth_date, u.name as parent_name, u.email as parent_email
-- FROM students s
-- INNER JOIN users u ON s.parent_id = u.id
-- WHERE s.grade = 'Inicial 3 años';

-- Ejemplo 8: Buscar pedidos con sus productos (JOIN)
-- SELECT o.id, o.total, o.status, u.name, u.email
-- FROM orders o
-- INNER JOIN users u ON o.user_id = u.id
-- WHERE o.status = 'completed'
-- ORDER BY o.created_at DESC;

-- ----------------------------------------------------------------------------
-- TRANSACCIONES - Ejemplos de operaciones múltiples
-- ----------------------------------------------------------------------------

-- Ejemplo 1: Actualizar precio y stock en una transacción
-- START TRANSACTION;
-- UPDATE products SET price = 55.00 WHERE id = 1;
-- UPDATE products SET stock = stock - 10 WHERE id = 1;
-- COMMIT;

-- Ejemplo 2: Eliminar producto y sus referencias
-- START TRANSACTION;
-- DELETE FROM order_items WHERE product_id = 10;
-- DELETE FROM products WHERE id = 10;
-- COMMIT;

-- Ejemplo 3: Rollback en caso de error
-- START TRANSACTION;
-- UPDATE products SET price = -50.00 WHERE id = 1; -- Error: precio negativo
-- ROLLBACK; -- Deshacer cambios si hay error

-- ============================================================================
-- NOTAS IMPORTANTES:
-- ============================================================================
-- 1. Siempre haz un SELECT antes de hacer UPDATE o DELETE para verificar qué registros afectarás
-- 2. Usa WHERE en tus UPDATE y DELETE, o modificarás/eliminarás TODA la tabla
-- 3. Considera usar LIMIT en DELETE para eliminar por lotes
-- 4. Haz respaldos antes de ejecutar DELETE masivos
-- 5. Usa transacciones (START TRANSACTION, COMMIT, ROLLBACK) para operaciones críticas
-- 6. Verifica las relaciones de clave foránea antes de eliminar registros
-- ============================================================================
