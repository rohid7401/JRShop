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

# Función para ejecutar consultas SQL
def execute_query(query, params=None):
    cursor = db.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    db.commit()
    return cursor

# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    query = "SELECT * FROM users"
    result = execute_query(query)
    users = [{'id': row[0], 'name': row[1], 'email': row[2], 'shipping_address': row[3]} for row in result]
    return jsonify(users)

# Obtener un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    result = execute_query(query, (user_id,))
    user = result.fetchone()
    if user:
        user_data = {'id': user[0], 'name': user[1], 'email': user[2], 'shipping_address': user[3]}
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'}), 404

# Insertar un nuevo usuario
@app.route('/users', methods=['POST'])
def insert_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    shipping_address = data['shipping_address']
    query = "INSERT INTO users (name, email, password, shipping_address) VALUES (%s, %s, %s, %s)"
    execute_query(query, (name, email, password, shipping_address))
    return jsonify({'message': 'User created successfully'}), 201

# Actualizar un usuario existente
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    shipping_address = data['shipping_address']
    query = "UPDATE users SET name = %s, email = %s, password = %s, shipping_address = %s WHERE id = %s"
    execute_query(query, (name, email, password, shipping_address, user_id))
    return jsonify({'message': 'User updated successfully'})

# Eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %s"
    execute_query(query, (user_id,))
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run()
