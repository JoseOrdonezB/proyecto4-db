from flask import Blueprint, request, jsonify
from extensions import db
from models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Listar todos los usuarios
@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'fecha_registro': u.fecha_registro.isoformat()
    } for u in usuarios])

# Obtener un usuario por ID
@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'fecha_registro': usuario.fecha_registro.isoformat()
    })

# Crear un nuevo usuario
@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        contrasena=data['contrasena'],
        fecha_registro=data['fecha_registro']  # formato 'YYYY-MM-DD'
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado', 'id': nuevo_usuario.id}), 201

# Actualizar usuario
@usuarios_bp.route('/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.email = data.get('email', usuario.email)
    usuario.contrasena = data.get('contrasena', usuario.contrasena)
    usuario.fecha_registro = data.get('fecha_registro', usuario.fecha_registro)

    db.session.commit()
    return jsonify({'mensaje': 'Usuario actualizado'})

# Eliminar usuario
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado'})