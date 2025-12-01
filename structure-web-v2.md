# 🏗️ Estructura Web - Wawalu Centro Educativo v2.1

## 📁 Estructura de Directorios Actualizada

```
aws-wawalu/
├── 📄 app.py                      # Aplicación Flask principal (3490 líneas)
├── 📄 schema.sql                  # Esquema completo de BD (v2.1 - BLOB Storage)
├── 📄 schema_insert.sql           # Datos de prueba
├── 📄 requirements.txt            # Dependencias Python
├── 📄 package.json                # Configuración npm (Tailwind CSS)
├── 📄 tailwind.config.js          # Configuración Tailwind
├── 📄 sitemap.xml                 # Sitemap para SEO
├── 📄 sitemap.md                  # Documentación del sitemap (actualizado)
├── 📄 structure-web.md            # Estructura del proyecto
├── 📄 README.md                   # Documentación general (actualizado)
├── 📄 VERIFICACION_APP.md         # Reporte de verificación técnica
├── 📄 update_students_columns.py  # Script de migración BD
├── 📄 .env                        # Variables de entorno (NO SUBIR)
├── 📄 .gitignore                  # Archivos ignorados
│
├── 📁 utils/                      # Utilidades del sistema
│   └── 📄 file_compression.py     # Compresión imágenes/PDFs → BLOB
│
├── 📁 static/                     # Archivos estáticos
│   ├── 📁 css/                    # 20+ archivos CSS
│   │   ├── 📄 input.css           # Entrada Tailwind
│   │   ├── 📄 output.css          # Salida compilada
│   │   ├── 📄 base.css            # Estilos base
│   │   ├── 📄 dashboard.css       # Dashboard general
│   │   └── ...                    # CSS específicos por página
│   │
│   ├── 📁 js/                     # Scripts JavaScript
│   │   ├── 📄 base.js             # Funciones globales
│   │   ├── 📄 manage_programs.js  # CRUD programas (AJAX) ⭐
│   │   ├── 📄 manage_complaints.js # Gestión quejas (AJAX) ⭐
│   │   ├── 📄 complaint_detail.js  # Detalle queja ⭐
│   │   ├── 📄 chatbot.js          # Chatbot interactivo
│   │   └── ...                    # Otros scripts
│   │
│   ├── 📁 image/                  # Imágenes (referencias, no BLOBs)
│   │   ├── 📁 logo/               # Logos institucionales
│   │   ├── 📁 products/           # Referencias productos
│   │   ├── 📁 teachers/           # Fotos docentes
│   │   └── 📁 galery/             # Referencias galería
│   │
│   └── 📁 icons/                  # Iconos y recursos
│       ├── 📁 social/             # Redes sociales
│       └── 📁 qr/                 # Códigos QR
│
├── 📁 templates/                  # Plantillas HTML (45+ archivos)
│   ├── 📄 base.html               # Layout público
│   ├── 📄 auth_base.html          # Layout autenticación
│   ├── 📄 index.html              # Inicio
│   ├── 📄 about.html              # Nosotros
│   ├── 📄 programs.html           # Programas
│   ├── 📄 admission.html          # Admisión
│   ├── 📄 contact.html            # Contacto
│   ├── 📄 complaints.html         # Libro reclamaciones
│   ├── 📄 comments.html           # Testimonios
│   ├── 📄 login.html              # Login
│   ├── 📄 store.html              # Tienda pública
│   ├── 📄 cart_public.html        # Carrito público
│   ├── 📄 galery.html             # Galería pública
│   ├── 📄 news.html               # Noticias públicas
│   ├── 📄 news-detail.html        # Detalle noticia
│   ├── 📄 cookies.html            # Cookies
│   ├── 📄 privacy.html            # Privacidad
│   ├── 📄 terms.html              # Términos
│   │
│   ├── 📁 components/             # Componentes reutilizables
│   │   └── 📄 product_card.html   # Tarjeta producto
│   │
│   └── 📁 dashboard/              # Dashboard privado (30+ archivos)
│       ├── 📄 base_dashboard.html # Layout dashboard
│       ├── 📄 index.html          # Resumen
│       ├── 📄 profile.html        # Perfil
│       ├── 📄 enrollment.html     # Matrícula ⭐
│       │
│       └── 📁 admin/              # Panel administración
│           ├── 📄 index.html      # Dashboard admin
│           │
│           ├── 📄 manage_users.html        # Usuarios
│           ├── 📄 user_form.html           # Form usuario
│           │
│           ├── 📄 manage_admissions.html   # Admisiones
│           ├── 📄 admission_form.html      # Form admisión
│           │
│           ├── 📄 manage_programs.html     # Programas ⭐
│           ├── 📄 program_form.html        # Form programa ⭐
│           ├── 📄 program_detail.html      # Detalle programa ⭐
│           │
│           ├── 📄 manage_enrollments.html  # Matrículas
│           ├── 📄 enrollment_detail.html   # Detalle matrícula
│           │
│           ├── 📄 manage_complaints.html   # Quejas ⭐
│           ├── 📄 complaint_detail.html    # Detalle queja ⭐
│           │
│           ├── 📄 manage_products.html     # Productos
│           ├── 📄 product_form.html        # Form producto
│           │
│           ├── 📄 manage_orders.html       # Pedidos
│           ├── 📄 manage_news.html         # Noticias
│           ├── 📄 manage_galery.html       # Galería
│           └── ...                         # Otras vistas
│
└── 📁 venv/                       # Entorno virtual (NO SUBIR)
```

