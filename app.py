import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session,flash
import pymysql
from config import Config
from bcrypt import hashpw, checkpw, gensalt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "supersecretkey"  # Necesario para manejar sesiones

# Configuración para la carga de archivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear el directorio de carga si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conexión a la base de datos
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=app.config["DB_HOST"],
            user=app.config["DB_USER"],
            password=app.config["DB_PASSWORD"],
            database=app.config["DB_NAME"],
            port=app.config["DB_PORT"],
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
@app.context_processor
def inject_footer_data():
    """Inyecta los datos de la empresa y redes sociales en todas las plantillas."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Información de la compañía
            cursor.execute("""
                SELECT name, description, address, phone_number, email
                FROM info_companies
                WHERE id = 1
            """)
            company_info = cursor.fetchone()

            # Redes sociales
            cursor.execute("""
                SELECT network_name, network_url
                FROM company_social_networks
            """)
            social_networks = cursor.fetchall()
    finally:
        conn.close()

    # Asegúrate de manejar el caso en que los datos no estén disponibles
    return {
        "company_info": company_info or {},
        "social_networks": social_networks or [],
    }


# Ruta principal (home) que muestra los productos y permite buscar
@app.route("/")
def home():
    query = request.args.get("query", "").strip()  # Recupera el término de búsqueda de la URL
    category = request.args.get("category")  # Recupera la categoría seleccionada
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cursor:
            # Consulta para recuperar productos
            if query or category:
                sql = """
                    SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category, p.image_url
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                    WHERE 1=1
                """
                params = []
                if query:
                    sql += " AND (p.name LIKE %s OR p.description LIKE %s)"
                    params.extend([f"%{query}%", f"%{query}%"])
                if category:
                    sql += " AND c.id = %s"
                    params.append(category)
                
                cursor.execute(sql, params)
            else:
                cursor.execute("""
                    SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category, p.image_url
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                """)
            
            products = cursor.fetchall()

            # Consulta para recuperar categorías
            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
    finally:
        conn.close()
    
    # Recupera el usuario activo
    username = session.get("username", "Invitado")
    
    # Modificamos la información de los productos para incluir el estado de stock
    for product in products:
        product['out_of_stock'] = product['stock'] == 0  # Marcar los productos sin stock como agotados

    return render_template("cliente/index.html", products=products, categories=categories, username=username, query=query)



# Ruta para registro de usuarios
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        allowed_domains = ["@gmail.com", "@tienda.com"]
        if not any(email.endswith(domain) for domain in allowed_domains):
            return render_template("cliente/register.html", error="Solo se permiten correos de Google")
        
        # Asignar rol
        role = "admin" if email == "admin@tienda.com" else "customer"

        # Cifrar la contraseña
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                    (username, email, hashed_password, role)
                )
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error al insertar en la base de datos: {e}")
            return render_template("cliente/register.html", error="Error al registrar el usuario.")
        finally:
            conn.close()
        return redirect(url_for("login"))
    return render_template("cliente/register.html")

# Ruta para inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, role, password FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
        conn.close()

        if user and checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("home"))
        else:
            return render_template("cliente/login.html", error="Credenciales inválidas.")
    return render_template("cliente/login.html")

# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Ruta para el panel de administración
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("home"))
    return render_template("admin/dashboard.html", username=session.get("username"))

# Ruta para gestionar productos
@app.route("/manage_products", methods=["GET", "POST"])
def manage_products():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                if 'add_product' in request.form:
                    # Agregar nuevo producto
                    name = request.form["name"]
                    description = request.form["description"]
                    price = request.form["price"]
                    stock = request.form["stock"]
                    category_id = request.form["category_id"]
                    image = request.files["image"]

                    if image and allowed_file(image.filename):
                        filename = secure_filename(image.filename)
                        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    else:
                        image_url = None

                    cursor.execute("""
                        INSERT INTO products (name, description, price, stock, category_id, image_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (name, description, price, stock, category_id, image_url))
                    conn.commit()
                elif 'add_category' in request.form:
                    # Agregar nueva categoría
                    category_name = request.form["category_name"]
                    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                    conn.commit()
                return redirect(url_for("manage_products"))

            # Obtener productos y categorías
            cursor.execute("""
                SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category, p.image_url
                FROM products p
                JOIN categories c ON p.category_id = c.id
            """)
            products = cursor.fetchall()

            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
    finally:
        conn.close()

    return render_template("admin/manage_products.html", products=products, categories=categories, username=session.get("username"))

