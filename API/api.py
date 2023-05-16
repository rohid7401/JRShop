from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
db = pymysql.connect(
    host='localhost',
    user='username',
    password='password',
    database='database_name'
)

# Función para ejecutar los procedimientos almacenados en la base de datos
def execute_procedure(proc_name, args=None):
    cursor = db.cursor()
    if args:
        cursor.callproc(proc_name, args)
    else:
        cursor.callproc(proc_name)
    db.commit()
    result = cursor.fetchall()
    return result

# Obtener todos los usuarios
@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    result = execute_procedure('get_all_users')
    users = [{'id': row[0], 'name': row[1], 'email': row[2], 'shipping_address': row[3]} for row in result]
    return jsonify(users)

# Obtener un usuario por su ID
@app.route('/get_user_by_id', methods=['POST'])
def get_user_by_id():
    user_id = request.json['id']
    result = execute_procedure('get_user_by_id', (user_id,))
    user = result.fetchone()
    if user:
        user_data = {'id': user[0], 'name': user[1], 'email': user[2], 'shipping_address': user[3]}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404

# Insertar un nuevo usuario
@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    shipping_address = data['shipping_address']
    execute_procedure('insert_user', (name, email, password, shipping_address))
    return jsonify({'message': 'User created successfully'}), 201

# Actualizar un usuario existente
@app.route('/update_user', methods=['POST'])
def update_user():
    data = request.get_json()
    user_id = data['id']
    name = data['name']
    email = data['email']
    password = data['password']
    shipping_address = data['shipping_address']
    execute_procedure('update_user', (user_id, name, email, password, shipping_address))
    return jsonify({'message': 'User updated successfully'})

# Eliminar un usuario
@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.json['id']
    execute_procedure('delete_user', (user_id,))
    return jsonify({'message': 'User deleted successfully'})


#--------------------------------------------------------------

# Obtener todos los vendedores
@app.route('/get_all_sellers', methods=['GET'])
def get_all_sellers():
    result = execute_procedure('get_all_sellers')
    sellers = [{'id': row[0], 'name': row[1]} for row in result]
    return jsonify(sellers)

# Obtener un vendedor por su ID
@app.route('/get_seller_by_id', methods=['POST'])
def get_seller_by_id():
    seller_id = request.json['id']
    result = execute_procedure('get_seller_by_id', (seller_id,))
    seller = result.fetchone()
    if seller:
        seller_data = {'id': seller[0], 'name': seller[1]}
        return jsonify(seller_data)
    else:
        return jsonify({'message': 'Seller not found'}), 404

# Insertar un nuevo vendedor
@app.route('/insert_seller', methods=['POST'])
def insert_seller():
    data = request.get_json()
    name = data['name']
    execute_procedure('insert_seller', (name,))
    return jsonify({'message': 'Seller created successfully'}), 201

# Actualizar un vendedor existente
@app.route('/update_seller', methods=['POST'])
def update_seller():
    data = request.get_json()
    seller_id = data['id']
    name = data['name']
    execute_procedure('update_seller', (seller_id, name))
    return jsonify({'message': 'Seller updated successfully'})

# Eliminar un vendedor
@app.route('/delete_seller', methods=['POST'])
def delete_seller():
    seller_id = request.json['id']
    execute_procedure('delete_seller', (seller_id,))
    return jsonify({'message': 'Seller deleted successfully'})

#--------------------------------------------------------------

# Obtener todos los productos
@app.route('/get_all_products', methods=['GET'])
def get_all_products():
    result = execute_procedure('get_all_products')
    products = []
    for row in result:
        product_data = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'price': float(row[3]),
            'quantity': row[4],
            'vendor_id': row[5]
        }
        products.append(product_data)
    return jsonify(products)

# Obtener un producto por su ID
@app.route('/get_product_by_id', methods=['POST'])
def get_product_by_id():
    product_id = request.json['id']
    result = execute_procedure('get_product_by_id', (product_id,))
    product = result.fetchone()
    if product:
        product_data = {
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': float(product[3]),
            'quantity': product[4],
            'vendor_id': product[5]
        }
        return jsonify(product_data)
    else:
        return jsonify({'message': 'Product not found'}), 404

# Insertar un nuevo producto
@app.route('/insert_product', methods=['POST'])
def insert_product():
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']
    quantity = data['quantity']
    vendor_id = data['vendor_id']
    execute_procedure('insert_product', (name, description, price, quantity, vendor_id))
    return jsonify({'message': 'Product created successfully'}), 201

# Actualizar un producto existente
@app.route('/update_product', methods=['POST'])
def update_product():
    data = request.get_json()
    product_id = data['id']
    name = data['name']
    description = data['description']
    price = data['price']
    quantity = data['quantity']
    vendor_id = data['vendor_id']
    execute_procedure('update_product', (product_id, name, description, price, quantity, vendor_id))
    return jsonify({'message': 'Product updated successfully'})

# Eliminar un producto
@app.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.json['id']
    execute_procedure('delete_product', (product_id,))
    return jsonify({'message': 'Product deleted successfully'})

#--------------------------------------------------------------

