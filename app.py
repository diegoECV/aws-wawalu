from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave segura en producción

# Configuración de subida de archivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que existe el directorio de uploads
os.makedirs(os.path.join(app.root_path, UPLOAD_FOLDER), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración de la base de datos
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1416')
DB_NAME = os.getenv('DB_NAME', 'wawalu_db')

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def update_db_schema():
    conn = get_db_connection()

def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if we need to insert sample data for comments
            try:
                cursor.execute("SELECT COUNT(*) as count FROM comments")
                result = cursor.fetchone()
                if result['count'] == 0:
                    sample_data = [
                        ("Ana Martínez", "Mamá de Lucía", "La dedicación y el cariño con el que tratan a los niños es excepcional. Mi hija ha crecido tanto desde que está en Wawalu."),
                        ("Carlos Ruiz", "Papá de Mateo", "La metodología de enseñanza es increíble. Mi hijo ha desarrollado habilidades que no imaginábamos a su edad.")
                    ]
                    cursor.executemany(
                        "INSERT INTO comments (name, relation, comment) VALUES (%s, %s, %s)",
                        sample_data
                    )
                conn.commit()
            except Exception as e:
                print(f"Skipping sample data insertion (table might not exist): {e}")
                
    except Exception as e:
        print(f"Error initializing DB: {e}")
    finally:
        conn.close()
    
    # Run schema updates
    update_db_schema()


@app.route('/')

@app.route('/')
def index():
    comments = []
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM comments WHERE is_approved = TRUE ORDER BY created_at DESC LIMIT 6')
            comments = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching comments: {e}")
    finally:
        conn.close()
    return render_template('index.html', comments=comments)

# Ruta pública para la tienda
@app.route('/public_shop')
def public_shop():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            products = cursor.fetchall()
    finally:
        conn.close()
    return render_template('public_shop.html', products=products)
    return render_template('index.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        relation = request.form['relation']
        comment = request.form['comment']
        next_page = request.form.get('next', url_for('index'))
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO comments (name, relation, comment) VALUES (%s, %s, %s)',
                    (name, relation, comment)
                )
                conn.commit()
                flash('¡Gracias por tu comentario! Se ha publicado exitosamente.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al publicar comentario: {str(e)}', 'error')
        finally:
            conn.close()
            
        return redirect(next_page)

@app.route('/comentarios')
def comments():
    comments = []
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM comments WHERE is_approved = TRUE ORDER BY created_at DESC')
            comments = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching comments: {e}")
    finally:
        conn.close()
    return render_template('comments.html', comments=comments)

@app.route('/nosotros')
def about():
    return render_template('about.html')

@app.route('/programas')
def programs():
    return render_template('programs.html')


# Ruta pública para galería
@app.route('/public_galery')
def public_galery():
    category = request.args.get('category')
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if category:
                cursor.execute('SELECT * FROM galery_items WHERE category = %s ORDER BY created_at DESC', (category,))
            else:
                cursor.execute('SELECT * FROM galery_items ORDER BY created_at DESC')
            galery_items = cursor.fetchall()
    finally:
        conn.close()
    return render_template('public_galery.html', galery_items=galery_items, current_category=category)

@app.route('/noticias')
def public_news():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
            news_items = cursor.fetchall()
    finally:
        conn.close()
    return render_template('public_news.html', news_items=news_items)

@app.route('/noticias/<int:news_id>')
def news_detail(news_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news WHERE id = %s', (news_id,))
            news = cursor.fetchone()
            if not news:
                return redirect(url_for('public_news'))
    finally:
        conn.close()
    return render_template('news-detail.html', news=news)

@app.route('/carrito')
def public_cart():
    """Public cart - accessible without login"""
    cart_data = session.get('cart', {})
    cart_items = []
    total = 0
    
    if cart_data:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                product_ids = list(map(int, cart_data.keys()))
                
                if product_ids:
                    format_strings = ','.join(['%s'] * len(product_ids))
                    cursor.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", tuple(product_ids))
                    products = cursor.fetchall()
                    
                    for product in products:
                        pid = str(product['id'])
                        if pid in cart_data:
                            qty = cart_data[pid]
                            product['quantity'] = qty
                            product['subtotal'] = float(product['price']) * qty
                            cart_items.append(product)
                            total += product['subtotal']
        finally:
            conn.close()
            
    return render_template('public_cart.html', cart_items=cart_items, total=total)

# --- Dashboard Routes ---

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard/index.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
            user = cursor.fetchone()
    finally:
        conn.close()
        
    return render_template('dashboard/profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    
    # Handle Image Upload
    profile_image = None
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add user_id prefix to avoid collisions
            filename = f"user_{session['user_id']}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = filename
            session['profile_image'] = filename # Update session

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if profile_image:
                cursor.execute(
                    'UPDATE users SET name = %s, email = %s, phone = %s, address = %s, profile_image = %s WHERE id = %s',
                    (name, email, phone, address, profile_image, session['user_id'])
                )
            else:
                cursor.execute(
                    'UPDATE users SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s',
                    (name, email, phone, address, session['user_id'])
                )
            conn.commit()
            session['user_name'] = name # Update session
            flash('Perfil actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar perfil: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('profile'))


@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    if new_password != confirm_password:
        flash('Las contraseñas nuevas no coinciden', 'error')
        return redirect(url_for('profile'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT password FROM users WHERE id = %s', (session['user_id'],))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], current_password):
                hashed_password = generate_password_hash(new_password)
                cursor.execute('UPDATE users SET password = %s WHERE id = %s', (hashed_password, session['user_id']))
                conn.commit()
                flash('Contraseña actualizada correctamente', 'success')
            else:
                flash('La contraseña actual es incorrecta', 'error')
    except Exception as e:
        flash(f'Error al cambiar contraseña: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('profile'))

@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Checkboxes are only sent if checked. Default to False if missing.
    notifications_email = 1 if 'notifications_email' in request.form else 0
    notifications_orders = 1 if 'notifications_orders' in request.form else 0
    notifications_promo = 1 if 'notifications_promo' in request.form else 0
    privacy_session = 1 if 'privacy_session' in request.form else 0
    privacy_analysis = 1 if 'privacy_analysis' in request.form else 0
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                '''UPDATE users SET 
                   notifications_email = %s, 
                   notifications_orders = %s, 
                   notifications_promo = %s, 
                   privacy_session = %s, 
                   privacy_analysis = %s 
                   WHERE id = %s''',
                (notifications_email, notifications_orders, notifications_promo, privacy_session, privacy_analysis, session['user_id'])
            )
            conn.commit()
            flash('Preferencias actualizadas correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar preferencias: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('profile'))

@app.route('/galery')
def galery():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    category = request.args.get('category')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if category:
                cursor.execute('SELECT * FROM galery_items WHERE category = %s ORDER BY created_at DESC', (category,))
            else:
                cursor.execute('SELECT * FROM galery_items ORDER BY created_at DESC')
            galery_items = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/galery.html', galery_items=galery_items, current_category=category)

@app.route('/galery/upload', methods=['POST'])
def upload_galery():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # Check permission (simple role check)
    if session.get('user_role') not in ['staff', 'admin']:
        flash('No tienes permiso para realizar esta acción', 'error')
        return redirect(url_for('galery'))

    title = request.form['title']
    category = request.form['category']
    
    if 'image' not in request.files:
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(url_for('galery'))
        
    file = request.files['image']
    
    if file.filename == '':
        flash('No se seleccionó ninguna imagen', 'error')
        return redirect(url_for('galery'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid collisions
        import time
        filename = f"galery_{int(time.time())}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO galery_items (title, image_url, category) VALUES (%s, %s, %s)',
                    (title, filename, category)
                )
                conn.commit()
            flash('Foto subida exitosamente', 'success')
        except Exception as e:
            flash(f'Error al subir foto: {str(e)}', 'error')
        finally:
            conn.close()
            
    return redirect(url_for('galery'))

@app.route('/galery/delete/<int:item_id>', methods=['POST'])
def delete_galery_item(item_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Get image filename to delete file
            cursor.execute('SELECT image_url FROM galery_items WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            
            if item:
                # Delete from DB
                cursor.execute('DELETE FROM galery_items WHERE id = %s', (item_id,))
                conn.commit()
                
                # Delete file from filesystem
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], item['image_url'])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                flash('Foto eliminada correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar foto: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('galery'))

@app.route('/shop')
def shop():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            products = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/shop.html', products=products)

@app.route('/shop/add', methods=['POST'])
def add_product():
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    name = request.form['name']
    price = request.form['price']
    category = request.form['category']
    description = request.form['description']
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import time
            filename = f"product_{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = filename
            
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO products (name, price, category, description, image_url) VALUES (%s, %s, %s, %s, %s)',
                (name, price, category, description, image_url)
            )
            conn.commit()
        flash('Producto agregado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agregar producto: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('shop'))

@app.route('/shop/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            conn.commit()
        flash('Producto eliminado', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'error')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
            news_items = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/news.html', news_items=news_items)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    cart_data = session.get('cart', {}) # Now storing {product_id: quantity}
    cart_items = []
    total = 0
    
    if cart_data:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Get all product IDs from cart keys
                product_ids = list(map(int, cart_data.keys()))
                
                if product_ids:
                    format_strings = ','.join(['%s'] * len(product_ids))
                    cursor.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", tuple(product_ids))
                    products = cursor.fetchall()
                    
                    for product in products:
                        pid = str(product['id'])
                        if pid in cart_data:
                            qty = cart_data[pid]
                            product['quantity'] = qty
                            product['subtotal'] = float(product['price']) * qty
                            cart_items.append(product)
                            total += product['subtotal']
        finally:
            conn.close()
            
    return render_template('dashboard/cart.html', cart_items=cart_items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    # Ensure cart is a dict (migration from list if needed, though session clear handles it)
    if isinstance(session['cart'], list):
        session['cart'] = {}
        
    pid = str(product_id)
    if pid in session['cart']:
        session['cart'][pid] += quantity
    else:
        session['cart'][pid] = quantity
        
    session.modified = True
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('shop'))

@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    quantity = int(request.form.get('quantity', 1))
    pid = str(product_id)
    
    if 'cart' in session and pid in session['cart']:
        if quantity > 0:
            session['cart'][pid] = quantity
        else:
            del session['cart'][pid]
        session.modified = True
        
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    pid = str(product_id)
    if 'cart' in session and pid in session['cart']:
        del session['cart'][pid]
        session.modified = True
        flash('Producto eliminado del carrito', 'success')
        
    return redirect(url_for('cart'))

@app.route('/news')
def news():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
            news_items = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/news.html', news_items=news_items)

@app.route('/news/add', methods=['POST'])
def add_news():
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    title = request.form['title']
    content = request.form['content']
    
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            import time
            filename = f"news_{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = filename
            
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO news (title, content, image_url) VALUES (%s, %s, %s)',
                (title, content, image_url)
            )
            conn.commit()
        flash('Noticia publicada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al publicar noticia: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('news'))

@app.route('/news/delete/<int:news_id>', methods=['POST'])
def delete_news(news_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM news WHERE id = %s', (news_id,))
            conn.commit()
        flash('Noticia eliminada', 'success')
    except Exception as e:
        flash(f'Error al eliminar noticia: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('news'))

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

@app.route('/calendar/add', methods=['POST'])
def add_event():
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    title = request.form['title']
    start_date = request.form['start_date']
    end_date = request.form['end_date'] or None
    event_type = request.form['type']
    description = request.form['description']
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO events (title, description, start_date, end_date, type) VALUES (%s, %s, %s, %s, %s)',
                (title, description, start_date, end_date, event_type)
            )
            conn.commit()
        flash('Evento agendado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al agendar evento: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('calendar'))

@app.route('/calendar/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM events WHERE id = %s', (event_id,))
            conn.commit()
        flash('Evento eliminado', 'success')
    except Exception as e:
        flash(f'Error al eliminar evento: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('calendar'))

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM menus ORDER BY id ASC') # Assuming ID order keeps insertion order roughly or add sort logic
            menu_items = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/menu.html', menu_items=menu_items)

@app.route('/menu/add', methods=['POST'])
def add_menu():
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    day = request.form['day']
    meal_type = request.form['type']
    description = request.form['meal_description']
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO menus (date, type, meal_description) VALUES (%s, %s, %s)',
                (day, meal_type, description) # Using 'date' column to store Day name for simplicity as per template logic
            )
            conn.commit()
        flash('Menú actualizado', 'success')
    except Exception as e:
        flash(f'Error al actualizar menú: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('menu'))

@app.route('/menu/delete/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM menus WHERE id = %s', (menu_id,))
            conn.commit()
        flash('Item eliminado del menú', 'success')
    except Exception as e:
        flash(f'Error al eliminar item: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('menu'))

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # If staff, show all. If parent, show only their kids (simplified here to show all for demo or filter by user if we had linking)
            # For this MVP, we'll show all reports to everyone, or filter by name if we had that logic.
            # Let's show all for now as per simple requirements, or maybe filter by user_id if we stored it.
            cursor.execute('SELECT * FROM student_reports ORDER BY created_at DESC')
            reports = cursor.fetchall()
    finally:
        conn.close()
        
    return render_template('dashboard/reports.html', reports=reports)

@app.route('/reports/add', methods=['POST'])
def add_report():
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    title = request.form['title']
    student_name = request.form['student_name']
    
    file_url = None
    if 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '' and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            import time
            filename = f"report_{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = filename
            
    if not file_url:
        flash('Debe subir un archivo PDF válido', 'error')
        return redirect(url_for('reports'))
            
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO student_reports (title, student_id, user_id, file_url, created_at) VALUES (%s, %s, %s, %s, NOW())',
                (title, student_name, session['user_id'], file_url) # Reusing student_id column for student name string for simplicity in this MVP or need to adjust schema
            )
            conn.commit()
        flash('Reporte subido exitosamente', 'success')
    except Exception as e:
        flash(f'Error al subir reporte: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('reports'))

@app.route('/reports/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    if 'user_id' not in session or session.get('user_role') not in ['staff', 'admin']:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT file_url FROM student_reports WHERE id = %s', (report_id,))
            report = cursor.fetchone()
            
            if report:
                cursor.execute('DELETE FROM student_reports WHERE id = %s', (report_id,))
                conn.commit()
                
                # Delete file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], report['file_url'])
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                flash('Reporte eliminado', 'success')
    except Exception as e:
        flash(f'Error al eliminar reporte: {str(e)}', 'error')
    finally:
        conn.close()
        
    return redirect(url_for('reports'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['user_role'] = user['role']
                    session['profile_image'] = user.get('profile_image') # Store image in session
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Correo o contraseña incorrectos', 'error')
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'padre') # Default to padre if not specified
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Check if email exists
                cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
                if cursor.fetchone():
                    flash('El correo electrónico ya está registrado', 'error')
                    return redirect(url_for('register'))
                
                # Hash password and insert user
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    'INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)',
                    (name, email, hashed_password, role)
                )
                conn.commit()
                flash('Registro exitoso. Por favor inicia sesión.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f'Error en el registro: {str(e)}', 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/terminos')
def terms():
    return render_template('terms.html')

@app.route('/privacidad')
def privacy():
    return render_template('privacy.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)',
                    (name, email, subject, message)
                )
                conn.commit()
            conn.close()
            flash('Mensaje enviado. Espere nuestra respuesta.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Error al enviar mensaje: {str(e)}', 'error')
            
    return render_template('contact.html')

@app.route('/reclamaciones', methods=['GET', 'POST'])
def complaints():
    if request.method == 'POST':
        try:
            # Extract form data
            data = {
                'name': request.form['name'],
                'lastname': request.form['lastname'],
                'doc_type': request.form['doc_type'],
                'document_number': request.form['document_number'],
                'phone': request.form['phone'],
                'email': request.form['email'],
                'address': request.form['address'],
                'good_type': request.form['good_type'],
                'amount': request.form['amount'],
                'good_description': request.form['good_description'],
                'claim_type': request.form['claim_type'],
                'claim_detail': request.form['claim_detail'],
                'consumer_request': request.form['consumer_request']
            }
            
            conn = get_db_connection()
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO complaints (
                        name, lastname, doc_type, document_number, phone, email, address,
                        good_type, amount, good_description, claim_type, claim_detail, consumer_request
                    ) VALUES (
                        %(name)s, %(lastname)s, %(doc_type)s, %(document_number)s, %(phone)s, %(email)s, %(address)s,
                        %(good_type)s, %(amount)s, %(good_description)s, %(claim_type)s, %(claim_detail)s, %(consumer_request)s
                    )
                """
                cursor.execute(sql, data)
                conn.commit()
            conn.close()
            flash('Reclamo enviado. En menos de 3 días solucionaremos el problema.', 'success')
            return redirect(url_for('complaints'))
        except Exception as e:
            flash(f'Error al enviar reclamo: {str(e)}', 'error')
            
    return render_template('complaints.html')

@app.route('/admision', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        try:
            # Extract form data
            data = {
                'parent_name': request.form['parent_name'],
                'parent_lastname': request.form['parent_lastname'],
                'parent_doc_type': request.form['parent_doc_type'],
                'parent_doc_number': request.form['parent_doc_number'],
                'parent_phone': request.form['parent_phone'],
                'parent_email': request.form['parent_email'],
                'child_name': request.form['child_name'],
                'child_lastname': request.form['child_lastname'],
                'child_dob': request.form['child_dob'],
                'child_gender': request.form['child_gender'],
                'program_interest': request.form['program_interest'],
                'comments': request.form['comments']
            }
            
            # In a real app, you would save this to the DB
            # For now, just flash success
            flash('Solicitud de admisión enviada correctamente. Nos pondremos en contacto pronto.', 'success')
            return redirect(url_for('admission'))
        except Exception as e:
            flash(f'Error al enviar solicitud: {str(e)}', 'error')
            
    return render_template('admission.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)