# Ruta para eliminar producto
@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for("manage_products"))

# Ruta para editar producto
@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                name = request.form["name"]
                description = request.form["description"]
                price = request.form["price"]
                stock = request.form["stock"]
                category_id = request.form["category_id"]
                image = request.files["image"]

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                else:
                    image_url = request.form["existing_image_url"]

                cursor.execute("""
                    UPDATE products
                    SET name = %s, description = %s, price = %s, stock = %s, category_id = %s, image_url = %s
                    WHERE id = %s
                """, (name, description, price, stock, category_id, image_url, product_id))
                conn.commit()
                return redirect(url_for("manage_products"))
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()

            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
    finally:
        conn.close()

    return render_template("admin/edit_product.html", product=product, categories=categories, username=session.get("username"))

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    category = request.args.get("category")  # Recupera la categoría seleccionada
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.id, p.name, p.description, p.price, p.stock, c.name AS category, p.image_url
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE 1=1
            """
            params = []
            if query:
                sql += " AND (p.name LIKE %s OR p.description LIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])
            if category:
                sql += " AND c.id = %s"
                params.append(category)
            
            cursor.execute(sql, params)
            products = cursor.fetchall()
    finally:
        conn.close()
    
    # Devuelve los resultados como JSON
    return jsonify(products)

@app.route("/about", methods=["GET", "POST"])
def about():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST" and session.get("role") == "admin":
                # Recuperar datos del formulario
                title = request.form["title"]
                description = request.form["description"]
                image = request.files["image"]

                # Manejar la carga de la imagen
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_url = f"uploads/{filename}"
                else:
                    image_url = request.form.get("existing_image_url", None)

                # Línea de depuración
                print(f"Image URL: {image_url}")
                print(f"File exists: {os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))}")

                # Actualizar la información existente
                cursor.execute("""
                    UPDATE quienes_somos
                    SET title = %s, description = %s, image_url = %s
                """, (title, description, image_url))
                conn.commit()
                return redirect(url_for("about"))

            # Recuperar la información actual
            cursor.execute("SELECT * FROM quienes_somos LIMIT 1")
            about_info = cursor.fetchone()

    finally:
        conn.close()                   

    if session.get("role") == "admin":
        return render_template("admin/admin_about_us.html", about_info=about_info,  username=session.get("username"))
    else:
        return render_template("cliente/quienes_somos.html", about_info=about_info, username=session.get("username"))
    
    
# Ruta para agregar un producto al carrito
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    if not session.get("user_id"):
        return jsonify({"message": "Debes iniciar sesión para agregar productos al carrito"}), 401

    user_id = session.get("user_id")
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Verificar si el producto ya está en el carrito
            cursor.execute("""
                SELECT id, quantity FROM cart
                WHERE user_id = %s AND product_id = %s
            """, (user_id, product_id))
            cart_item = cursor.fetchone()

            if cart_item:
                # Si el producto ya está en el carrito, incrementar la cantidad
                new_quantity = cart_item['quantity'] + quantity
                cursor.execute("""
                    UPDATE cart
                    SET quantity = %s
                    WHERE id = %s
                """, (new_quantity, cart_item['id']))
            else:
                # Si el producto no está en el carrito, agregar una nueva entrada
                cursor.execute("""
                    INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (user_id, product_id, quantity))
            conn.commit()
    except Exception as e:
        return jsonify({"message": "Error al agregar al carrito", "error": str(e)}), 500
    finally:
        conn.close()

    # Actualizar el carrito en la sesión
    session.modified = True
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({
        'product_id': product_id,
        'quantity': quantity,
        'price': data.get('price')  # Asegúrate de pasar el precio también
    })

    return jsonify({"message": "Producto agregado al carrito exitosamente"})