# Obtener todas las órdenes
@app.route('/get_all_orders', methods=['GET'])
def get_all_orders():
    result = execute_procedure('get_all_orders')
    orders = []
    for row in result:
        order_data = {
            'id': row[0],
            'customer_name': row[1],
            'customer_email': row[2],
            'customer_phone': row[3],
            'shipping_address': row[4],
            'shipping_city': row[5],
            'shipping_zipcode': row[6],
            'shipping_country': row[7],
            'total_price': float(row[8]),
            'status': row[9],
            'vendor_id': row[10]
        }
        orders.append(order_data)
    return jsonify(orders)

# Obtener una orden por su ID
@app.route('/get_order_by_id', methods=['POST'])
def get_order_by_id():
    order_id = request.json['id']
    result = execute_procedure('get_order_by_id', (order_id,))
    order = result.fetchone()
    if order:
        order_data = {
            'id': order[0],
            'customer_name': order[1],
            'customer_email': order[2],
            'customer_phone': order[3],
            'shipping_address': order[4],
            'shipping_city': order[5],
            'shipping_zipcode': order[6],
            'shipping_country': order[7],
            'total_price': float(order[8]),
            'status': order[9],
            'vendor_id': order[10]
        }
        return jsonify(order_data)
    else:
        return jsonify({'message': 'Order not found'}), 404

# Insertar una nueva orden
@app.route('/insert_order', methods=['POST'])
def insert_order():
    data = request.get_json()
    customer_name = data['customer_name']
    customer_email = data['customer_email']
    customer_phone = data['customer_phone']
    shipping_address = data['shipping_address']
    shipping_city = data['shipping_city']
    shipping_zipcode = data['shipping_zipcode']
    shipping_country = data['shipping_country']
    total_price = data['total_price']
    status = data['status']
    vendor_id = data['vendor_id']
    execute_procedure('insert_order', (
        customer_name,
        customer_email,
        customer_phone,
        shipping_address,
        shipping_city,
        shipping_zipcode,
        shipping_country,
        total_price,
        status,
        vendor_id
    ))
    return jsonify({'message': 'Order created successfully'}), 201

# Actualizar una orden existente
@app.route('/update_order', methods=['POST'])
def update_order():
    data = request.get_json()
    order_id = data['id']
    customer_name = data['customer_name']
    customer_email = data['customer_email']
    customer_phone = data['customer_phone']
    shipping_address = data['shipping_address']
    shipping_city = data['shipping_city']
    shipping_zipcode = data['shipping_zipcode']
    shipping_country = data['shipping_country']
    total_price = data['total_price']
    status = data['status']
    vendor_id = data['vendor_id']
    execute_procedure('update_order', (
        order_id,
        customer_name,
        customer_email,
        customer_phone,
        shipping_address,
        shipping_city,
        shipping_zipcode,
        shipping_country,
        total_price,
        status,
        vendor_id
    ))
    return jsonify({'message': 'Order updated successfully'})

# Actualizar el estado de una orden
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.get_json()
    order_id = data['id']
    order_status = data['status']
    execute_procedure('update_order_status', (order_id, order_status))
    return jsonify({'message': 'Order status updated successfully'})

# Eliminar una orden
@app.route('/delete_order', methods=['POST'])
def delete_order():
    order_id = request.json['id']
    execute_procedure('delete_order', (order_id,))
    return jsonify({'message': 'Order deleted successfully'})

#--------------------------------------------------------------

# Obtener todos los elementos de orden
@app.route('/get_all_order_items', methods=['GET'])
def get_all_order_items():
    result = execute_procedure('get_all_order_items')
    order_items = []
    for row in result:
        order_item_data = {
            'id': row[0],
            'order_id': row[1],
            'product_id': row[2],
            'quantity': row[3],
            'price': float(row[4])
        }
        order_items.append(order_item_data)
    return jsonify(order_items)

# Obtener elementos de orden por ID de orden
@app.route('/get_order_items_by_order_id', methods=['POST'])
def get_order_items_by_order_id():
    order_id = request.json['id']
    result = execute_procedure('get_order_items_by_order_id', (order_id,))
    order_items = []
    for row in result:
        order_item_data = {
            'id': row[0],
            'order_id': row[1],
            'product_id': row[2],
            'quantity': row[3],
            'price': float(row[4])
        }
        order_items.append(order_item_data)
    return jsonify(order_items)

# Insertar un nuevo elemento de orden
@app.route('/insert_order_item', methods=['POST'])
def insert_order_item():
    data = request.get_json()
    order_id = data['order_id']
    product_id = data['product_id']
    quantity = data['quantity']
    price = data['price']
    execute_procedure('insert_order_item', (order_id, product_id, quantity, price))
    return jsonify({'message': 'Order item created successfully'}), 201

# Actualizar un elemento de orden existente
@app.route('/update_order_item', methods=['POST'])
def update_order_item():
    data = request.get_json()
    order_item_id = data['id']
    order_id = data['order_id']
    product_id = data['product_id']
    quantity = data['quantity']
    price = data['price']
    execute_procedure('update_order_item', (order_item_id, order_id, product_id, quantity, price))
    return jsonify({'message': 'Order item updated successfully'})

# Eliminar un elemento de orden
@app.route('/delete_order_item', methods=['POST'])
def delete_order_item():
    order_item_id = request.json['id']
    execute_procedure('delete_order_item', (order_item_id,))
    return jsonify({'message': 'Order item deleted successfully'})

#--------------------------------------------------------------

if __name__ == '__main__':
    app.run()
