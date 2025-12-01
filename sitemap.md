# Mapa del Sitio - Wawalu Centro Educativo

## 🌐 Área Pública

Accesible para todos los visitantes sin autenticación.

### Páginas Institucionales
- `/` - **Inicio**: Página principal con testimonios, metodología Reggio Emilia y bienvenida.
- `/about` - **Nosotros**: Historia, misión, visión y equipo docente.
- `/programs` - **Programas**: Información sobre niveles educativos y metodología.
- `/contact` - **Contacto**: Formulario de contacto general y ubicación.

### Procesos
- `/admission` - **Admisión**: Formulario de solicitud de vacante con datos del niño.
- `/complaints` - **Libro de Reclamaciones**: Registro oficial de quejas y reclamos.

### Servicios Públicos
- `/public/shop` - **Tienda**: Catálogo de productos, uniformes y materiales.
- `/public/cart` - **Carrito**: Vista del carrito de compras (sin login).
- `/public/galery` - **Galería**: Fotos de eventos y actividades institucionales.
- `/public/news` - **Noticias**: Comunicados y novedades institucionales.
- `/news/<id>` - **Detalle de Noticia**: Visualización completa de una noticia.

### Legal
- `/cookies` - **Política de Cookies**: Información sobre uso de cookies.
- `/privacy` - **Privacidad**: Política de privacidad y protección de datos.
- `/terms` - **Términos y Condiciones**: Términos de uso del sitio.

### Autenticación
- `/login` - **Iniciar Sesión**: Acceso a la plataforma (padres, staff, admin).
- `/logout` - **Cerrar Sesión**: Cierre de sesión seguro.

## 🎓 Dashboard (Padres y Estudiantes)

Requiere inicio de sesión. Vista personalizada según rol.

### General
- `/dashboard` - **Panel Principal**: Resumen con accesos directos y estadísticas.
- `/profile` - **Perfil**: Gestión de datos personales, foto y cambio de contraseña.
- `/dashboard/guide` - **Guía**: Tutorial de uso de la plataforma.

### Académico
- `/dashboard/grades` - **Notas**: Calificaciones por curso, bimestre y promedio.
- `/dashboard/attendance` - **Asistencia**: Registro detallado con estadísticas de asistencias/faltas.
- `/dashboard/schedule` - **Horario**: Cronograma de clases semanal por estudiante.
- `/dashboard/assignments` - **Tareas**: Lista de tareas pendientes y entrega de trabajos.
- `/reports` - **Reportes**: Descarga de libretas y documentos académicos en PDF.

### Administrativo
- `/matricula` - **Matrícula**: Formulario de inscripción con carga de documentos.
- `/dashboard/payments` - **Pagos**: Estado de pensiones, cronograma y comprobantes.
- `/dashboard/documents` - **Documentos**: Solicitud y descarga de constancias y certificados.

### Recursos y Servicios
- `/calendar` - **Calendario**: Eventos escolares y fechas importantes.
- `/menu` - **Menú**: Comedor escolar y sugerencias de loncheras saludables.
- `/galery` - **Galería Privada**: Fotos exclusivas para la comunidad educativa.
- `/news` - **Noticias**: Comunicados internos y circulares.

### Tienda Virtual
- `/shop` - **Tienda**: Compra de uniformes, útiles y materiales educativos.
- `/cart` - **Carrito**: Gestión del carrito de compras.
- `/checkout` - **Checkout**: Proceso de pago y confirmación de pedido.
- `/orders` - **Mis Pedidos**: Historial de compras y seguimiento.
- `/order/<id>` - **Detalle de Pedido**: Información completa del pedido.
- `/order/confirmation/<id>` - **Confirmación**: Confirmación de pedido exitoso.

## 🛡️ Dashboard (Admin y Staff)

Acceso restringido a personal autorizado. Funcionalidades avanzadas de gestión.

### Gestión de Admisiones
- `/admissions/manage` - **Admisiones**: Revisión y procesamiento de solicitudes.
- `/admissions/accept/<id>` - **Aceptar**: Aprueba admisión y crea usuario automáticamente.
- `/admissions/reject/<id>` - **Rechazar**: Rechaza solicitud de admisión.
- `/admissions/add_admin` - **Nueva Admisión**: Crear admisión desde panel admin.
- `/admissions/edit_admin/<id>` - **Editar Admisión**: Modificar datos de admisión.
- `/admissions/delete_admin/<id>` - **Eliminar**: Eliminar solicitud de admisión.

