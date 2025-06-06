from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from extensions import db
from models.usuario import Usuario
from datetime import date

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# ----------------------------
# API JSON: Listar todos los usuarios
# ----------------------------
@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'fecha_registro': u.fecha_registro.isoformat()
    } for u in usuarios])

# ----------------------------
# API JSON: Obtener usuario por ID
# ----------------------------
@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email,
        'fecha_registro': usuario.fecha_registro.isoformat()
    })

# ----------------------------
# HTML: Listar usuarios con filtros
# ----------------------------
@usuarios_bp.route('/gestionar', methods=['GET'])
def gestionar_usuarios():
    nombre = request.args.get('nombre')
    email = request.args.get('email')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = Usuario.query

    if nombre:
        query = query.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if email:
        query = query.filter(Usuario.email.ilike(f"%{email}%"))
    if fecha_inicio:
        query = query.filter(Usuario.fecha_registro >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Usuario.fecha_registro <= fecha_fin)

    usuarios = query.all()
    return render_template('reportes/usuarios.html', usuarios=usuarios, editar=False, usuario=None)

# ----------------------------
# HTML: Mostrar formulario de edición
# ----------------------------
@usuarios_bp.route('/editar/<int:id>', methods=['GET'])
def editar_usuario_html(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('reportes/usuarios.html', usuarios=[], editar=True, usuario=usuario)

# ----------------------------
# HTML: Crear nuevo usuario
# ----------------------------
@usuarios_bp.route('/crear', methods=['POST'])
def crear_usuario_html():
    try:
        id_manual = request.form.get('id')
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        fecha_str = request.form.get('fecha_registro')
        fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()

        if id_manual:
            id_manual = int(id_manual)
            if Usuario.query.get(id_manual):
                return f"Error: Ya existe un usuario con ID {id_manual}", 400
            nuevo = Usuario(id=id_manual, nombre=nombre, email=email, contrasena=contrasena, fecha_registro=fecha)
        else:
            nuevo = Usuario(nombre=nombre, email=email, contrasena=contrasena, fecha_registro=fecha)

        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('usuarios.gestionar_usuarios'))

    except Exception as e:
        db.session.rollback()
        return f"Error al crear el usuario: {str(e)}", 500

# ----------------------------
# HTML: Editar usuario existente
# ----------------------------
@usuarios_bp.route('/editar/<int:id>', methods=['POST'])
def actualizar_usuario_html(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']

        contrasena = request.form.get('contrasena')
        if contrasena:
            usuario.contrasena = contrasena

        fecha_str = request.form.get('fecha_registro')
        if fecha_str:
            usuario.fecha_registro = date.fromisoformat(fecha_str)

        db.session.commit()
        return redirect(url_for('usuarios.gestionar_usuarios'))
    except Exception as e:
        db.session.rollback()
        return f"Error al editar el usuario: {str(e)}", 500

# ----------------------------
# HTML: Eliminar usuario
# ----------------------------
@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario_html(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('usuarios.gestionar_usuarios'))
    except Exception as e:
        db.session.rollback()
        return f"Error al eliminar el usuario: {str(e)}", 500