# Ruta para ver los productos en el carrito
@app.route("/cart", methods=["GET"])
def view_cart():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, p.name, p.description, p.image_url, p.price, c.quantity, c.added_at
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """, (user_id,))
            cart_items = cursor.fetchall()
            total = sum(item['price'] * item['quantity'] for item in cart_items)
    except Exception as e:
        return render_template("cliente/cart.html", cart_items=[], total=0, error=str(e))
    finally:
        conn.close()

    return render_template("cliente/cart.html", cart_items=cart_items, total=total)

#Ruta para actualizar la cantidad en el carrito
@app.route("/cart/update/<int:id>", methods=["POST"])
def update_cart(id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    quantity = request.form["quantity"]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE cart
                SET quantity = %s
                WHERE id = %s AND user_id = %s
            """, (quantity, id, user_id))
            conn.commit()
    except Exception as e:
        return redirect(url_for("view_cart", error=str(e)))
    finally:
        conn.close()

    return redirect(url_for("view_cart"))

# Ruta para eliminar un producto del carrito
@app.route("/cart/remove/<int:id>", methods=["POST"])
def remove_from_cart(id):
    if not session.get("user_id"):
        return jsonify({"message": "Debes iniciar sesión para eliminar productos del carrito"}), 401

    user_id = session.get("user_id")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM cart
                WHERE id = %s AND user_id = %s
            """, (id, user_id))
            conn.commit()
    except Exception as e:
        return jsonify({"message": "Error al eliminar del carrito", "error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"message": "Producto eliminado del carrito exitosamente"})

# Mostrar logo
@app.route("/logos", methods=["GET"])
def get_logos():
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # Usar DictCursor para obtener resultados como diccionarios
            cursor.execute("SELECT id, name, image_url FROM logos")
            logos = cursor.fetchall()
        
        return jsonify(logos), 200
    except pymysql.MySQLError as e:
        print(f"Error al obtener los logos: {e}")
        return jsonify({"error": f"Error al obtener los logos: {e}"}), 500
    finally:
        conn.close()


# Actualizar logo
@app.route("/admin/logos", methods=["GET", "POST"])
def admin_logos():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))  # Redirigir al login si no está autenticado o no es admin
    
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:  # Usar DictCursor para obtener resultados como diccionarios
            if request.method == "POST":
                # Recuperar datos del formulario
                name = request.form["name"]
                image = request.files["image"]

                # Manejar la carga de la imagen
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_url = f"uploads/{filename}"
                else:
                    image_url = request.form.get("existing_image_url", None)

                # Verificar si ya existe una fila en la tabla
                cursor.execute("SELECT COUNT(*) AS count FROM logos")
                count = cursor.fetchone()["count"]

                if count == 0:
                    # Insertar una nueva fila si no existe ninguna
                    cursor.execute("""
                        INSERT INTO logos (name, image_url)
                        VALUES (%s, %s)
                    """, (name, image_url))
                else:
                    # Actualizar la información existente
                    cursor.execute("""
                        UPDATE logos
                        SET name = %s, image_url = %s
                        WHERE id = %s
                    """, (name, image_url, 1))  # Asumiendo que solo hay un logo con ID 1

                conn.commit()
                return redirect(url_for("admin_logos"))

            # Recuperar la información actual
            cursor.execute("SELECT * FROM logos LIMIT 1")
            logo_info = cursor.fetchone()

    finally:
        conn.close()

    return render_template("admin/logos.html", logo_info=logo_info)

@app.route("/create_order", methods=["GET", "POST"])
def create_order():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        delivery_date = request.form["delivery_date"]
        delivery_location = request.form["delivery_location"]
        customer_name = request.form["customer_name"]
        customer_phone = request.form["customer_phone"]
        delivery_time = request.form["delivery_time"]
        observation = request.form["observation"]
        payment_method = request.form["payment_method"]
        payment_type = request.form["payment_type"]

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Crear la orden
                cursor.execute("""
                    INSERT INTO orders (delivery_date, delivery_location, customer_name, customer_phone, delivery_time, observation, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (delivery_date, delivery_location, customer_name, customer_phone, delivery_time, observation))
                order_id = cursor.lastrowid

                # Obtener productos del carrito
                cursor.execute("""
                    SELECT product_id, quantity
                    FROM cart
                    WHERE user_id = %s
                """, (user_id,))
                cart_items = cursor.fetchall()

                # Insertar productos en la orden y descontar stock
                for item in cart_items:
                    product_id = item["product_id"]
                    quantity = item["quantity"]

                    cursor.execute("""
                        INSERT INTO order_items (order_id, product_id, quantity)
                        VALUES (%s, %s, %s)
                    """, (order_id, product_id, quantity))

                    cursor.execute("""
                        UPDATE products
                        SET stock = stock - %s
                        WHERE id = %s
                    """, (quantity, product_id))

                # Crear el método de pago
                cursor.execute("""
                    INSERT INTO payment_system (order_id, payment_method, payment_type, created_at)
                    VALUES (%s, %s, %s, NOW())
                """, (order_id, payment_method, payment_type))

                # Vaciar el carrito
                cursor.execute("""
                    DELETE FROM cart
                    WHERE user_id = %s
                """, (user_id,))
                conn.commit()
        finally:
            conn.close()
        return redirect(url_for("order_confirmation", order_id=order_id))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, p.name, p.price, c.quantity
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """, (user_id,))
            cart_items = cursor.fetchall()
    finally:
        conn.close()

    return render_template("cliente/create_order.html", cart_items=cart_items)

@app.route("/order_confirmation/<int:order_id>", methods=["GET"])
def order_confirmation(order_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT o.id, o.delivery_date, o.delivery_location, o.customer_name, o.customer_phone, o.delivery_time, o.observation, o.created_at, ps.payment_method, ps.payment_type
                FROM orders o
                JOIN payment_system ps ON o.id = ps.order_id
                WHERE o.id = %s
            """, (order_id,))
            order = cursor.fetchone()

            cursor.execute("""
                SELECT oi.product_id, p.name, oi.quantity
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
            """, (order_id,))
            order_items = cursor.fetchall()
    finally:
        conn.close()

    return render_template("cliente/order_confirmation.html", order=order, order_items=order_items)