---

## 🎯 Arquitectura del Sistema

### 🔧 Backend (Flask + PyMySQL)

```python
app.py (3490 líneas)
├── 📦 Configuración
│   ├── Variables de entorno (.env)
│   ├── Conexión MySQL (AWS RDS)
│   ├── Secret key y sesiones
│   └── Utilidades (compress_image, compress_pdf) ⭐
│
├── 🌐 Rutas Públicas (15 rutas)
│   ├── /, /about, /programs, /contact
│   ├── /admission (formulario)
│   ├── /complaints (libro reclamaciones)
│   ├── /public/shop, /public/galery, /public/news
│   └── /cookies, /privacy, /terms
│
├── 🔐 Autenticación (3 rutas)
│   ├── /login (con validación específica)
│   └── /logout
│
├── 🎓 Dashboard Estudiante/Padre (25 rutas)
│   ├── /dashboard (principal)
│   ├── /profile (gestión perfil)
│   ├── /matricula (formulario matrícula) ⭐
│   ├── Académico: /grades, /attendance, /schedule
│   ├── Admin: /payments, /documents
│   └── Tienda: /shop, /cart, /checkout, /orders
│
├── 🛡️ Dashboard Admin/Staff (78 rutas)
│   ├── Admisiones: manage, accept, reject, add, edit, delete
│   ├── Usuarios: manage, add, edit, delete
│   ├── Programas: manage, create, edit, view, delete, toggle ⭐
│   ├── Matrículas: manage, view, update_status, delete
│   ├── Quejas: manage, detail, update_status ⭐
│   ├── Productos: manage, add, edit, delete
│   ├── Pedidos: manage, update_status
│   ├── Noticias: manage, add, edit, delete
│   ├── Galería: manage, add, edit, delete
│   ├── Cursos: manage, add, edit, delete
│   └── Horarios: manage, add, delete
│
└── 🔧 APIs y Servicios (15 rutas)
    ├── /serve_image/<table>/<id> (servir BLOB) ⭐
    ├── /download/<type>/<id> (descargar BLOB) ⭐
    ├── /api/cart (REST API carrito)
    └── Otras APIs AJAX (toggle, update_status...)
```

---

## 💾 Base de Datos MySQL (wawalu_db)

### Esquema v2.1 - Almacenamiento BLOB ⭐