### Gestión de Usuarios
- `/users/manage` - **Usuarios**: Lista y gestión de todas las cuentas.
- `/add_user` - **Nuevo Usuario**: Crear cuenta de padre, staff o admin.
- `/users/edit/<id>` - **Editar Usuario**: Modificar datos y rol de usuario.
- `/users/delete/<id>` - **Eliminar Usuario**: Eliminar cuenta de usuario.

### Gestión de Programas Académicos ⭐ NUEVO
- `/programs/manage` - **Programas**: CRUD completo de programas educativos.
- `/programs/create` - **Crear Programa**: Nuevo nivel o programa educativo.
- `/programs/edit/<id>` - **Editar Programa**: Modificar programa existente.
- `/programs/view/<id>` - **Ver Programa**: Detalle con lista de matriculados.
- `/programs/delete/<id>` - **Eliminar Programa**: Eliminar programa (con validación).
- `/programs/toggle/<id>` - **Activar/Desactivar**: Cambiar estado del programa (AJAX).

### Gestión de Matrículas
- `/enrollments/manage` - **Matrículas**: Control de estudiantes matriculados.
- `/enrollments/view/<id>` - **Ver Matrícula**: Detalle completo con documentos.
- `/enrollments/update_status/<id>` - **Actualizar Estado**: Aprobar/rechazar matrícula.
- `/enrollments/delete/<id>` - **Eliminar**: Eliminar registro de matrícula.

### Gestión de Quejas y Reclamos ⭐ NUEVO
- `/complaints/manage` - **Quejas**: Libro de reclamaciones oficial.
- `/complaints/detail/<id>` - **Detalle**: Ver información completa de la queja.
- `/complaints/update_status/<id>` - **Actualizar**: Cambiar estado (pendiente/en proceso/resuelto).

### Gestión de Productos (Tienda)
- `/products/manage` - **Productos**: Inventario de la tienda virtual.
- `/add_product` - **Nuevo Producto**: Agregar producto con imagen.
- `/products/edit/<id>` - **Editar Producto**: Modificar datos y precio.
- `/products/delete/<id>` - **Eliminar**: Quitar producto del catálogo.

### Gestión de Pedidos
- `/orders/manage` - **Pedidos**: Lista de todas las órdenes de compra.
- `/orders/update_status/<id>` - **Actualizar Estado**: Cambiar estado del pedido (AJAX).

### Gestión de Contenido
- `/news/manage` - **Noticias**: Publicación de comunicados.
- `/news/add` - **Nueva Noticia**: Crear noticia con imagen.
- `/news/edit/<id>` - **Editar Noticia**: Modificar contenido.
- `/news/delete/<id>` - **Eliminar**: Quitar noticia.
- `/galery/manage` - **Galería**: Administración de fotos.
- `/galery/add` - **Subir Foto**: Nueva imagen con categoría.
- `/galery/edit/<id>` - **Editar Foto**: Modificar título y categoría.
- `/galery/delete/<id>` - **Eliminar**: Quitar foto de galería.

### Gestión Académica
- `/courses/manage` - **Cursos**: Gestión de cursos por programa.
- `/courses/add` - **Nuevo Curso**: Crear curso con profesor.
- `/courses/edit/<id>` - **Editar Curso**: Modificar datos del curso.
- `/courses/delete/<id>` - **Eliminar**: Quitar curso.
- `/schedule/manage` - **Horarios**: Programación de clases.

### Archivos y Servicios ⭐ BLOB Storage
- `/serve_image/<table>/<id>` - **Servir Imagen**: Mostrar imágenes desde BD (BLOB).
- `/download/<type>/<id>` - **Descargar Archivo**: Descargar PDFs desde BD (BLOB).

---

## 📊 Estadísticas del Sitio

- **Total de Rutas**: 121
- **Rutas Públicas**: 15
- **Rutas Privadas**: 106
- **APIs REST**: 12
- **Archivos de Plantilla**: 45+
- **Tablas de BD**: 23
