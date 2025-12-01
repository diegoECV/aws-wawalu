# 🎓 Wawalu Centro Educativo

![Wawalu Banner](static/image/logo/logo.png)

> Plataforma web integral para el Centro Educativo Wawalu, basada en la metodología Reggio Emilia. Incluye sistema de inscripciones, tienda virtual, gestión administrativa, libro de reclamaciones y portal para padres.

![Estado](https://img.shields.io/badge/Estado-Producción-success)
![Versión](https://img.shields.io/badge/Versión-2.1-blue)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API](#-api)
- [Base de Datos](#-base-de-datos)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## ✨ Características

### 🏫 Portal Educativo Público

- **Información Institucional**: Páginas de "Nosotros", "Programas" y metodología.
- **Galería Multimedia**: Galería de fotos filtrable por categorías.
- **Noticias y Blog**: Sistema de noticias para mantener informada a la comunidad.
- **Calendario de Actividades**: Visualización de eventos próximos.
- **Menú de Comedor**: Visualización del menú semanal para los padres.

### 👨‍👩‍👧‍👦 Dashboard para Padres y Estudiantes

#### 📚 Gestión Académica

- **Notas**: Visualización de calificaciones por curso y bimestre.
- **Asistencia**: Registro detallado de asistencias, tardanzas y faltas.
- **Horario**: Cronograma semanal de clases.
- **Reportes**: Descarga de libretas de notas y constancias en PDF.

#### 💼 Gestión Administrativa

- **Pagos**: Estado de cuenta de pensiones y cronograma de pagos.
- **Documentos**: Solicitud y descarga de documentos administrativos.

#### 💬 Interacción

- **Tareas**: Visualización y entrega de tareas en línea.
- **Mensajería**: Comunicación interna con profesores y administrativos.

### 🛒 Tienda Virtual (E-commerce)

- **Catálogo de Productos**: Venta de uniformes, libros y materiales.
- **Carrito de Compras**: Gestión de carrito persistente en sesión.
- **Checkout**: Simulación de proceso de compra.

### 👤 Gestión de Usuarios

- **Autenticación**: Registro, inicio de sesión y cierre de sesión seguros.
- **Perfil**: Gestión de datos personales y cambio de contraseña.
- **Roles**: Sistema de roles (Padre, Staff, Admin).

### 🔧 Panel Administrativo (Admin/Staff)

- **Gestión de Contenido**: Noticias, Galería, Eventos, Menú.
- **Gestión Académica**: Cursos, Notas, Asistencia, Horarios, Programas.
- **Gestión Administrativa**: Pensiones, Documentos, Matrículas, Admisiones.
- **Gestión de Tienda**: Productos, Pedidos, Inventario.
- **Gestión de Usuarios**: Admisiones automáticas, Usuarios, Roles.
- **Libro de Reclamaciones**: Gestión completa de quejas y reclamos con seguimiento.
- **Almacenamiento en BD**: Todos los archivos (imágenes, PDFs) se guardan como BLOBs comprimidos.

---

## 🛠️ Tecnologías

### Backend

- **Lenguaje**: Python 3.8+
- **Framework**: Flask 3.0.0
- **Base de Datos**: MySQL 8.0+ (con PyMySQL)
- **Seguridad**: Werkzeug (hashing), Cryptography
- **Utilidades**: Python-dotenv

### Frontend

- **Estructura**: HTML5 (Jinja2 Templates)
- **Estilos**: Tailwind CSS (vía CDN) + CSS personalizado
- **Scripting**: JavaScript ES6+
- **Iconos**: Material Symbols (Google Fonts)

### Herramientas

- **Control de Versiones**: Git
- **Entorno Virtual**: venv
- **Gestión de Paquetes**: pip, npm

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- MySQL Server 8.0+
- Git

### Pasos

1.  **Clonar el repositorio**

    ```bash
    git clone https://github.com/diegoECV/aws-wawalu.git
    cd aws-wawalu
    ```

2.  **Configurar entorno virtual**

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Base de Datos**

    - Crea una base de datos vacía en MySQL llamada `wawalu_db`.
    - Importa el esquema completo:
      ```bash
      mysql -u root -p wawalu_db < schema.sql
      ```
    - Importa los datos de prueba:
      ```bash
      mysql -u root -p wawalu_db < schema_insert.sql
      ```

5.  **Variables de Entorno**
    - Crea un archivo `.env` en la raíz:
    ```env
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=tu_password
    DB_NAME=wawalu_db
    SECRET_KEY=tu_clave_secreta
    ```

---

## ⚙️ Configuración

El archivo `app.py` contiene la configuración principal. Asegúrate de actualizar las credenciales de base de datos si no usas variables de entorno.

```python
# Configuración de la base de datos en app.py
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'tu_password')
DB_NAME = os.getenv('DB_NAME', 'wawalu_db')
```

---

## 🎮 Uso

1.  **Iniciar la aplicación**

    ```bash
    python app.py
    ```

2.  **Acceder al navegador**
    - Frontend: `http://localhost:5000`
    - Dashboard: `http://localhost:5000/dashboard` (Requiere login)

### Credenciales de Prueba

- **Admin**: `admin@wawalu.com` / `hashed_password` (Nota: En entorno real las contraseñas están hasheadas)
- **Padre**: `padre@wawalu.com` / `hashed_password`

---

## 📁 Estructura del Proyecto

```text
aws-wawalu/
├── .git/                      # Control de versiones
├── static/                    # Archivos estáticos
│   ├── css/                   # Estilos CSS (Tailwind + Custom)
│   ├── image/                 # Imágenes del sitio
│   │   ├── logo/              # Logos institucionales
│   │   ├── products/          # Imágenes de productos
│   │   ├── teachers/          # Fotos de docentes
│   │   └── galery/            # Galería fotográfica
│   ├── js/                    # Scripts JavaScript
│   └── icons/                 # Iconos y recursos gráficos
├── templates/                 # Plantillas HTML (Jinja2)
│   ├── dashboard/             # Dashboard privado
│   │   ├── admin/             # Panel de administración
│   │   │   ├── manage_programs.html
│   │   │   ├── manage_complaints.html
│   │   │   ├── manage_admissions.html
│   │   │   ├── manage_enrollments.html
│   │   │   └── ...            # Otras vistas admin
│   │   ├── staff/             # Panel de personal
│   │   └── ...                # Vistas padre/estudiante
│   ├── components/            # Componentes reutilizables
│   └── ...                    # Plantillas públicas
├── utils/                     # Utilidades
│   └── file_compression.py    # Compresión de imágenes/PDFs
├── venv/                      # Entorno virtual Python
├── .env                       # Variables de entorno (NO SUBIR)
├── app.py                     # 🚀 Aplicación Flask principal (3490 líneas)
├── requirements.txt           # Dependencias Python
├── package.json               # Configuración Tailwind CSS
├── tailwind.config.js         # Configuración Tailwind
├── schema.sql                 # Esquema de BD (actualizado v2.1)
├── schema_insert.sql          # Datos de prueba
├── update_students_columns.py # Script de migración BD
├── sitemap.xml                # SEO sitemap
├── sitemap.md                 # Documentación del sitemap
├── structure-web.md           # Estructura del proyecto
├── VERIFICACION_APP.md        # Reporte de verificación
└── README.md                  # Esta documentación
```

---

## 🔗 API y Rutas Principales

### Públicas

- `GET /`: Inicio
- `GET /about`: Nosotros
- `GET /programs`: Programas
- `GET /admission`: Admisión
- `GET /public/shop`: Tienda pública
- `GET /public/news`: Noticias públicas

### Dashboard Estudiante/Padre

- `GET /dashboard/grades`: Notas
- `GET /dashboard/attendance`: Asistencia
- `GET /dashboard/schedule`: Horario
- `GET /dashboard/payments`: Pagos
- `GET /dashboard/assignments`: Tareas
- `GET /dashboard/messages`: Mensajería

### Dashboard Admin

- `GET /users/manage`: Gestión de usuarios
- `GET /admissions/manage`: Gestión de admisiones
- `GET /enrollments/manage`: Gestión de matrículas

---

## 🗄️ Base de Datos

El sistema utiliza MySQL con un esquema relacional completo que incluye:

### Tablas Principales

- **Usuarios**: `users`, `students` (con campos BLOB para documentos)
- **Académico**: `programs`, `courses`, `enrollments`, `grades`, `attendance`, `class_schedule`
- **Administrativo**: `pensions`, `student_documents`, `admissions`
- **Interacción**: `assignments`, `submissions`, `internal_messages`
- **Contenido**: `news`, `events`, `galery_items`, `menus` (imágenes en BLOB)
- **Tienda**: `products`, `orders`, `order_items` (imágenes en BLOB)
- **Otros**: `complaints`, `messages`, `comments`

### Características de Almacenamiento

- ✅ **Almacenamiento BLOB**: Todos los archivos (imágenes, PDFs) se guardan comprimidos en la BD
- ✅ **Columnas de tipo MEDIUMBLOB**: Para archivos de hasta 16MB
- ✅ **Columnas de MIME type**: Para identificar el tipo de archivo
- ✅ **Sin dependencia del sistema de archivos**: No requiere carpeta `uploads/`

### Tabla `students` (Actualizada v2.1)

```sql
students (
  id, parent_id, first_name, last_name, dob, gender,
  allergies, medical_info,
  -- Documentos con datos BLOB
  parent_id_front, parent_id_front_data, parent_id_front_type,
  parent_id_back, parent_id_back_data, parent_id_back_type,
  birth_certificate, birth_certificate_data, birth_certificate_type,
  student_photo, student_photo_data, student_photo_type,
  created_at, updated_at
)
```

---

## 🤝 Contribuir

1.  Haz un Fork del proyecto.
2.  Crea tu rama de funcionalidad (`git checkout -b feature/AmazingFeature`).
3.  Haz Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`).
4.  Push a la rama (`git push origin feature/AmazingFeature`).
5.  Abre un Pull Request.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 📞 Contacto

**Wawalu Centro Educativo**

- 📍 **Dirección**: Av. Mariscal Benavides 1365, Cañete, Lima, Perú
- 📧 **Email**: contacto@wawalu.edu.pe
- 📱 **WhatsApp**: +51 987 654 321
- 🌐 **Web**: [wawalu.edu.pe](http://wawalu.edu.pe)

### Desarrolladores

- **Diego Centeno** - _Full Stack Developer_ - [GitHub](https://github.com/diegoECV)

### Repositorio

- 🔗 **GitHub**: [https://github.com/diegoECV/aws-wawalu](https://github.com/diegoECV/aws-wawalu)
- 🌟 **Branch**: `version2`

## 📝 Changelog v2.1 (Diciembre 2025)

### ✨ Nuevas Funcionalidades

- ✅ **Sistema de Programas Académicos**: CRUD completo con capacidad y filtros
- ✅ **Gestión de Quejas**: Libro de reclamaciones con estados y seguimiento
- ✅ **Admisiones Automáticas**: Creación automática de usuarios al aceptar
- ✅ **Matrícula Digital**: Formulario con carga de documentos

### 🔧 Mejoras Técnicas

- ✅ **Migración a BLOB Storage**: Eliminación completa de dependencia de archivos físicos
- ✅ **Compresión de Archivos**: Imágenes y PDFs comprimidos antes de guardar
- ✅ **Validación CVE**: Verificación de vulnerabilidades en dependencias Java
- ✅ **Código Limpio**: Eliminación de prints debug y código deprecated

### 🐛 Correcciones

- ✅ Fix: Error UPLOAD_FOLDER en formulario de matrícula
- ✅ Fix: Columna 's.phone' inexistente en enrollment_detail
- ✅ Fix: HTML roto en manage_admissions y manage_users
- ✅ Fix: Botones desalineados en filtros
- ✅ Fix: Fondos negros en modales

---

_Hecho con ❤️ para la educación infantil._