```
wawalu_db
├── 👤 Usuarios
│   ├── users (id, name, email, password_hash, role, phone, address, profile_picture, last_login)
│   └── students (id, parent_id, first_name, last_name, dob, gender, allergies, medical_info,
│                  parent_id_front, parent_id_front_data ⭐, parent_id_front_type ⭐,
│                  parent_id_back, parent_id_back_data ⭐, parent_id_back_type ⭐,
│                  birth_certificate, birth_certificate_data ⭐, birth_certificate_type ⭐,
│                  student_photo, student_photo_data ⭐, student_photo_type ⭐)
│
├── 🎓 Académico
│   ├── programs ⭐ (id, name, description, age_range, academic_year, fees, capacity, current_enrollment, is_active)
│   ├── courses (id, program_id, name, description, teacher_name)
│   ├── enrollments (id, student_id, program_id, enrollment_year, enrollment_period, status, observations)
│   ├── grades (id, student_id, course_id, bimester, grade, comments)
│   ├── attendance (id, student_id, date, status, comments)
│   └── class_schedule (id, course_id, day_of_week, start_time, end_time)
│
├── 💼 Administrativo
│   ├── pensions (id, student_id, month, year, amount, due_date, payment_date, status)
│   ├── student_documents (id, student_id, document_type, file_url, issue_date)
│   └── admissions (id, parent_name, parent_lastname, email, phone, doc_type, doc_number,
│                    child_name, child_lastname, child_dob, child_gender,
│                    program, allergies, medical_observations, status, user_id)
│
├── 💬 Interacción
│   ├── assignments (id, course_id, title, description, due_date, file_url, file_data ⭐, file_type ⭐)
│   ├── submissions (id, assignment_id, student_id, file_url, file_data ⭐, file_type ⭐, grade, comments)
│   ├── internal_messages (id, from_user_id, to_user_id, subject, body, is_read)
│   └── comments (id, user_id, content, is_approved, is_featured)
│
├── 🛒 Tienda
│   ├── products (id, name, description, price, stock, category, image_url, image_data ⭐, image_type ⭐)
│   ├── orders (id, user_id, total_amount, status, shipping_name, shipping_address, payment_method, payment_proof_data ⭐, payment_proof_type ⭐)
│   └── order_items (id, order_id, product_id, quantity, price_at_purchase)
│
├── 📰 Contenido
│   ├── news (id, title, content, image_url, image_data ⭐, image_type ⭐, views)
│   ├── events (id, title, description, event_date, location)
│   ├── galery_items (id, title, category, description, image_url, image_data ⭐, image_type ⭐)
│   └── menus (id, day_of_week, week_number, year, breakfast, lunch, snack)
│
└── 🔔 Otros
    ├── complaints ⭐ (id, user_id, complaint_type, product_service, description, claim_type, details,
    │                  identification_type, identification_number, phone, email, parent_name,
    │                  minor_name, address, product_details, amount, incident_description,
    │                  consumer_request, status, staff_response, created_at, updated_at)
    └── messages (id, name, email, subject, message, created_at)
```

### ⭐ Cambios v2.1

- **Almacenamiento BLOB**: Todos los archivos (imágenes, PDFs) se guardan comprimidos en la BD
- **Columnas _data**: MEDIUMBLOB (hasta 16MB por archivo)
- **Columnas _type**: VARCHAR(50) con MIME type (image/jpeg, application/pdf, etc.)
- **Sin filesystem**: Ya no se usa carpeta `static/uploads/`

---

## 🚀 Flujos de Datos Principales

### 1. Proceso de Admisión → Usuario

```
Usuario visita /admission
    ↓
Llena formulario (datos padre + hijo)
    ↓
POST /admission → INSERT INTO admissions (status='pending')
    ↓
Admin ve en /admissions/manage
    ↓
Admin hace clic en "Aceptar" (/admissions/accept/<id>)
    ↓
Sistema:
  1. Verifica si email ya existe en users
  2. Si no existe:
     - Genera contraseña = DNI del padre
     - Hashea contraseña con werkzeug
     - INSERT INTO users (role='parent')
     - INSERT INTO students (datos del hijo)
  3. UPDATE admissions SET status='accepted', user_id=X
  4. Envía email con credenciales
    ↓
Padre puede hacer login en /login ✅
```

### 2. Proceso de Matrícula (NUEVO v2.1) ⭐

```
Padre logueado accede a /matricula
    ↓
Completa formulario:
  - Datos del estudiante
  - Selecciona programa (de tabla programs)
  - Sube 4 archivos OBLIGATORIOS:
    * DNI frontal (PDF)
    * DNI reverso (PDF)
    * Certificado nacimiento (PDF)
    * Foto estudiante (JPG/PNG)
    ↓
POST /matricula
    ↓
Sistema procesa archivos:
  1. Comprime PDFs con compress_pdf() → BLOB data
  2. Comprime imagen con compress_image() → BLOB data
  3. Extrae MIME types
    ↓
INSERT INTO students (
  parent_id, first_name, last_name, dob, gender,
  parent_id_front_data ⭐, parent_id_front_type ⭐,
  parent_id_back_data ⭐, parent_id_back_type ⭐,
  birth_certificate_data ⭐, birth_certificate_type ⭐,
  student_photo_data ⭐, student_photo_type ⭐
)
    ↓
INSERT INTO enrollments (
  student_id, program_id, enrollment_year,
  enrollment_period, status='pending'
)
    ↓
Admin revisa en /enrollments/manage
    ↓
Admin aprueba: UPDATE enrollments SET status='approved' ✅
```