# ver orden
@app.route("/view_orders", methods=["GET"])
def view_orders():
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT o.id, o.delivery_date, o.delivery_location, o.customer_name, o.customer_phone, o.delivery_time, o.observation, o.created_at, ps.payment_method, ps.payment_type
                FROM orders o
                JOIN payment_system ps ON o.id = ps.order_id
            """)
            orders = cursor.fetchall()

            # Obtener los productos de cada orden
            order_details = {}
            for order in orders:
                cursor.execute("""
                    SELECT oi.product_id, p.name, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """, (order["id"],))
                order_details[order["id"]] = cursor.fetchall()
    finally:
        conn.close()

    return render_template("admin/view_orders.html", orders=orders, order_details=order_details)

#Ruta para mostrar las redes sociales
@app.route("/update_social_networks", methods=["GET", "POST"])
def update_social_networks():
    """Ruta para mostrar y agregar redes sociales."""
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, network_name, network_url
                FROM company_social_networks
            """)
            social_networks = cursor.fetchall()
    finally:
        conn.close()

    return render_template("admin/update_social_networks.html", social_networks=social_networks)


@app.route("/add_social_network", methods=["POST"])
def add_social_network():
    """Ruta para agregar una nueva red social."""
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    network_name = request.form["network_name"]
    network_url = request.form["network_url"]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO company_social_networks (network_name, network_url)
                VALUES (%s, %s)
            """, (network_name, network_url))
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for("update_social_networks"))


@app.route("/edit_social_network/<int:network_id>", methods=["POST"])
def edit_social_network(network_id):
    """Ruta para editar una red social existente."""
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    network_name = request.form["network_name"]
    network_url = request.form["network_url"]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE company_social_networks
                SET network_name = %s, network_url = %s
                WHERE id = %s
            """, (network_name, network_url, network_id))
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for("update_social_networks"))

@app.route("/update_company_info", methods=["GET", "POST"])
def update_company_info():
    """Ruta para actualizar la información de la compañía."""
    if session.get("role") != "admin":
        return redirect(url_for("home"))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                name = request.form["name"]
                description = request.form["description"]
                address = request.form["address"]
                phone_number = request.form["phone_number"]
                email = request.form["email"]

                cursor.execute("""
                    UPDATE info_companies
                    SET name = %s, description = %s, address = %s, phone_number = %s, email = %s, updated_at = NOW()
                    WHERE id = 1
                """, (name, description, address, phone_number, email))
                conn.commit()
                return redirect(url_for("update_company_info"))

            cursor.execute("""
                SELECT name, description, address, phone_number, email
                FROM info_companies
                WHERE id = 1
            """)
            company_info = cursor.fetchone()
    finally:
        conn.close()

    return render_template("admin/update_company_info.html", company_info=company_info)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=Config.DEBUG)