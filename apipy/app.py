from flask import Flask, jsonify, request
from db import obtener_conexion

app = Flask(__name__)
@app.route('/')
def inicio():
    return jsonify({'mensaje': 'Bienvenido a la API de Taller de Grado'})

@app.route('/docentes', methods=['GET'])
def obtener_docentes():
    conexion = obtener_conexion()
    docentes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM docentes")
        docentes = cursor.fetchall()
    conexion.close()
    return jsonify(docentes)

@app.route('/login', methods=['POST'])
def login():
    # Obtener datos del formulario
    datos_usuario = request.json
    email = datos_usuario.get('email')
    password = datos_usuario.get('password')

    conexion = obtener_conexion()
    usuario = None
    tipo_usuario = None
    
    # Consultar en la tabla de Estudiantes
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM estudiantes WHERE correo = %s AND contrasena = %s", (email, password))
        usuario = cursor.fetchone()
        if usuario:
            tipo_usuario = 'estudiante'
    
    # Si no encontró en Estudiantes, consultar en Docentes
    if not usuario:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM docentes WHERE correo = %s AND contrasena = %s", (email, password))
            usuario = cursor.fetchone()
            if usuario:
                tipo_usuario = 'docente'
    
    # Si no encontró en Docentes, consultar en Coordinadores
    if not usuario:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM coordinadores WHERE correo = %s AND contrasena = %s", (email, password))
            usuario = cursor.fetchone()
            if usuario:
                tipo_usuario = 'coordinador'
    
    # Si no encontró en Coordinadores, consultar en Directores
    if not usuario:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM directores WHERE correo = %s AND contrasena = %s", (email, password))
            usuario = cursor.fetchone()
            if usuario:
                tipo_usuario = 'director'

    conexion.close()
    
    
    if not usuario:
        return jsonify({'mensaje': 'Correo o contraseña incorrectos'}), 401
    
    
    return jsonify({'mensaje': 'Inicio de sesión exitoso', 'tipo_usuario': tipo_usuario}), 200



@app.route('/category', methods=['POST'])
def agregar_categoria():
    nueva_categoria = request.json
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO category (name, last_update, isDeleted) VALUES (%s, NOW(), 0)", (nueva_categoria['name'],))
        conexion.commit()
    conexion.close()
    return jsonify({'mensaje': 'Categoría agregada'}), 201

@app.route('/category/<int:id>', methods=['PATCH'])
def actualizar_categoria(id):
    datos_categoria = request.json
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE category SET name = %s, last_update = NOW() WHERE category_id = %s AND isDeleted = 0", (datos_categoria['name'], id))
        conexion.commit()
    conexion.close()
    return jsonify({'mensaje': 'Categoría actualizada'})

@app.route('/category/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE category SET isDeleted = 1, last_update = NOW() WHERE category_id = %s", (id,))
        conexion.commit()
    conexion.close()
    return jsonify({'mensaje': 'Categoría eliminada'})

if __name__ == '__main__':
    app.run(debug=True)
