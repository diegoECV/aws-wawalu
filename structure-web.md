🏗️ Estructura Web - Wawalu Centro Educativo

📁 Estructura de Directorios
wawalu/
├── 📄 app.py # Aplicación Flask principal
├── 📄 schema.sql # Esquema completo de Base de Datos
├── 📄 schema_insert.sql # Datos de prueba
├── 📄 requirements.txt # Dependencias Python
├── 📄 package.json # Configuración Frontend
├── 📄 sitemap.xml # Sitemap para SEO
├── 📄 sitemap.md # Documentación del sitemap
├── 📄 structure-web.md # Este archivo
├── 📄 README.md # Documentación general
│
├── 📁 static/ # Archivos estáticos
│ ├── 📁 css/ # Estilos (Tailwind + Custom)
│ ├── 📁 js/ # Scripts JavaScript
│ ├── 📁 img/ # Imágenes del sitio
│ └── 📁 uploads/ # Archivos subidos (fotos, pdfs)
│
├── 📁 templates/ # Plantillas HTML
│ ├── 📄 base.html # Layout público
│ ├── 📄 index.html # Inicio
│ ├── 📄 about.html # Nosotros
│ ├── 📄 programs.html # Programas
│ ├── 📄 admission.html # Formulario de admisión
│ ├── 📄 contact.html # Contacto
│ ├── 📄 login.html # Login
│ ├── 📄 public_shop.html # Tienda pública
│ ├── 📄 public_news.html # Noticias públicas
│ ├── 📄 public_galery.html # Galería pública
│ ├── 📄 public_cart.html # Carrito público
│ ├── 📄 complaints.html # Libro de reclamaciones
│ │
│ └── 📁 dashboard/ # Área privada
│ ├── 📄 base_dashboard.html # Layout del dashboard
│ ├── 📄 index.html # Resumen principal
│ ├── 📄 profile.html # Perfil de usuario
│ │
│ ├── 🎓 Académico
│ ├── 📄 grades.html # Notas
│ ├── 📄 attendance.html # Asistencia
│ ├── 📄 schedule.html # Horario
│ ├── 📄 reports.html # Reportes
│ │
│ ├── 💼 Administrativo
│ ├── 📄 payments.html # Pagos
│ ├── 📄 documents.html # Documentos
│ │
│ ├── 💬 Interacción
│ ├── 📄 assignments.html # Tareas
│ ├── 📄 messages.html # Mensajería
│ │
│ ├── 🛒 Servicios
│ ├── 📄 shop.html # Tienda interna
│ ├── 📄 cart.html # Carrito interno
│ ├── 📄 checkout.html # Proceso de pago
│ ├── 📄 menu.html # Menú de comedor
│ ├── 📄 calendar.html # Calendario
│ ├── 📄 news.html # Noticias internas
│ │
│ └── 📁 admin/ # Vistas de administrador
│ ├── 📄 manage_users.html
│ ├── 📄 manage_products.html
│ ├── 📄 manage_news.html
│ ├── 📄 manage_enrollments.html
│ └── ...
│
└── 📁 venv/ # Entorno virtual Python

🎯 Arquitectura del Sistema

🔧 Backend (Flask)
app.py
├── Configuración y Conexión DB
├── Rutas Públicas (/, /about, /programs...)
├── Rutas de Autenticación (/login, /logout)
├── Rutas del Dashboard Estudiante (/dashboard/_)
├── Rutas del Dashboard Admin (/users/_, /products/\*)
└── APIs Internas (Carrito, etc.)

💾 Base de Datos (MySQL)
wawalu_db
├── 👤 Usuarios
│ ├── users # Credenciales y roles
│ └── students # Datos académicos del estudiante
│
├── 🎓 Académico
│ ├── programs # Niveles educativos
│ ├── courses # Cursos por programa
│ ├── enrollments # Matrículas
│ ├── grades # Notas por bimestre
│ ├── attendance # Registro de asistencia
│ └── class_schedule # Horario de clases
│
├── 💼 Administrativo
│ ├── pensions # Pagos de pensiones
│ ├── student_documents # Documentos administrativos
│ └── admissions # Solicitudes de vacante
│
├── 💬 Interacción
│ ├── assignments # Tareas asignadas
│ ├── submissions # Entregas de estudiantes
│ └── internal_messages # Mensajería interna
│
├── 🛒 Tienda
│ ├── products # Catálogo
│ ├── orders # Pedidos
│ └── order_items # Detalle de pedidos
│
└── 📰 Contenido
├── news # Noticias
├── events # Calendario
├── galery_items # Galería
├── menus # Comedor
├── complaints # Reclamos
└── comments # Testimonios

🚀 Flujo de Datos Principal

1.  **Admisión**:
    `admission.html` → `POST /admission` → `admissions` (table) → Admin aprueba → Crea `users` y `students`.

2.  **Matrícula**:
    Padre completa datos → `enrollments` (table) → Admin confirma → Estudiante activo.

3.  **Académico**:
    Profesor registra notas/asistencia → `grades`/`attendance` (tables) → Padre visualiza en `grades.html`.

4.  **Tareas**:
    Profesor crea tarea (`assignments`) → Estudiante ve y sube archivo (`submissions`) → Profesor califica.

5.  **Tienda**:
    Usuario agrega a carrito (Session) → Checkout (`orders` table) → Confirmación.
