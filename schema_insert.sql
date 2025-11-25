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
INSERT INTO gallery_items (title, image_url, category) VALUES
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
