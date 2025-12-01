# --- Importaciones principales ---
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
from utils.file_compression import compress_image, compress_pdf, get_mime_type
from flask import send_file
import io

load_dotenv()
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave segura en producción

# Configuración de subida de archivos
# UPLOAD_FOLDER = 'static/uploads' # Deprecated: Using DB storage
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que existe el directorio de uploads
# os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración de la base de datos
DB_HOST = os.getenv('DB_HOST', 'aws.c506266wsgbx.us-east-1.rds.amazonaws.com')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'diego1416')
DB_NAME = os.getenv('DB_NAME', 'wawalu_db')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM comments")
            result = cursor.fetchone()
        conn.close()
        print("Base de datos conectada y flujo de datos realizada")
    except Exception as e:
        print(f"Conexión con la base de datos error: {e}")


# --- Rutas para servir archivos desde BD ---
@app.route('/serve_image/<table>/<int:id>')
def serve_image(table, id):
    """Serve image from database or fallback to filesystem/default"""
    allowed_tables = ['users', 'products', 'galery_items', 'news', 'students', 'pensions', 'orders']
    
    if table not in allowed_tables:
        return "Invalid table", 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Determine column names based on table
            if table == 'users':
                query = 'SELECT profile_image_data as data, profile_image_type as type, profile_image as legacy_url FROM users WHERE id = %s'
            elif table == 'products':
                query = 'SELECT image_data as data, image_type as type, image_url as legacy_url FROM products WHERE id = %s'
            elif table == 'galery_items':
                query = 'SELECT image_data as data, image_type as type, image_url as legacy_url FROM galery_items WHERE id = %s'
            elif table == 'news':
                query = 'SELECT image_data as data, image_type as type, image_url as legacy_url FROM news WHERE id = %s'
            elif table == 'students':
                query = 'SELECT student_photo_data as data, student_photo_type as type, student_photo as legacy_url FROM students WHERE id = %s'
            elif table == 'pensions':
                query = 'SELECT receipt_data as data, receipt_type as type, receipt_url as legacy_url FROM pensions WHERE id = %s'
            elif table == 'orders':
                query = 'SELECT payment_proof_data as data, payment_proof_type as type, NULL as legacy_url FROM orders WHERE id = %s'
                
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result and result['data']:
                return send_file(
                    io.BytesIO(result['data']),
                    mimetype=result['type'] or 'image/jpeg',
                    as_attachment=False
                )
            elif result and result['legacy_url']:
                # Fallback to legacy filesystem path (now in static/image)
                if table == 'products':
                    return redirect(url_for('static', filename='image/products/' + result['legacy_url']))
                elif table == 'users':
                    return redirect(url_for('static', filename='image/profiles/' + result['legacy_url']))
                elif table == 'galery_items':
                    return redirect(url_for('static', filename='image/galery/' + result['legacy_url']))
                elif table == 'news':
                    return redirect(url_for('static', filename='image/news/' + result['legacy_url']))
                elif table == 'students':
                    return redirect(url_for('static', filename='image/students/' + result['legacy_url']))
            
            # Fallback to default images if not found in DB or legacy
            if table == 'users':
                return redirect(url_for('static', filename='image/default_profile.png'))
            elif table == 'products':
                return redirect(url_for('static', filename='image/default_product.png'))
            elif table == 'galery_items':
                return redirect(url_for('static', filename='image/default_gallery.png'))
            elif table == 'students':
                return redirect(url_for('static', filename='image/default_profile.png'))
            
            return "Image not found", 404
    finally:
        conn.close()

@app.route('/download/<file_type>/<int:id>')
def download_file(file_type, id):
    """Download file from database"""
    allowed_types = ['report', 'document', 'assignment', 'submission', 'receipt']
    
    if file_type not in allowed_types:
        return "Invalid file type", 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if file_type == 'report':
                cursor.execute('SELECT file_data, file_type, title, file_url FROM student_reports WHERE id = %s', (id,))
                result = cursor.fetchone()
                
                if result and result['file_data']:
                    # Use original filename if available, otherwise title
                    filename = result['file_url'] if result['file_url'] else f"{result['title']}.pdf"
                    
                    return send_file(
                        io.BytesIO(result['file_data']),
                        mimetype=result['file_type'] or 'application/pdf',
                        as_attachment=True,
                        download_name=filename
                    )
            elif file_type == 'document':
                cursor.execute('SELECT file_data, file_type, title, file_url FROM student_documents WHERE id = %s', (id,))
                result = cursor.fetchone()
                
                if result and result['file_data']:
                    filename = result['file_url'] if result['file_url'] else f"{result['title']}.pdf"
                    return send_file(
                        io.BytesIO(result['file_data']),
                        mimetype=result['file_type'] or 'application/pdf',
                        as_attachment=True,
                        download_name=filename
                    )
            elif file_type == 'assignment':
                cursor.execute('SELECT file_data, file_type, title, file_url FROM assignments WHERE id = %s', (id,))
                result = cursor.fetchone()
                
                if result and result['file_data']:
                    filename = result['file_url'] if result['file_url'] else f"{result['title']}.pdf"
                    return send_file(
                        io.BytesIO(result['file_data']),
                        mimetype=result['file_type'] or 'application/pdf',
                        as_attachment=True,
                        download_name=filename
                    )
            elif file_type == 'submission':
                cursor.execute('SELECT file_data, file_type, file_url FROM submissions WHERE id = %s', (id,))
                result = cursor.fetchone()
                
                if result and result['file_data']:
                    filename = result['file_url'] if result['file_url'] else f"submission_{id}.pdf"
                    return send_file(
                        io.BytesIO(result['file_data']),
                        mimetype=result['file_type'] or 'application/pdf',
                        as_attachment=True,
                        download_name=filename
                    )
            elif file_type == 'receipt':
                cursor.execute('SELECT receipt_data, receipt_type, receipt_url FROM pensions WHERE id = %s', (id,))
                result = cursor.fetchone()
                
                if result and result['receipt_data']:
                    filename = result['receipt_url'] if result['receipt_url'] else f"receipt_{id}.pdf"
                    return send_file(
                        io.BytesIO(result['receipt_data']),
                        mimetype=result['receipt_type'] or 'application/pdf',
                        as_attachment=True,
                        download_name=filename
                    )
            
            return "File not found", 404
    finally:
        conn.close()

# --- Funciones de Correo ---
def send_credentials_email(to_email, name, password):
    sender_email = os.getenv('SMTP_USER')
    sender_password = os.getenv('SMTP_PASS')
    smtp_server = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Credenciales de Acceso - Wawalu"

    body = f"""
    Hola {name},
    
    Tu cuenta ha sido creada exitosamente.
    
    Usuario: {to_email}
    Contraseña: {password}
    
    Por favor cambia tu contraseña al iniciar sesión.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_acceptance_email(to_email, name, password, child_name):
    sender_email = os.getenv('SMTP_USER')
    sender_password = os.getenv('SMTP_PASS')
    smtp_server = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"¡Felicidades! {child_name} ha sido aceptado/a en Wawalu"

    body = f"""
    Estimado/a {name},

    Nos complace informarle que su solicitud de admisión para {child_name} ha sido ACEPTADA.

    Hemos creado una cuenta para usted en nuestra plataforma para que pueda proceder con la matrícula.

    Credenciales de Acceso:
    ------------------------
    Usuario: {to_email}
    Contraseña: {password}
    ------------------------

    Por favor, inicie sesión en nuestro sitio web y diríjase a la sección "Matrícula" para finalizar el proceso.

    ¡Bienvenidos a la familia Wawalu!

    Atentamente,
    El equipo de Wawalu
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending acceptance email: {e}")
        return False

