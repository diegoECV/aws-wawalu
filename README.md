# 🎓 Wawalu Centro Educativo

![Wawalu Banner](static/img/banner.jpg)

> Plataforma web integral para el Centro Educativo Wawalu, basada en la metodología Reggio Emilia. Incluye sistema de inscripciones, tienda virtual, gestión administrativa, libro de reclamaciones y portal para padres.

![Estado](https://img.shields.io/badge/Estado-Activo-success)
![Versión](https://img.shields.io/badge/Versión-2.0-blue)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)

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
- **Gestión Académica**: Cursos, Notas, Asistencia, Horarios.
- **Gestión Administrativa**: Pensiones, Documentos, Matrículas.
- **Gestión de Tienda**: Productos, Pedidos.
- **Gestión de Usuarios**: Admisiones, Usuarios, Reclamos.

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
    git clone https://github.com/vallegrande/ASE251S2_T13_wp.git
    cd ASE251S2_T13_wp
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
wawalu/
├── .git/                # Control de versiones
├── static/              # Archivos estáticos
│   ├── css/             # Estilos CSS
│   ├── img/             # Imágenes del sitio
│   ├── js/              # Scripts JavaScript
│   └── uploads/         # Archivos subidos
├── templates/           # Plantillas HTML (Jinja2)
│   ├── dashboard/       # Plantillas del panel administrativo
│   │   ├── admin/       # Vistas de administrador
│   │   ├── staff/       # Vistas de personal
│   │   └── ...          # Vistas de estudiante/padre
│   └── ...              # Plantillas públicas
├── venv/                # Entorno virtual Python
├── .env                 # Variables de entorno
├── app.py               # 🚀 Aplicación principal Flask
├── requirements.txt     # Dependencias Backend
├── schema.sql           # Estructura de Base de Datos (Completa)
├── schema_insert.sql    # Datos de prueba (Completo)
└── README.md            # Documentación
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

El sistema utiliza MySQL con un esquema relacional completo que incluye tablas para:

- **Usuarios**: `users`, `students`
- **Académico**: `programs`, `courses`, `enrollments`, `grades`, `attendance`, `class_schedule`
- **Administrativo**: `pensions`, `student_documents`, `admissions`
- **Interacción**: `assignments`, `submissions`, `internal_messages`
- **Contenido**: `news`, `events`, `galery_items`, `menus`
- **Tienda**: `products`, `orders`, `order_items`
- **Otros**: `complaints`, `messages`, `comments`

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
- 🌐 **Web**: [wawalu.com](http://wawalu.com)

### Desarrolladores

- **Diego Centeno** - _Full Stack Developer_ - [GitHub](https://github.com/vallegrande)

---

_Hecho con ❤️ para la educación infantil._