### 3. Gestión de Programas (NUEVO v2.1) ⭐

```
Admin accede a /programs/manage
    ↓
Ve lista con 4 estadísticas:
  - Total programas
  - Programas activos
  - Total matriculados
  - Programas con cupo lleno
    ↓
Puede:
  1. Crear programa (/programs/create)
     → Formulario con 8 campos
     → INSERT INTO programs
  
  2. Editar programa (/programs/edit/<id>)
     → Carga datos existentes
     → UPDATE programs
  
  3. Ver detalle (/programs/view/<id>)
     → Lista de estudiantes matriculados
     → Progreso de capacidad
     → Botón eliminar (con validación)
  
  4. Toggle estado (AJAX /programs/toggle/<id>)
     → Activa/desactiva programa
     → Actualiza sin recargar página
  
  5. Filtrar programas (JavaScript)
     → Por estado (todos/activos/inactivos)
     → Búsqueda en tiempo real
```

### 4. Gestión de Quejas (NUEVO v2.1) ⭐

```
Usuario público accede a /complaints
    ↓
Llena formulario oficial (16 campos):
  - Tipo de queja/reclamo
  - Datos personales
  - Descripción detallada
    ↓
POST /complaints → INSERT INTO complaints (status='pending')
    ↓
Admin accede a /complaints/manage
    ↓
Ve lista filtrable:
  - Por estado (pendiente/en proceso/resuelto)
  - Por tipo (queja/reclamo)
  - Búsqueda
    ↓
Admin hace clic en queja → /complaints/detail/<id>
    ↓
Ve toda la información + puede:
  1. Cambiar estado (AJAX /complaints/update_status/<id>)
     → pendiente → en proceso → resuelto
  2. Agregar respuesta del personal
    ↓
Sistema actualiza sin recargar (AJAX) ✅
```

### 5. Servicio de Imágenes BLOB ⭐

```
Template necesita mostrar imagen:
  <img src="/serve_image/products/{{ product.id }}">
    ↓
GET /serve_image/<table>/<id>
    ↓
Sistema:
  1. SELECT image_data, image_type FROM <table> WHERE id=<id>
  2. Convierte BLOB a bytes
  3. send_file(BytesIO(data), mimetype=type)
    ↓
Navegador muestra imagen ✅

Similar para PDFs:
  <a href="/download/parent_id_front/{{ student.id }}">
    ↓
  GET /download/<type>/<id>
    ↓
  Descarga PDF desde BLOB
```

---

## 📊 Estadísticas del Proyecto v2.1

### Código
- **app.py**: 3,490 líneas
- **Templates**: 45+ archivos HTML
- **CSS**: 20+ archivos (Tailwind + Custom)
- **JavaScript**: 15+ archivos
- **Rutas totales**: 121
  - Públicas: 15
  - Dashboard Padre: 25
  - Dashboard Admin: 78
  - APIs: 12

### Base de Datos
- **Tablas**: 23
- **Almacenamiento BLOB**: 10 tablas con columnas _data y _type
- **Filas de ejemplo**: 100+ (schema_insert.sql)

### Funcionalidades Principales
- ✅ Sistema de roles (Admin, Staff, Padre)
- ✅ Admisiones automáticas con creación de usuarios
- ✅ Matrícula digital con documentos BLOB ⭐
- ✅ CRUD completo de programas ⭐
- ✅ Libro de reclamaciones oficial ⭐
- ✅ Tienda virtual con carrito
- ✅ Gestión académica (notas, asistencia, horarios)
- ✅ Galería y noticias con imágenes BLOB
- ✅ Dashboard responsivo con Tailwind CSS

---

## 🔧 Tecnologías v2.1

### Backend
- Python 3.8+
- Flask 3.0.0
- PyMySQL (AWS RDS compatible)
- Werkzeug (seguridad)
- Pillow (compresión imágenes) ⭐
- PyPDF2 (compresión PDFs) ⭐

### Frontend
- HTML5 + Jinja2
- Tailwind CSS 3.x
- JavaScript ES6+ (AJAX, Fetch API)
- Material Symbols (iconos)

### Base de Datos
- MySQL 8.0+ (AWS RDS)
- BLOB Storage (MEDIUMBLOB) ⭐
- Índices optimizados

### Hosting
- AWS EC2 (Backend)
- AWS RDS (Database)
- GitHub (Repositorio: diegoECV/aws-wawalu)

---

_Última actualización: Diciembre 2025 - Versión 2.1_