def send_order_status_email(to_email, name, order_id, status):
    sender_email = os.getenv('SMTP_USER')
    sender_password = os.getenv('SMTP_PASS')
    smtp_server = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"Actualización de Pedido #{order_id} - Wawalu"

    status_messages = {
        'pending': 'está pendiente de procesamiento',
        'paid': 'ha sido confirmado y pagado',
        'shipped': 'ha sido enviado',
        'completed': 'ha sido completado',
        'cancelled': 'ha sido cancelado'
    }

    body = f"""
    Estimado/a {name},

    Le informamos que su pedido #{order_id} {status_messages.get(status, 'ha sido actualizado')}.

    Puede revisar los detalles de su pedido en su panel de usuario.

    Gracias por su compra.

    Atentamente,
    El equipo de Wawalu
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending order status email: {e}")
        return False

# ========================================
# RUTAS PÚBLICAS
# ========================================

# Lista de palabras inapropiadas para filtrar comentarios
BAD_WORDS = [
    'puta', 'puto', 'mierda', 'coño', 'carajo', 'pendejo', 'idiota', 'estúpido',
    'imbécil', 'bastardo', 'cabrón', 'chingar', 'joder', 'cojudo', 'huevón',
    'marica', 'perra', 'zorra', 'verga', 'concha', 'chucha', 'ctm', 'hdp',
    'ptm', 'mrd', 'malparido', 'gonorrea', 'hijueputa', 'chimba'
]

def contains_bad_words(text):
    """Verifica si el texto contiene palabras inapropiadas"""
    if not text:
        return False
    text_lower = text.lower()
    for bad_word in BAD_WORDS:
        if bad_word in text_lower:
            return True
    return False

@app.route('/')
def index():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM comments WHERE is_approved = TRUE ORDER BY created_at DESC LIMIT 6')
            comments = cursor.fetchall()
    finally:
        conn.close()
    return render_template('index.html', comments=comments)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM programs WHERE is_active = TRUE')
            programs = cursor.fetchall()
    finally:
        conn.close()
    return render_template('programs.html', programs=programs)

@app.route('/public/shop')
def public_shop():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT id, name, description, price, image_url, category, stock, 
                       material, usage_info, dimensions, sizes, created_at,
                       (image_data IS NOT NULL) as has_image
                FROM products 
                ORDER BY created_at DESC
            ''')
            products_raw = cursor.fetchall()
            
            # Convert products to JSON-safe format
            products = []
            for product in products_raw:
                product_dict = dict(product)
                # Convert bytes to string if needed
                if 'image_url' in product_dict and isinstance(product_dict['image_url'], bytes):
                    product_dict['image_url'] = product_dict['image_url'].decode('utf-8') if product_dict['image_url'] else None
                products.append(product_dict)
    finally:
        conn.close()
    return render_template('public_shop.html', products=products)

@app.route('/public/galery')
def public_galery():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM galery_items ORDER BY created_at DESC')
            galery_items = cursor.fetchall()
    finally:
        conn.close()
    return render_template('public_galery.html', galery_items=galery_items)

@app.route('/public/news')
def public_news():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT id, title, content, created_at, image_url, 
                (image_data IS NOT NULL) as has_image 
                FROM news 
                ORDER BY created_at DESC
            ''')
            news = cursor.fetchall()
    finally:
        conn.close()
    return render_template('public_news.html', news_items=news)

@app.route('/public/cart')
def public_cart():
    cart_items = session.get('cart', [])
    # Filter out None or invalid items
    cart_items = [item for item in cart_items if isinstance(item, dict)]
    # Calculate total without modifying session objects
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    return render_template('public_cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            product = cursor.fetchone()
            
            if product:
                if 'cart' not in session:
                    session['cart'] = []
                
                # Filter out None items first to avoid errors
                session['cart'] = [item for item in session['cart'] if isinstance(item, dict)]
                
                # Check if item exists
                existing_item = next((item for item in session['cart'] if item['id'] == product_id), None)
                
                if existing_item:
                    existing_item['quantity'] += quantity
                else:
                    # Ensure image_url is a string, not bytes
                    image_url = product['image_url']
                    if isinstance(image_url, bytes):
                        image_url = image_url.decode('utf-8') if image_url else None
                    
                    cart_item = {
                        'id': product['id'],
                        'name': product['name'],
                        'price': float(product['price']),
                        'quantity': quantity,
                        'image_url': image_url,
                        'category': product['category'],
                        'stock': product['stock']
                    }
                    session['cart'].append(cart_item)
                
                session.modified = True
                flash('Producto agregado al carrito', 'success')
            else:
                flash('Producto no encontrado', 'error')
    finally:
        conn.close()
        
    return redirect(request.referrer or url_for('public_shop'))

@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity'))
    if 'cart' in session:
        for item in session['cart']:
            if item['id'] == product_id:
                if quantity > 0:
                    item['quantity'] = quantity
                else:
                    session['cart'].remove(item)
                break
        session.modified = True
    return redirect(url_for('public_cart'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
    return redirect(url_for('public_cart'))

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT id, title, content, created_at, image_url, 
                (image_data IS NOT NULL) as has_image 
                FROM news 
                WHERE id = %s
            ''', (news_id,))
            news_item = cursor.fetchone()
    finally:
        conn.close()
    return render_template('news-detail.html', news=news_item)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)',
                             (name, email, subject, message))
                conn.commit()
                flash('Mensaje enviado exitosamente', 'success')
        except Exception as e:
            flash(f'Error al enviar mensaje: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        parent_name = request.form.get('parent_name')
        parent_lastname = request.form.get('parent_lastname')
        email = request.form.get('email')
        doc_type = request.form.get('parent_doc_type')
        doc_number = request.form.get('parent_doc_number')
        phone = request.form.get('phone')
        parent_dob = request.form.get('parent_dob')
        program = request.form.get('program')
        message = request.form.get('message')
        child_name = request.form.get('child_name')
        child_lastname = request.form.get('child_lastname')
        child_dob = request.form.get('child_dob')
        child_gender = request.form.get('child_gender')
        allergies = request.form.get('allergies')
        medical_observations = request.form.get('medical_observations')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''INSERT INTO admissions 
                    (parent_name, parent_lastname, email, doc_type, doc_number, phone, parent_dob, program, message, 
                     child_name, child_lastname, child_dob, child_gender, allergies, medical_observations, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (parent_name, parent_lastname, email, doc_type, doc_number, phone, parent_dob, program, message,
                     child_name, child_lastname, child_dob, child_gender, allergies, medical_observations, 'pending'))
                conn.commit()
                flash('Solicitud de admisión enviada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al enviar solicitud: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('admission'))
    return render_template('admission.html')

@app.route('/complaints', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        doc_type = request.form.get('doc_type')
        document_number = request.form.get('document_number')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        good_type = request.form.get('good_type')
        amount = request.form.get('amount')
        good_description = request.form.get('good_description')
        claim_type = request.form.get('claim_type')
        claim_detail = request.form.get('claim_detail')
        consumer_request = request.form.get('consumer_request')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''INSERT INTO complaints 
                    (name, lastname, doc_type, document_number, phone, email, address, good_type, amount, 
                     good_description, claim_type, claim_detail, consumer_request)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (name, lastname, doc_type, document_number, phone, email, address, good_type, amount,
                     good_description, claim_type, claim_detail, consumer_request))
                conn.commit()
                flash('Reclamación enviada exitosamente', 'success')
        except Exception as e:
            flash(f'Error al enviar reclamación: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('complaints'))
    return render_template('complaints.html')

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        name = request.form.get('name')
        relation = request.form.get('relation')
        comment = request.form.get('comment')
        
        # Verificar si contiene malas palabras
        has_bad_words = contains_bad_words(name) or contains_bad_words(comment)
        is_approved = not has_bad_words  # Aprobar automáticamente si no hay malas palabras
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO comments (name, relation, comment, is_approved) VALUES (%s, %s, %s, %s)',
                             (name, relation, comment, is_approved))
                conn.commit()
                if is_approved:
                    flash('¡Gracias por tu comentario! Ya está publicado.', 'success')
                else:
                    flash('Tu comentario está en revisión debido a su contenido. Será evaluado por un administrador.', 'warning')
        except Exception as e:
            flash(f'Error al enviar comentario: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('comments'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM comments WHERE is_approved = TRUE ORDER BY created_at DESC')
            comments = cursor.fetchall()
    finally:
        conn.close()
    return render_template('comments.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    """Alias para agregar comentarios desde index.html"""
    name = request.form.get('name')
    relation = request.form.get('relation')
    comment = request.form.get('comment')
    
    # Verificar si contiene malas palabras
    has_bad_words = contains_bad_words(name) or contains_bad_words(comment)
    is_approved = not has_bad_words  # Aprobar automáticamente si no hay malas palabras
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO comments (name, relation, comment, is_approved) VALUES (%s, %s, %s, %s)',
                         (name, relation, comment, is_approved))
            conn.commit()
            if is_approved:
                flash('¡Gracias por tu comentario! Ya está publicado.', 'success')
            else:
                flash('Tu comentario está en revisión debido a su contenido. Será evaluado por un administrador.', 'warning')
    except Exception as e:
        flash(f'Error al enviar comentario: {str(e)}', 'error')
    finally:
        conn.close()
    next_url = request.form.get('next')
    return redirect(next_url or url_for('index'))

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

# ========================================
# AUTENTICACIÓN
# ========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        next_url = request.form.get('next')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()
                
                if not user:
                    flash('No existe usuario con ese email', 'error')
                elif not check_password_hash(user['password'], password):
                    flash('Contraseña incorrecta', 'error')
                else:
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['user_email'] = user['email']
                    session['user_role'] = user['role']
                    # Check if user has a profile image (either path or BLOB)
                    session['profile_image'] = True if (user.get('profile_image') or user.get('profile_image_data')) else None
                    
                    cursor.execute('UPDATE users SET last_login = NOW() WHERE id = %s', (user['id'],))
                    conn.commit()
                    
                    flash('Inicio de sesión exitoso', 'success')
                    if next_url:
                        return redirect(next_url)
                    return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
        finally:
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

# ========================================
# DASHBOARD PRINCIPAL
# ========================================

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_role = session.get('user_role')
    
    if user_role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif user_role == 'staff':
        return redirect(url_for('staff_dashboard'))
    else:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
                students = cursor.fetchall()
                
                cursor.execute('SELECT * FROM student_reports WHERE user_id = %s ORDER BY created_at DESC LIMIT 5', 
                             (session['user_id'],))
                recent_reports = cursor.fetchall()
        finally:
            conn.close()
        return render_template('dashboard/index.html', students=students, recent_reports=recent_reports)

@app.route('/dashboard/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM students')
            total_students = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM admissions WHERE status = "pending"')
            pending_admissions = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM orders')
            total_orders = cursor.fetchone()['count']
    finally:
        conn.close()
    
    return render_template('dashboard/admin/index.html', 
                         total_users=total_users,
                         total_students=total_students,
                         pending_admissions=pending_admissions,
                         total_orders=total_orders)

@app.route('/dashboard/staff')
def staff_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'staff':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']

            cursor.execute('SELECT COUNT(*) as count FROM students')
            total_students = cursor.fetchone()['count']
            
            cursor.execute('SELECT COUNT(*) as count FROM admissions WHERE status = "pending"')
            pending_admissions = cursor.fetchone()['count']

            cursor.execute('SELECT COUNT(*) as count FROM orders')
            total_orders = cursor.fetchone()['count']
    finally:
        conn.close()
    
    return render_template('dashboard/staff/index.html',
                         total_users=total_users,
                         total_students=total_students,
                         pending_admissions=pending_admissions,
                         total_orders=total_orders)

@app.route('/dashboard/guide')
def dashboard_guide():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard/guide.html')

# ========================================
# PERFIL DE USUARIO
# ========================================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                name = request.form.get('name')
                phone = request.form.get('phone')
                address = request.form.get('address')
                
                # Manejo de imagen de perfil
                if 'profile_image' in request.files:
                    file = request.files['profile_image']
                    if file and file.filename != '':
                        if allowed_file(file.filename):
                            try:
                                # Comprimir imagen
                                compressed_data, mime_type = compress_image(file, max_width=400, max_height=400, quality=80)
                                
                                # Actualizar base de datos con la imagen BLOB
                                cursor.execute('UPDATE users SET name = %s, phone = %s, address = %s, profile_image_data = %s, profile_image_type = %s WHERE id = %s',
                                             (name, phone, address, compressed_data, mime_type, session['user_id']))
                                
                                # Update session to reflect new image
                                session['profile_image'] = True
                                flash('Perfil e imagen actualizados exitosamente', 'success')
                            except Exception as e:
                                flash(f'Error al subir la imagen: {str(e)}', 'error')
                                # Actualizar sin imagen si hay error
                                cursor.execute('UPDATE users SET name = %s, phone = %s, address = %s WHERE id = %s',
                                             (name, phone, address, session['user_id']))
                        else:
                            flash('Formato de imagen no permitido. Use PNG, JPG, JPEG o GIF', 'warning')
                            cursor.execute('UPDATE users SET name = %s, phone = %s, address = %s WHERE id = %s',
                                         (name, phone, address, session['user_id']))
                    else:
                        # No se seleccionó archivo, solo actualizar otros campos
                        cursor.execute('UPDATE users SET name = %s, phone = %s, address = %s WHERE id = %s',
                                     (name, phone, address, session['user_id']))
                else:
                    # No hay campo de imagen en el formulario
                    cursor.execute('UPDATE users SET name = %s, phone = %s, address = %s WHERE id = %s',
                                 (name, phone, address, session['user_id']))
                
                conn.commit()
                session['user_name'] = name
                if 'Perfil e imagen actualizados' not in [msg[1] for msg in session.get('_flashes', [])]:
                    flash('Perfil actualizado exitosamente', 'success')
                return redirect(url_for('profile'))
            
            cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
            user = cursor.fetchone()
    except Exception as e:
        flash(f'Error al actualizar perfil: {str(e)}', 'error')
    finally:
        conn.close()
    
    return render_template('dashboard/profile.html', user=user)



# ========================================
# MATRÍCULA Y MATRÍCULAS
# ========================================

@app.route('/enrollments', methods=['GET', 'POST'])
def enrollments():
    if request.method == 'POST':
        # Formulario público de matrícula
        student_name = request.form.get('student_name')
        student_lastname = request.form.get('student_lastname')
        parent_name = request.form.get('parent_name')
        parent_email = request.form.get('parent_email')
        parent_phone = request.form.get('parent_phone')
        program_id = request.form.get('program_id')
        
        flash('Solicitud de matrícula enviada. Nos contactaremos pronto.', 'success')
        return redirect(url_for('enrollments'))
    
    # Mostrar formulario con programas disponibles
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM programs WHERE is_active = TRUE')
            programs = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('enrollments.html', programs=programs)

@app.route('/matricula', methods=['GET', 'POST'])
def matricula():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                # Procesar formulario de matrícula
                student_first_name = request.form.get('student_first_name')
                student_last_name = request.form.get('student_last_name')
                student_dob = request.form.get('student_dob')
                student_gender = request.form.get('student_gender')
                allergies = request.form.get('allergies')
                medical_info = request.form.get('medical_info')
                program_id = request.form.get('program_id')
                enrollment_year = request.form.get('enrollment_year')
                enrollment_period = request.form.get('enrollment_period')
                observations = request.form.get('observations')
                
                # Procesar archivos subidos
                parent_id_front_file = None
                parent_id_front_data = None
                parent_id_front_type = None
                parent_id_back_file = None
                parent_id_back_data = None
                parent_id_back_type = None
                birth_certificate_file = None
                birth_certificate_data = None
                birth_certificate_type = None
                student_photo_file = None
                student_photo_data = None
                student_photo_type = None
                
                try:
                    # DNI Frontal
                    if 'parent_id_front' in request.files:
                        file = request.files['parent_id_front']
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(f"dni_front_{session['user_id']}_{int(time.time())}_{file.filename}")
                            parent_id_front_data, parent_id_front_type = compress_pdf(file)
                            parent_id_front_file = filename
                    
                    # DNI Reverso
                    if 'parent_id_back' in request.files:
                        file = request.files['parent_id_back']
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(f"dni_back_{session['user_id']}_{int(time.time())}_{file.filename}")
                            parent_id_back_data, parent_id_back_type = compress_pdf(file)
                            parent_id_back_file = filename
                    
                    # Certificado de Nacimiento
                    if 'birth_certificate' in request.files:
                        file = request.files['birth_certificate']
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(f"birth_cert_{session['user_id']}_{int(time.time())}_{file.filename}")
                            birth_certificate_data, birth_certificate_type = compress_pdf(file)
                            birth_certificate_file = filename
                    
                    # Foto del Estudiante
                    if 'student_photo' in request.files:
                        file = request.files['student_photo']
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(f"student_photo_{session['user_id']}_{int(time.time())}_{file.filename}")
                            # Compress and get data
                            student_photo_data, student_photo_type = compress_image(file, max_width=400, max_height=400, quality=80)
                            student_photo_file = filename
                    
                    # Verificar que todos los archivos fueron subidos
                    if not all([parent_id_front_file, parent_id_back_file, birth_certificate_file, student_photo_file]):
                        flash('Todos los documentos son obligatorios', 'error')
                        return redirect(url_for('matricula'))
                    
                except Exception as e:
                    flash(f'Error al subir archivos: {str(e)}', 'error')
                    return redirect(url_for('matricula'))
                
                # Crear estudiante con documentos
                cursor.execute('''INSERT INTO students 
                    (parent_id, first_name, last_name, dob, gender, allergies, medical_info,
                     parent_id_front, parent_id_front_data, parent_id_front_type,
                     parent_id_back, parent_id_back_data, parent_id_back_type,
                     birth_certificate, birth_certificate_data, birth_certificate_type,
                     student_photo, student_photo_data, student_photo_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (session['user_id'], student_first_name, student_last_name, 
                     student_dob, student_gender, allergies, medical_info,
                     parent_id_front_file, parent_id_front_data, parent_id_front_type,
                     parent_id_back_file, parent_id_back_data, parent_id_back_type,
                     birth_certificate_file, birth_certificate_data, birth_certificate_type,
                     student_photo_file, student_photo_data, student_photo_type))
                
                student_id = cursor.lastrowid
                
                # Crear matrícula
                cursor.execute('''INSERT INTO enrollments 
                    (student_id, program_id, enrollment_year, enrollment_period, status, observations)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (student_id, program_id, enrollment_year, enrollment_period, 'pending', observations))
                
                conn.commit()
                flash('Matrícula enviada exitosamente. Será revisada por el personal administrativo.', 'success')
                return redirect(url_for('matricula'))
            
            # Obtener programas disponibles
            cursor.execute('SELECT * FROM programs WHERE is_active = TRUE')
            programs = cursor.fetchall()
            
            # Obtener historial de matrículas del usuario
            cursor.execute('''
                SELECT e.*, s.first_name, s.last_name, p.name as program_name,
                       CONCAT(s.first_name, ' ', s.last_name) as student_name
                FROM enrollments e
                JOIN students s ON e.student_id = s.id
                JOIN programs p ON e.program_id = p.id
                WHERE s.parent_id = %s
                ORDER BY e.created_at DESC
            ''', (session['user_id'],))
            enrollments = cursor.fetchall()
            
    finally:
        conn.close()
    
    return render_template('dashboard/matricula.html', programs=programs, enrollments=enrollments)

# ========================================
# REPORTES
# ========================================

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM student_reports WHERE user_id = %s ORDER BY created_at DESC',
                         (session['user_id'],))
            reports = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/reports.html', reports=reports)

# ========================================
# CALENDARIO
# ========================================

@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM events ORDER BY start_date ASC')
            events = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/calendar.html', events=events)

# ========================================
# MENÚ DE ALIMENTOS
# ========================================

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM menu_items')
            menu_items = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/menu.html', menu_items=menu_items)

# ========================================
# GESTIÓN ACADÉMICA (ESTUDIANTE/PADRE)
# ========================================

@app.route('/dashboard/grades')
def student_grades():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Obtener estudiantes asociados al padre
            cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
            students = cursor.fetchall()
            
            # Por defecto mostrar el primer estudiante o el seleccionado
            student_id = request.args.get('student_id')
            if not student_id and students:
                student_id = students[0]['id']
            
            grades = []
            if student_id:
                cursor.execute('''
                    SELECT g.*, c.name as course_name, p.name as program_name
                    FROM grades g
                    JOIN enrollments e ON g.enrollment_id = e.id
                    JOIN courses c ON g.course_id = c.id
                    JOIN programs p ON c.program_id = p.id
                    WHERE e.student_id = %s
                    ORDER BY g.period, c.name
                ''', (student_id,))
                grades = cursor.fetchall()
                
    finally:
        conn.close()
    
    return render_template('dashboard/grades.html', students=students, grades=grades, current_student_id=int(student_id) if student_id else None)

@app.route('/dashboard/attendance')
def student_attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
            students = cursor.fetchall()
            
            student_id = request.args.get('student_id')
            if not student_id and students:
                student_id = students[0]['id']
            
            attendance = []
            stats = {'present': 0, 'absent': 0, 'late': 0, 'excused': 0}
            
            if student_id:
                cursor.execute('''
                    SELECT a.*, c.name as course_name
                    FROM attendance a
                    JOIN enrollments e ON a.enrollment_id = e.id
                    LEFT JOIN courses c ON e.program_id = c.program_id -- Simplificación, idealmente asistencia es por curso
                    WHERE e.student_id = %s
                    ORDER BY a.date DESC
                ''', (student_id,))
                attendance = cursor.fetchall()
                
                for record in attendance:
                    if record['status'] in stats:
                        stats[record['status']] += 1
                        
    finally:
        conn.close()
    
    return render_template('dashboard/attendance.html', students=students, attendance=attendance, stats=stats, current_student_id=int(student_id) if student_id else None)

@app.route('/dashboard/schedule')
def student_schedule():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
            students = cursor.fetchall()
            
            student_id = request.args.get('student_id')
            if not student_id and students:
                student_id = students[0]['id']
            
            schedule = {}
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            
            if student_id:
                cursor.execute('''
                    SELECT s.*, c.name as course_name, c.teacher_name
                    FROM class_schedule s
                    JOIN courses c ON s.course_id = c.id
                    JOIN enrollments e ON c.program_id = e.program_id
                    WHERE e.student_id = %s
                    ORDER BY s.start_time
                ''', (student_id,))
                rows = cursor.fetchall()
                
                for row in rows:
                    day = row['day_of_week']
                    if day not in schedule:
                        schedule[day] = []
                    schedule[day].append(row)
                        
    finally:
        conn.close()
    
    return render_template('dashboard/schedule.html', students=students, schedule=schedule, days=days, current_student_id=int(student_id) if student_id else None)

    return render_template('dashboard/schedule.html', students=students, schedule=schedule, days=days, current_student_id=int(student_id) if student_id else None)

# ========================================
# GESTIÓN ADMINISTRATIVA (ESTUDIANTE/PADRE)
# ========================================

@app.route('/dashboard/payments')
def student_payments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
            students = cursor.fetchall()
            
            student_id = request.args.get('student_id')
            if not student_id and students:
                student_id = students[0]['id']
            
            pensions = []
            if student_id:
                cursor.execute('''
                    SELECT p.*, e.enrollment_year, pr.name as program_name
                    FROM pensions p
                    JOIN enrollments e ON p.enrollment_id = e.id
                    JOIN programs pr ON e.program_id = pr.id
                    WHERE e.student_id = %s
                    ORDER BY p.due_date DESC
                ''', (student_id,))
                pensions = cursor.fetchall()
                
    finally:
        conn.close()
    
    return render_template('dashboard/payments.html', students=students, pensions=pensions, current_student_id=int(student_id) if student_id else None)

@app.route('/dashboard/documents')
def student_documents():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE parent_id = %s', (session['user_id'],))
            students = cursor.fetchall()
            
            student_id = request.args.get('student_id')
            if not student_id and students:
                student_id = students[0]['id']
            
            documents = []
            if student_id:
                cursor.execute('''
                    SELECT * FROM student_documents
                    WHERE student_id = %s
                    ORDER BY upload_date DESC
                ''', (student_id,))
                documents = cursor.fetchall()
                
    finally:
        conn.close()
    
    return render_template('dashboard/documents.html', students=students, documents=documents, current_student_id=int(student_id) if student_id else None)

# ========================================
# GALERÍA (DASHBOARD)
# ========================================

@app.route('/galery')
def galery():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM galery_items ORDER BY created_at DESC')
            galery_items = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/galery.html', galery_items=galery_items)

# ========================================
# TIENDA (DASHBOARD)
# ========================================

@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            products_raw = cursor.fetchall()
            
            # Convert products to JSON-safe format
            products = []
            for product in products_raw:
                product_dict = dict(product)
                # Remove binary fields that can't be JSON serialized
                if 'image_data' in product_dict:
                    del product_dict['image_data']
                # Convert bytes to string if needed
                if 'image_url' in product_dict and isinstance(product_dict['image_url'], bytes):
                    product_dict['image_url'] = product_dict['image_url'].decode('utf-8') if product_dict['image_url'] else None
                products.append(product_dict)
    finally:
        conn.close()
    
    return render_template('dashboard/shop.html', products=products)

# ========================================
# NOTICIAS (DASHBOARD)
# ========================================

@app.route('/news')
def news():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
            news = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/news.html', news=news)

# ========================================
# CARRITO Y CHECKOUT
# ========================================

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = session.get('cart', [])
    # Filter out None or invalid items
    cart_items = [item for item in cart_items if isinstance(item, dict)]
    
    # Calculate total
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    
    # Calculate subtotals for display if needed (though template might do it)
    for item in cart_items:
        if isinstance(item, dict):
            item['subtotal'] = item.get('price', 0) * item.get('quantity', 0)
            
    return render_template('dashboard/cart.html', cart_items=cart_items, total=total)

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def api_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    if 'cart' not in session:
        session['cart'] = []
    
    if request.method == 'GET':
        return jsonify(session['cart'])
    
    elif request.method == 'POST':
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
                product = cursor.fetchone()
                
                if product:
                    # Ensure image_url is a string, not bytes
                    image_url = product['image_url']
                    if isinstance(image_url, bytes):
                        image_url = image_url.decode('utf-8') if image_url else None
                    
                    cart_item = {
                        'id': product['id'],
                        'name': product['name'],
                        'price': float(product['price']),
                        'quantity': quantity,
                        'image_url': image_url
                    }
                    
                    existing_item = next((item for item in session['cart'] if item['id'] == product_id), None)
                    if existing_item:
                        existing_item['quantity'] += quantity
                    else:
                        session['cart'].append(cart_item)
                    
                    session.modified = True
                    return jsonify({'success': True, 'cart': session['cart']})
        finally:
            conn.close()
        
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    elif request.method == 'DELETE':
        data = request.get_json()
        product_id = data.get('product_id')
        
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
        return jsonify({'success': True, 'cart': session['cart']})

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    
    if 'cart' not in session or len(session['cart']) == 0:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('shop'))
        
    # Filter out None items
    session['cart'] = [item for item in session['cart'] if isinstance(item, dict)]
    session.modified = True
    
    if request.method == 'POST':
        shipping_name = request.form.get('shipping_name')
        shipping_lastname = request.form.get('shipping_lastname')
        shipping_email = request.form.get('shipping_email')
        shipping_phone = request.form.get('shipping_phone')
        shipping_address = request.form.get('shipping_address')
        payment_method = request.form.get('payment_method')
        
        total_amount = sum(item['price'] * item['quantity'] for item in session['cart'])
        
        payment_proof_data = None
        payment_proof_type = None
        
        if 'payment_proof' in request.files:
            file = request.files['payment_proof']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                
                if file_ext == 'pdf':
                    payment_proof_data, payment_proof_type = compress_pdf(file)
                else:
                    payment_proof_data, payment_proof_type = compress_image(file, max_width=1200, max_height=1200, quality=85)

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''INSERT INTO orders 
                    (user_id, total_amount, status, payment_method, shipping_address, shipping_phone, 
                     shipping_name, shipping_lastname, shipping_email, payment_proof_data, payment_proof_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (session['user_id'], total_amount, 'pending', payment_method, shipping_address,
                     shipping_phone, shipping_name, shipping_lastname, shipping_email, payment_proof_data, payment_proof_type))
                
                order_id = cursor.lastrowid
                
                for item in session['cart']:
                    cursor.execute('''INSERT INTO order_items 
                        (order_id, product_id, quantity, price_at_purchase, subtotal)
                        VALUES (%s, %s, %s, %s, %s)''',
                        (order_id, item['id'], item['quantity'], item['price'], 
                         item['price'] * item['quantity']))
                
                conn.commit()
                session.pop('cart', None)
                flash('Pedido realizado exitosamente', 'success')
                return redirect(url_for('order_confirmation', order_id=order_id))
        except Exception as e:
            flash(f'Error al procesar pedido: {str(e)}', 'error')
        finally:
            conn.close()
    
    user_name = session.get('user_name', '')
    user_first_name = user_name.split()[0] if user_name else ''
    
    cart_items = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 0) for item in cart_items)
    
    return render_template('dashboard/checkout.html', cart=cart_items, user_first_name=user_first_name, total=total)

@app.route('/order/confirmation/<int:order_id>')
def order_confirmation(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM orders WHERE id = %s AND user_id = %s', 
                         (order_id, session['user_id']))
            order = cursor.fetchone()
            
            if not order:
                flash('Pedido no encontrado', 'error')
                return redirect(url_for('shop'))
            
            cursor.execute('''SELECT oi.*, p.name, p.image_url 
                            FROM order_items oi 
                            JOIN products p ON oi.product_id = p.id 
                            WHERE oi.order_id = %s''', (order_id,))
            order_items = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/order_confirmation.html', order=order, order_items=order_items)

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC', 
                         (session['user_id'],))
            orders = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:order_id>')
def order_detail(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if session.get('user_role') in ['admin', 'staff']:
                cursor.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
            else:
                cursor.execute('SELECT * FROM orders WHERE id = %s AND user_id = %s', 
                             (order_id, session['user_id']))
            
            order = cursor.fetchone()
            
            if not order:
                flash('Pedido no encontrado', 'error')
                return redirect(url_for('orders'))
            
            cursor.execute('''SELECT oi.*, p.name, p.image_url 
                            FROM order_items oi 
                            JOIN products p ON oi.product_id = p.id 
                            WHERE oi.order_id = %s''', (order_id,))
            order_items = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('order_detail.html', order=order, order_items=order_items)

# ========================================
# GESTIÓN DE ADMISIONES (ADMIN/STAFF)
# ========================================

@app.route('/admissions/manage')
def manage_admissions():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM admissions ORDER BY created_at DESC')
            admissions = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_admissions.html', admissions=admissions)
    else:
        return render_template('dashboard/staff/manage_admissions.html', admissions=admissions)

@app.route('/admissions/accept/<int:admission_id>')
def accept_admission(admission_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM admissions WHERE id = %s', (admission_id,))
            admission = cursor.fetchone()
            
            if not admission:
                flash('Admisión no encontrada', 'error')
                return redirect(url_for('manage_admissions'))
            
            # Verificar si ya existe un usuario con ese email
            cursor.execute('SELECT id FROM users WHERE email = %s', (admission['email'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                user_id = existing_user['id']
                flash(f'Usuario ya existía con ID: {user_id}', 'info')
            else:
                # Crear nuevo usuario
                hashed_password = generate_password_hash(admission['doc_number'])
                cursor.execute('''INSERT INTO users (name, email, password, role, phone) 
                                VALUES (%s, %s, %s, %s, %s)''',
                             (f"{admission['parent_name']} {admission['parent_lastname']}", 
                              admission['email'], hashed_password, 'padre', admission['phone']))
                user_id = cursor.lastrowid
                
                flash(f'Usuario creado con ID: {user_id}, Email: {admission["email"]}, Contraseña: {admission["doc_number"]}', 'info')
                
                # Enviar email con credenciales
                try:
                    send_acceptance_email(
                        admission['email'],
                        admission['parent_name'],
                        admission['doc_number'],
                        f"{admission['child_name']} {admission['child_lastname']}"
                    )
                    flash('Email enviado exitosamente', 'success')
                except Exception as email_error:
                    flash(f'Usuario creado pero error al enviar email: {str(email_error)}', 'warning')
            
            # Crear registro de estudiante
            cursor.execute('''INSERT INTO students 
                (parent_id, first_name, last_name, dob, gender, medical_info, allergies)
                VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (user_id, admission['child_name'], admission['child_lastname'], 
                 admission['child_dob'], admission['child_gender'], 
                 admission['medical_observations'], admission['allergies']))
            
            # Actualizar estado de admisión
            cursor.execute('UPDATE admissions SET status = %s, user_id = %s WHERE id = %s',
                         ('accepted', user_id, admission_id))
            
            conn.commit()
            flash('Admisión aceptada exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al aceptar admisión: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_admissions'))

@app.route('/admissions/reject/<int:admission_id>')
def reject_admission(admission_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE admissions SET status = %s WHERE id = %s', ('rejected', admission_id))
            conn.commit()
            flash('Admisión rechazada', 'success')
    except Exception as e:
        flash(f'Error al rechazar admisión: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_admissions'))

@app.route('/admissions/add_admin', methods=['GET', 'POST'])
def add_admission_admin():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Parent Info
        parent_name = request.form.get('parent_name')
        parent_lastname = request.form.get('parent_lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        doc_type = request.form.get('doc_type')
        doc_number = request.form.get('doc_number')
        
        # Child Info
        child_name = request.form.get('child_name')
        child_lastname = request.form.get('child_lastname')
        child_dob = request.form.get('child_dob')
        child_gender = request.form.get('child_gender')
        
        # Academic Info
        program = request.form.get('program')
        status = request.form.get('status', 'pending')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO admissions (
                        parent_name, parent_lastname, email, phone, doc_type, doc_number,
                        child_name, child_lastname, child_dob, child_gender,
                        program, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (parent_name, parent_lastname, email, phone, doc_type, doc_number,
                      child_name, child_lastname, child_dob, child_gender,
                      program, status))
                conn.commit()
                flash('Admisión creada exitosamente', 'success')
                return redirect(url_for('manage_admissions'))
        except Exception as e:
            flash(f'Error al crear admisión: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/admission_form.html', admission=None)

@app.route('/admissions/edit_admin/<int:admission_id>', methods=['GET', 'POST'])
def edit_admission_admin(admission_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                # Parent Info
                parent_name = request.form.get('parent_name')
                parent_lastname = request.form.get('parent_lastname')
                email = request.form.get('email')
                phone = request.form.get('phone')
                doc_type = request.form.get('doc_type')
                doc_number = request.form.get('doc_number')
                
                # Child Info
                child_name = request.form.get('child_name')
                child_lastname = request.form.get('child_lastname')
                child_dob = request.form.get('child_dob')
                child_gender = request.form.get('child_gender')
                
                # Academic Info
                program = request.form.get('program')
                status = request.form.get('status')
                
                cursor.execute('''
                    UPDATE admissions SET
                        parent_name=%s, parent_lastname=%s, email=%s, phone=%s, doc_type=%s, doc_number=%s,
                        child_name=%s, child_lastname=%s, child_dob=%s, child_gender=%s,
                        program=%s, status=%s
                    WHERE id=%s
                ''', (parent_name, parent_lastname, email, phone, doc_type, doc_number,
                      child_name, child_lastname, child_dob, child_gender,
                      program, status, admission_id))
                conn.commit()
                flash('Admisión actualizada exitosamente', 'success')
                return redirect(url_for('manage_admissions'))
            
            cursor.execute('SELECT * FROM admissions WHERE id = %s', (admission_id,))
            admission = cursor.fetchone()
            if not admission:
                flash('Admisión no encontrada', 'error')
                return redirect(url_for('manage_admissions'))
                
            return render_template('dashboard/admin/admission_form.html', admission=admission)
    finally:
        conn.close()

@app.route('/admissions/delete_admin/<int:admission_id>')
def delete_admission_admin(admission_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM admissions WHERE id = %s', (admission_id,))
            conn.commit()
            flash('Admisión eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar admisión: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_admissions'))

# ========================================
# GESTIÓN DE USUARIOS (ADMIN/STAFF)
# ========================================

@app.route('/users/manage')
def manage_users():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if session.get('user_role') == 'admin':
                cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            else:
                cursor.execute("SELECT * FROM users WHERE role != 'admin' ORDER BY created_at DESC")
            users = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_users.html', users=users)
    else:
        return render_template('dashboard/staff/manage_users.html', users=users)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                name = request.form.get('name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                role = request.form.get('role')
                password = request.form.get('password')
                
                # Check if email exists for other users
                cursor.execute('SELECT id FROM users WHERE email = %s AND id != %s', (email, user_id))
                if cursor.fetchone():
                    flash('El correo electrónico ya está en uso por otro usuario', 'error')
                    return redirect(url_for('edit_user', user_id=user_id))
                
                if password:
                    hashed_password = generate_password_hash(password)
                    cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s, role = %s, password = %s WHERE id = %s',
                                 (name, email, phone, role, hashed_password, user_id))
                else:
                    cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s, role = %s WHERE id = %s',
                                 (name, email, phone, role, user_id))
                
                conn.commit()
                flash('Usuario actualizado exitosamente', 'success')
                return redirect(url_for('manage_users'))
            
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                flash('Usuario no encontrado', 'error')
                return redirect(url_for('manage_users'))
                
            return render_template('dashboard/admin/user_form.html', user=user)
    finally:
        conn.close()

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
            conn.commit()
            flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar usuario: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_users'))



# ========================================
# GESTIÓN DE PEDIDOS (ADMIN/STAFF)
# ========================================

@app.route('/orders/manage')
def manage_orders():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT o.*, u.name as user_name, u.email as user_email 
                            FROM orders o
                            JOIN users u ON o.user_id = u.id
                            ORDER BY o.created_at DESC''')
            orders = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_orders.html', orders=orders)
    else:
        return render_template('dashboard/staff/manage_orders.html', orders=orders)

@app.route('/orders/update_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'success': False, 'message': 'Status required'}), 400
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get order details for email
            cursor.execute('SELECT o.*, u.email, u.name FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = %s', (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return jsonify({'success': False, 'message': 'Order not found'}), 404
            
            # Update status
            cursor.execute('UPDATE orders SET status = %s WHERE id = %s', (new_status, order_id))
            conn.commit()
            
            # Send email notification
            try:
                send_order_status_email(order['email'], order['name'], order_id, new_status)
            except Exception as e:
                print(f"Error sending email: {e}")
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
    
    return jsonify({'success': True})

# ========================================
# GESTIÓN DE PRODUCTOS (ADMIN/STAFF)
# ========================================

@app.route('/products/manage')
def manage_products():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            products_raw = cursor.fetchall()
            
            # Convert products to JSON-safe format
            products = []
            for product in products_raw:
                product_dict = dict(product)
                # Remove binary fields that can't be JSON serialized
                if 'image_data' in product_dict:
                    del product_dict['image_data']
                # Convert bytes to string if needed
                if 'image_url' in product_dict and isinstance(product_dict['image_url'], bytes):
                    product_dict['image_url'] = product_dict['image_url'].decode('utf-8') if product_dict['image_url'] else None
                products.append(product_dict)
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_products.html', products=products)
    else:
        return render_template('dashboard/staff/manage_products.html', products=products)

# ========================================
# GESTIÓN DE GALERÍA (ADMIN/STAFF)
# ========================================

@app.route('/galery/manage')
def manage_galery():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM galery_items ORDER BY created_at DESC')
            galery_items = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_galery.html', galery_items=galery_items)
    else:
        return render_template('dashboard/staff/manage_galery.html', galery_items=galery_items)

@app.route('/galery/add', methods=['GET', 'POST'])
def add_gallery_item():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        file = request.files.get('image')
        
        if file and file.filename:
            # Compress and save image
            image_data, image_type = compress_image(file)
            
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO galery_items (title, category, description, image_data, image_type) VALUES (%s, %s, %s, %s, %s)',
                                 (title, category, description, image_data, image_type))
                    conn.commit()
                    flash('Foto agregada exitosamente', 'success')
                    return redirect(url_for('manage_galery'))
            except Exception as e:
                flash(f'Error al agregar foto: {str(e)}', 'error')
            finally:
                conn.close()
        else:
            flash('Debe seleccionar una imagen', 'error')
            
    return render_template('dashboard/admin/gallery_form.html', item=None)

@app.route('/galery/upload', methods=['POST'])
def upload_galery():
    """Alias for quick upload from gallery page"""
    return add_gallery_item()

@app.route('/galery/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_galery_item(item_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                title = request.form.get('title')
                category = request.form.get('category')
                description = request.form.get('description')
                file = request.files.get('image')
                
                if file and file.filename:
                    image_data, image_type = compress_image(file)
                    cursor.execute('UPDATE galery_items SET title=%s, category=%s, description=%s, image_data=%s, image_type=%s WHERE id=%s',
                                 (title, category, description, image_data, image_type, item_id))
                else:
                    cursor.execute('UPDATE galery_items SET title=%s, category=%s, description=%s WHERE id=%s',
                                 (title, category, description, item_id))
                                 
                conn.commit()
                flash('Foto actualizada exitosamente', 'success')
                return redirect(url_for('manage_galery'))
            
            cursor.execute('SELECT * FROM galery_items WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            
            if not item:
                flash('Foto no encontrada', 'error')
                return redirect(url_for('manage_galery'))
                
            return render_template('dashboard/admin/gallery_form.html', item=item)
    finally:
        conn.close()

@app.route('/galery/delete/<int:item_id>')
def delete_gallery_item(item_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM galery_items WHERE id = %s', (item_id,))
            conn.commit()
            flash('Foto eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar foto: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(request.referrer or url_for('manage_galery'))

# ========================================
# GESTIÓN DE NOTICIAS (ADMIN/STAFF)
# ========================================

@app.route('/news/manage')
def manage_news():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
            news = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_news.html', news=news)
    else:
        return render_template('dashboard/staff/manage_news.html', news=news)

@app.route('/news/add', methods=['GET', 'POST'])
def add_news():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('image')
        
        print(f"DEBUG: add_news request.files keys: {request.files.keys()}")
        print(f"DEBUG: add_news file object: {file}")
        if file:
            print(f"DEBUG: add_news filename: {file.filename}")
        
        image_data = None
        image_type = None
        
        if file and file.filename:
            image_data, image_type = compress_image(file)
            
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO news (title, content, image_data, image_type) VALUES (%s, %s, %s, %s)',
                             (title, content, image_data, image_type))
                conn.commit()
                flash('Noticia agregada exitosamente', 'success')
                return redirect(url_for('manage_news'))
        except Exception as e:
            flash(f'Error al agregar noticia: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/news_form.html', news=None)

@app.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
def edit_news(news_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                title = request.form.get('title')
                content = request.form.get('content')
                file = request.files.get('image')
                
                if file and file.filename:
                    image_data, image_type = compress_image(file)
                    cursor.execute('UPDATE news SET title=%s, content=%s, image_data=%s, image_type=%s WHERE id=%s',
                                 (title, content, image_data, image_type, news_id))
                else:
                    cursor.execute('UPDATE news SET title=%s, content=%s WHERE id=%s',
                                 (title, content, news_id))
                                 
                conn.commit()
                flash('Noticia actualizada exitosamente', 'success')
                return redirect(url_for('manage_news'))
            
            cursor.execute('SELECT * FROM news WHERE id = %s', (news_id,))
            news_item = cursor.fetchone()
            
            if not news_item:
                flash('Noticia no encontrada', 'error')
                return redirect(url_for('manage_news'))
                
            return render_template('dashboard/admin/news_form.html', news=news_item)
    finally:
        conn.close()

@app.route('/news/delete/<int:news_id>')
def delete_news(news_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM news WHERE id = %s', (news_id,))
            conn.commit()
            flash('Noticia eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar noticia: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(request.referrer or url_for('manage_news'))

# ========================================
# GESTIÓN DE MATRÍCULAS (ADMIN/STAFF)
# ========================================

@app.route('/enrollments/manage')
def manage_enrollments():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT e.*, s.first_name, s.last_name, p.name as program_name
                            FROM enrollments e
                            JOIN students s ON e.student_id = s.id
                            JOIN programs p ON e.program_id = p.id
                            ORDER BY e.created_at DESC''')
            enrollments = cursor.fetchall()
    finally:
        conn.close()
    
    if session.get('user_role') == 'admin':
        return render_template('dashboard/admin/manage_enrollments.html', enrollments=enrollments)
    else:
        return render_template('dashboard/staff/manage_enrollments.html', enrollments=enrollments)

@app.route('/enrollments/update_status/<int:id>', methods=['POST'])
def update_enrollment_status(id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'success': False, 'message': 'Status required'}), 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE enrollments SET status = %s WHERE id = %s', (new_status, id))
            conn.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
        
    return jsonify({'success': True})

@app.route('/enrollments/delete/<int:id>', methods=['POST'])
def delete_enrollment(id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM enrollments WHERE id = %s', (id,))
            conn.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
        
    return jsonify({'success': True})

@app.route('/enrollments/view/<int:enrollment_id>')
def view_enrollment(enrollment_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get enrollment details with student and program info
            cursor.execute('''
                SELECT e.*, 
                       s.first_name, s.last_name, s.dob, s.gender, s.student_photo,
                       s.allergies, s.medical_info,
                       p.name as program_name, p.description as program_description,
                       u.name as parent_name, u.email as parent_email, u.phone as parent_phone
                FROM enrollments e
                JOIN students s ON e.student_id = s.id
                JOIN programs p ON e.program_id = p.id
                LEFT JOIN users u ON s.parent_id = u.id
                WHERE e.id = %s
            ''', (enrollment_id,))
            enrollment = cursor.fetchone()
            
            if not enrollment:
                flash('Matrícula no encontrada', 'error')
                return redirect(url_for('manage_enrollments'))
            
            return render_template('dashboard/admin/enrollment_detail.html', enrollment=enrollment)
    finally:
        conn.close()


# ========================================
# RUTAS ADICIONALES PARA FORMULARIOS
# ========================================

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if email exists
                cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
                if cursor.fetchone():
                    flash('El correo electrónico ya está registrado', 'error')
                    return render_template('dashboard/admin/user_form.html', user=None)
                
                hashed_password = generate_password_hash(password)
                cursor.execute('INSERT INTO users (name, email, phone, role, password) VALUES (%s, %s, %s, %s, %s)',
                             (name, email, phone, role, hashed_password))
                conn.commit()
                flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('manage_users'))
        except Exception as e:
            flash(f'Error al crear usuario: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/user_form.html', user=None)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category = request.form.get('category')
        description = request.form.get('description')
        image = request.files.get('image')
        
        image_data = None
        image_type = None
        
        if image and image.filename:
            try:
                # Comprimir imagen (800x800, 85%)
                image_data, image_type = compress_image(image, max_width=800, max_height=800, quality=85)
            except Exception as e:
                flash(f'Error al procesar imagen: {str(e)}', 'error')
                return render_template('dashboard/admin/product_form.html', product=None)
            
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO products (name, price, stock, category, description, image_data, image_type) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                             (name, price, stock, category, description, image_data, image_type))
                conn.commit()
                flash('Producto agregado exitosamente', 'success')
                return redirect(url_for('manage_products'))
        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/product_form.html', product=None)

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form.get('price')
            product = cursor.fetchone()
            
            if not product:
                flash('Producto no encontrado', 'error')
                return redirect(url_for('manage_products'))
                
            return render_template('dashboard/admin/product_form.html', product=product)
    finally:
        conn.close()

@app.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            conn.commit()
            flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('manage_products'))

# ========================================
# REPORTES
# ========================================

@app.route('/reports/manage')
def manage_reports():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Join with users to get student details
            cursor.execute('''
                SELECT r.*, u.name as student_name, u.email as student_email 
                FROM student_reports r 
                JOIN users u ON r.student_id = u.id 
                ORDER BY r.created_at DESC
            ''')
            reports = cursor.fetchall()
            
            # Fetch students for the upload modal
            cursor.execute("SELECT id, name, email FROM users WHERE role != 'admin' ORDER BY name")
            students = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_reports.html', reports=reports, students=students)

@app.route('/reports/upload', methods=['GET', 'POST'])
def upload_report():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                student_id = request.form.get('student_id')
                title = request.form.get('title')
                description = request.form.get('description')
                file = request.files.get('report_file')
                print(f"DEBUG: request.files keys: {request.files.keys()}")
                print(f"DEBUG: file object: {file}")
                if file:
                    print(f"DEBUG: filename: {file.filename}")
                
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    base, ext = os.path.splitext(filename)
                    filename = f"{base}_{int(time.time())}{ext}"
                    
                    # Compress and prepare for DB
                    file_data, file_type = compress_pdf(file)
                    
                    cursor.execute('INSERT INTO student_reports (student_id, user_id, title, content, file_url, file_data, file_type) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                 (student_id, student_id, title, description, filename, file_data, file_type))
                    conn.commit()
                    flash('Reporte subido exitosamente', 'success')
                    return redirect(url_for('manage_reports'))
                else:
                    flash('Debe seleccionar un archivo PDF', 'error')
            
            # Fetch students for the dropdown
            # Assuming 'student' role exists, or we list all users for now if roles aren't strictly 'student'
            # Let's assume we want to list all users who are likely students/parents.
            # For now, let's list all users except admins to be safe, or just all users.
            cursor.execute("SELECT id, name, email FROM users WHERE role != 'admin' ORDER BY name")
            students = cursor.fetchall()
            
            return render_template('dashboard/admin/reports_form.html', students=students)
    finally:
        conn.close()

@app.route('/reports/delete/<int:report_id>')
def delete_report(report_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Delete report from database
            cursor.execute('DELETE FROM student_reports WHERE id = %s', (report_id,))
            conn.commit()
            flash('Reporte eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar reporte: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('manage_reports'))

# ========================================
# GESTIÓN ACADÉMICA (ADMIN/STAFF)
# ========================================

@app.route('/schedule/manage')
def manage_schedule():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT cs.*, c.name as course_name, p.name as program_name
                            FROM class_schedule cs
                            JOIN courses c ON cs.course_id = c.id
                            JOIN programs p ON c.program_id = p.id
                            ORDER BY cs.day_of_week, cs.start_time''')
            schedules = cursor.fetchall()
            
            cursor.execute('SELECT c.*, p.name as program_name FROM courses c JOIN programs p ON c.program_id = p.id')
            courses = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_schedule.html', schedules=schedules, courses=courses)

# ========================================
# COURSE MANAGEMENT ROUTES
# ========================================

@app.route('/courses/manage')
def manage_courses():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT c.*, p.name as program_name 
                            FROM courses c 
                            JOIN programs p ON c.program_id = p.id 
                            ORDER BY p.name, c.name''')
            courses = cursor.fetchall()
            
            cursor.execute('SELECT id, name FROM programs WHERE is_active = TRUE ORDER BY name')
            programs = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_courses.html', courses=courses, programs=programs)

@app.route('/courses/add', methods=['POST'])
def add_course():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    program_id = request.form.get('program_id')
    name = request.form.get('name')
    description = request.form.get('description', '')
    teacher_name = request.form.get('teacher_name', '')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO courses (program_id, name, description, teacher_name) 
                            VALUES (%s, %s, %s, %s)''',
                         (program_id, name, description, teacher_name))
            conn.commit()
            flash('Curso agregado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar curso: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_courses'))

@app.route('/courses/edit/<int:course_id>', methods=['POST'])
def edit_course(course_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    program_id = request.form.get('program_id')
    name = request.form.get('name')
    description = request.form.get('description', '')
    teacher_name = request.form.get('teacher_name', '')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''UPDATE courses 
                            SET program_id = %s, name = %s, description = %s, teacher_name = %s 
                            WHERE id = %s''',
                         (program_id, name, description, teacher_name, course_id))
            conn.commit()
            flash('Curso actualizado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar curso: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_courses'))

@app.route('/courses/delete/<int:course_id>')
def delete_course(course_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM courses WHERE id = %s', (course_id,))
            conn.commit()
            flash('Curso eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar curso: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_courses'))


@app.route('/schedule/add', methods=['POST'])
def add_schedule():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False}), 403
    
    course_id = request.form.get('course_id')
    day_of_week = request.form.get('day_of_week')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    room = request.form.get('room')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO class_schedule (course_id, day_of_week, start_time, end_time, room) VALUES (%s, %s, %s, %s, %s)',
                         (course_id, day_of_week, start_time, end_time, room))
            conn.commit()
            flash('Horario agregado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar horario: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_schedule'))

@app.route('/schedule/delete/<int:schedule_id>')
def delete_schedule(schedule_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM class_schedule WHERE id = %s', (schedule_id,))
            conn.commit()
            flash('Horario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar horario: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_schedule'))

@app.route('/assignments/manage')
def manage_assignments_admin():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT a.*, c.name as course_name, p.name as program_name,
                            COUNT(s.id) as submission_count
                            FROM assignments a
                            JOIN courses c ON a.course_id = c.id
                            JOIN programs p ON c.program_id = p.id
                            LEFT JOIN submissions s ON a.id = s.assignment_id
                            GROUP BY a.id
                            ORDER BY a.due_date DESC''')
            assignments = cursor.fetchall()
            
            cursor.execute('SELECT c.*, p.name as program_name FROM courses c JOIN programs p ON c.program_id = p.id')
            courses = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_assignments.html', assignments=assignments, courses=courses)

@app.route('/dashboard/assignments/submit/<int:assignment_id>', methods=['POST'])
def submit_assignment(assignment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    student_id = request.form.get('student_id')
    comments = request.form.get('comments')
    file = request.files.get('file')
    
    if not file:
        flash('Debe subir un archivo', 'error')
        return redirect(request.referrer or url_for('student_grades')) # Fallback redirect
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Verify enrollment/student belongs to parent? (Optional but good for security)
            
            filename = secure_filename(file.filename)
            file_data, file_type = compress_pdf(file) # Assuming PDF submissions mostly
            
            cursor.execute('''INSERT INTO submissions (assignment_id, student_id, file_url, file_data, file_type, comments, status)
                            VALUES (%s, %s, %s, %s, %s, %s, 'submitted')
                            ON DUPLICATE KEY UPDATE 
                            file_url = VALUES(file_url), 
                            file_data = VALUES(file_data), 
                            file_type = VALUES(file_type),
                            comments = VALUES(comments),
                            submission_date = CURRENT_TIMESTAMP,
                            status = 'submitted'
                            ''',
                         (assignment_id, student_id, filename, file_data, file_type, comments))
            conn.commit()
            flash('Tarea entregada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al entregar tarea: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(request.referrer or url_for('student_grades'))

@app.route('/assignments/add_admin', methods=['POST'])
def add_assignment_admin():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        conn.close()
    
    return redirect(url_for('manage_assignments_admin'))

@app.route('/assignments/grade/<int:assignment_id>')
def grade_assignment(assignment_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM assignments WHERE id = %s', (assignment_id,))
            assignment = cursor.fetchone()
            
            cursor.execute('''SELECT s.*, st.first_name, st.last_name
                            FROM submissions s
                            JOIN students st ON s.student_id = st.id
                            WHERE s.assignment_id = %s''', (assignment_id,))
            submissions = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/grade_assignment.html', assignment=assignment, submissions=submissions)

@app.route('/student/assignments')
def student_assignments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # For now, return a simple message or empty assignments list
    # You can implement the full functionality later
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get assignments for the student (placeholder query)
            cursor.execute('''SELECT a.*, c.name as course_name
                            FROM assignments a
                            JOIN courses c ON a.course_id = c.id
                            ORDER BY a.due_date DESC
                            LIMIT 10''')
            assignments = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/student/assignments.html', assignments=assignments)

@app.route('/student/messages')
def student_messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Placeholder for messages functionality
    messages = []
    
    return render_template('dashboard/student/messages.html', messages=messages)

@app.route('/submissions/grade/<int:submission_id>', methods=['POST'])
def grade_submission(submission_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False}), 403
    
    grade = request.form.get('grade')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE submissions SET grade = %s, status = %s WHERE id = %s',
                         (grade, 'graded', submission_id))
            conn.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
    
    return jsonify({'success': True})

@app.route('/attendance/manage')
def manage_attendance():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM programs WHERE is_active = TRUE')
            programs = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_attendance.html', programs=programs)

@app.route('/attendance/take', methods=['POST'])
def take_attendance():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False}), 403
    
    data = request.get_json()
    program_id = data.get('program_id')
    date = data.get('date')
    attendance_records = data.get('records', [])
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for record in attendance_records:
                enrollment_id = record.get('enrollment_id')
                status = record.get('status')
                remarks = record.get('remarks', '')
                
                cursor.execute('''INSERT INTO attendance (enrollment_id, date, status, remarks)
                                VALUES (%s, %s, %s, %s)
                                ON DUPLICATE KEY UPDATE status = VALUES(status), remarks = VALUES(remarks)''',
                             (enrollment_id, date, status, remarks))
            conn.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
    
    return jsonify({'success': True})

@app.route('/attendance/get/<int:program_id>/<date>')
def get_attendance(program_id, date):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return jsonify({'success': False}), 403
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT e.id as enrollment_id, s.first_name, s.last_name,
                            a.status, a.remarks
                            FROM enrollments e
                            JOIN students s ON e.student_id = s.id
                            LEFT JOIN attendance a ON e.id = a.enrollment_id AND a.date = %s
                            WHERE e.program_id = %s AND e.status = 'active'
                            ORDER BY s.last_name, s.first_name''',
                         (date, program_id))
            students = cursor.fetchall()
    finally:
        conn.close()
    
    return jsonify({'success': True, 'students': students})

# ========================================
# GESTIÓN DE EVENTOS (ADMIN/STAFF)

@app.route('/events/manage')
def manage_events():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM events ORDER BY start_date DESC')
            events = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_events.html', events=events)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        type = request.form.get('type')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO events (title, description, start_date, end_date, type) VALUES (%s, %s, %s, %s, %s)',
                             (title, description, start_date, end_date, type))
                conn.commit()
                flash('Evento agregado exitosamente', 'success')
                return redirect(url_for('manage_events'))
        except Exception as e:
            flash(f'Error al agregar evento: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/event_form.html', event=None)

@app.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                title = request.form.get('title')
                description = request.form.get('description')
                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')
                type = request.form.get('type')
                
                cursor.execute('UPDATE events SET title = %s, description = %s, start_date = %s, end_date = %s, type = %s WHERE id = %s',
                             (title, description, start_date, end_date, type, event_id))
                conn.commit()
                flash('Evento actualizado exitosamente', 'success')
                return redirect(url_for('manage_events'))
            
            cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
            event = cursor.fetchone()
            
            if not event:
                flash('Evento no encontrado', 'error')
                return redirect(url_for('manage_events'))
                
            return render_template('dashboard/admin/event_form.html', event=event)
    finally:
        conn.close()

@app.route('/events/delete/<int:event_id>')
def delete_event(event_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM events WHERE id = %s', (event_id,))
            conn.commit()
            flash('Evento eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar evento: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('manage_events'))

@app.route('/menu/manage')
def manage_menu():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Order by custom day order could be tricky in SQL, but for now simple select
            # We can sort in python or add a day_index column later if needed.
            cursor.execute('SELECT * FROM menu_items')
            menu_items = cursor.fetchall()
            
            # Sort by day order
            days_order = {'Lunes': 1, 'Martes': 2, 'Miércoles': 3, 'Jueves': 4, 'Viernes': 5}
            menu_items = sorted(menu_items, key=lambda x: days_order.get(x['day'], 6))
            
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_menu.html', menu_items=menu_items)

@app.route('/menu/add', methods=['GET', 'POST'])
def add_menu_item():
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        day = request.form.get('day')
        type = request.form.get('type')
        meal_description = request.form.get('meal_description')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO menu_items (day, type, meal_description) VALUES (%s, %s, %s)',
                             (day, type, meal_description))
                conn.commit()
                flash('Plato agregado exitosamente', 'success')
                return redirect(url_for('manage_menu'))
        except Exception as e:
            flash(f'Error al agregar plato: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('dashboard/admin/menu_form.html', item=None)

@app.route('/menu/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_menu_item(item_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                day = request.form.get('day')
                type = request.form.get('type')
                meal_description = request.form.get('meal_description')
                
                cursor.execute('UPDATE menu_items SET day = %s, type = %s, meal_description = %s WHERE id = %s',
                             (day, type, meal_description, item_id))
                conn.commit()
                flash('Plato actualizado exitosamente', 'success')
                return redirect(url_for('manage_menu'))
            
            cursor.execute('SELECT * FROM menu_items WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            
            if not item:
                flash('Plato no encontrado', 'error')
                return redirect(url_for('manage_menu'))
                
            return render_template('dashboard/admin/menu_form.html', item=item)
    finally:
        conn.close()

@app.route('/menu/delete/<int:item_id>')
def delete_menu_item(item_id):
    if 'user_id' not in session or session.get('user_role') not in ['admin', 'staff']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM menu_items WHERE id = %s', (item_id,))
            conn.commit()
            flash('Plato eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar plato: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('manage_menu'))

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT password FROM users WHERE id = %s', (session['user_id'],))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], current_password):
                hashed_password = generate_password_hash(new_password)
                cursor.execute('UPDATE users SET password = %s WHERE id = %s',
                             (hashed_password, session['user_id']))
                conn.commit()
                flash('Contraseña actualizada exitosamente', 'success')
            else:
                flash('Contraseña actual incorrecta', 'error')
    except Exception as e:
        flash(f'Error al cambiar contraseña: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('profile'))

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    flash('Preferencias actualizadas', 'success')
    return redirect(url_for('profile'))

@app.route('/process_order', methods=['POST'])
def process_order():
    """Alias para checkout POST"""
    return checkout()

# ========================================
# GESTIÓN DE COMENTARIOS (ADMIN)
# ========================================

@app.route('/admin/comments')
def manage_comments():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM comments ORDER BY created_at DESC')
            comments = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_comments.html', comments=comments)

@app.route('/admin/comments/toggle/<int:comment_id>', methods=['POST'])
def toggle_comment_approval(comment_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get current status
            cursor.execute('SELECT is_approved FROM comments WHERE id = %s', (comment_id,))
            comment = cursor.fetchone()
            
            if comment:
                new_status = not comment['is_approved']
                cursor.execute('UPDATE comments SET is_approved = %s WHERE id = %s', 
                             (new_status, comment_id))
                conn.commit()
                
                if new_status:
                    flash('Comentario aprobado exitosamente', 'success')
                else:
                    flash('Comentario desaprobado', 'warning')
            else:
                flash('Comentario no encontrado', 'error')
    except Exception as e:
        flash(f'Error al actualizar comentario: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_comments'))

@app.route('/admin/comments/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM comments WHERE id = %s', (comment_id,))
            conn.commit()
            flash('Comentario eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar comentario: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_comments'))

# ========================================
# GESTIÓN DE RECLAMOS (ADMIN)
# ========================================

@app.route('/admin/complaints')
def manage_complaints():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM complaints ORDER BY created_at DESC')
            complaints = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_complaints.html', complaints=complaints)

@app.route('/admin/complaints/view/<int:complaint_id>')
def view_complaint(complaint_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM complaints WHERE id = %s', (complaint_id,))
            complaint = cursor.fetchone()
            
            if not complaint:
                flash('Reclamo no encontrado', 'error')
                return redirect(url_for('manage_complaints'))
    finally:
        conn.close()
    
    return render_template('dashboard/admin/complaint_detail.html', complaint=complaint)

@app.route('/admin/complaints/update_status/<int:complaint_id>', methods=['POST'])
def update_complaint_status(complaint_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'in_process', 'resolved']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE complaints SET status = %s WHERE id = %s', (new_status, complaint_id))
            conn.commit()
            
            # Get complainant email for notification
            cursor.execute('SELECT email, name, lastname FROM complaints WHERE id = %s', (complaint_id,))
            complaint = cursor.fetchone()
            
            # TODO: Send email notification to complainant
            
        return jsonify({'success': True, 'message': 'Estado actualizado correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/admin/complaints/delete/<int:complaint_id>', methods=['POST'])
def delete_complaint(complaint_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM complaints WHERE id = %s', (complaint_id,))
            conn.commit()
            flash('Reclamo eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar reclamo: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_complaints'))

# ========================================
# GESTIÓN DE PROGRAMAS
# ========================================

@app.route('/admin/programs')
def manage_programs():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT p.*, 
                    (SELECT COUNT(*) FROM enrollments WHERE program_id = p.id) as enrolled_count
                FROM programs p
                ORDER BY p.created_at DESC
            ''')
            programs = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/manage_programs.html', programs=programs)

@app.route('/admin/programs/create', methods=['GET', 'POST'])
def create_program():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        age_range = request.form.get('age_range')
        academic_year = request.form.get('academic_year')
        registration_fee = request.form.get('registration_fee', 0)
        monthly_fee = request.form.get('monthly_fee', 0)
        capacity = request.form.get('capacity', 20)
        is_active = request.form.get('is_active') == 'on'
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO programs (name, description, age_range, academic_year, 
                                         registration_fee, monthly_fee, capacity, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (name, description, age_range, academic_year, registration_fee, 
                      monthly_fee, capacity, is_active))
                conn.commit()
                flash('Programa creado exitosamente', 'success')
                return redirect(url_for('manage_programs'))
        except Exception as e:
            flash(f'Error al crear programa: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('dashboard/admin/program_form.html', program=None)

@app.route('/admin/programs/edit/<int:program_id>', methods=['GET', 'POST'])
def edit_program(program_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        age_range = request.form.get('age_range')
        academic_year = request.form.get('academic_year')
        registration_fee = request.form.get('registration_fee', 0)
        monthly_fee = request.form.get('monthly_fee', 0)
        capacity = request.form.get('capacity', 20)
        is_active = request.form.get('is_active') == 'on'
        
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    UPDATE programs 
                    SET name = %s, description = %s, age_range = %s, academic_year = %s,
                        registration_fee = %s, monthly_fee = %s, capacity = %s, is_active = %s
                    WHERE id = %s
                ''', (name, description, age_range, academic_year, registration_fee,
                      monthly_fee, capacity, is_active, program_id))
                conn.commit()
                flash('Programa actualizado exitosamente', 'success')
                return redirect(url_for('manage_programs'))
        except Exception as e:
            flash(f'Error al actualizar programa: {str(e)}', 'error')
        finally:
            conn.close()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM programs WHERE id = %s', (program_id,))
            program = cursor.fetchone()
            if not program:
                flash('Programa no encontrado', 'error')
                return redirect(url_for('manage_programs'))
    finally:
        conn.close()
    
    return render_template('dashboard/admin/program_form.html', program=program)

@app.route('/admin/programs/toggle/<int:program_id>', methods=['POST'])
def toggle_program_status(program_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Acceso denegado'}), 403
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT is_active FROM programs WHERE id = %s', (program_id,))
            program = cursor.fetchone()
            if not program:
                return jsonify({'success': False, 'message': 'Programa no encontrado'}), 404
            
            new_status = not program['is_active']
            cursor.execute('UPDATE programs SET is_active = %s WHERE id = %s', 
                          (new_status, program_id))
            conn.commit()
            
            return jsonify({
                'success': True, 
                'is_active': new_status,
                'message': 'Estado actualizado correctamente'
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/admin/programs/delete/<int:program_id>', methods=['POST'])
def delete_program(program_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Verificar si hay matrículas asociadas
            cursor.execute('SELECT COUNT(*) as count FROM enrollments WHERE program_id = %s', (program_id,))
            result = cursor.fetchone()
            
            if result['count'] > 0:
                flash(f'No se puede eliminar el programa. Tiene {result["count"]} matrícula(s) asociada(s).', 'error')
            else:
                cursor.execute('DELETE FROM programs WHERE id = %s', (program_id,))
                conn.commit()
                flash('Programa eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar programa: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('manage_programs'))

@app.route('/admin/programs/view/<int:program_id>')
def view_program(program_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM programs WHERE id = %s', (program_id,))
            program = cursor.fetchone()
            
            if not program:
                flash('Programa no encontrado', 'error')
                return redirect(url_for('manage_programs'))
            
            # Obtener matrículas asociadas
            cursor.execute('''
                SELECT e.*, u.name as student_name, u.lastname as student_lastname, 
                       u.email as student_email
                FROM enrollments e
                JOIN users u ON e.user_id = u.id
                WHERE e.program_id = %s
                ORDER BY e.created_at DESC
            ''', (program_id,))
            enrollments = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard/admin/program_detail.html', 
                         program=program, enrollments=enrollments)

# ========================================
# INICIALIZACIÓN
# ========================================

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
