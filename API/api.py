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

if __name__ == '__main__':
    app.run()
