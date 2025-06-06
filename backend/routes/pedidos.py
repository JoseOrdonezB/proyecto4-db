from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from extensions import db
from models.pedido import Pedido, DetallePedido
from models.usuario import Usuario
from models.vista_pedidos_completos import VistaPedidosCompletos
from datetime import date

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')


# ----------------------------
# API JSON: Obtener todos los pedidos
# ----------------------------
@pedidos_bp.route('/', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([{
        'id': p.id,
        'usuario_id': p.usuario_id,
        'total': float(p.total),
        'fecha': p.fecha.isoformat(),
        'estado': p.estado
    } for p in pedidos])


# ----------------------------
# API JSON: Obtener detalles de un pedido
# ----------------------------
@pedidos_bp.route('/<int:id>', methods=['GET'])
def obtener_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    detalles = [{
        'producto_id': d.producto_id,
        'nombre': d.producto.nombre,
        'cantidad': d.cantidad,
        'precio_unitario': float(d.precio_unitario)
    } for d in pedido.detalles]

    return jsonify({
        'id': pedido.id,
        'usuario_id': pedido.usuario_id,
        'total': float(pedido.total),
        'fecha': pedido.fecha.isoformat(),
        'estado': pedido.estado,
        'detalles': detalles
    })


# ----------------------------
# HTML: Listar pedidos con filtros
# ----------------------------
@pedidos_bp.route('/gestionar', methods=['GET'])
def listar_pedidos_html():
    cliente = request.args.get('cliente')
    email = request.args.get('email')
    estado = request.args.get('estado')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = VistaPedidosCompletos.query

    if cliente:
        query = query.filter(VistaPedidosCompletos.cliente.ilike(f"%{cliente}%"))
    if email:
        query = query.filter(VistaPedidosCompletos.email.ilike(f"%{email}%"))
    if estado:
        query = query.filter(VistaPedidosCompletos.estado == estado)
    if fecha_inicio:
        query = query.filter(VistaPedidosCompletos.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(VistaPedidosCompletos.fecha <= fecha_fin)

    pedidos = query.all()
    return render_template('reportes/pedidos.html', pedidos=pedidos, editar=False)


# ----------------------------
# HTML: Mostrar formulario de edición
# ----------------------------
@pedidos_bp.route('/editar/<int:id>', methods=['GET'])
def editar_pedido_html(id):
    pedido = Pedido.query.get_or_404(id)
    return render_template('reportes/pedidos.html', pedidos=[], editar=True, pedido=pedido)


# ----------------------------
# HTML: Crear nuevo pedido (requiere usuario existente y ID libre si se indica)
# ----------------------------
@pedidos_bp.route('/crear', methods=['POST'])
def crear_pedido():
    try:
        id_manual = request.form.get('id')  # Puede venir vacío
        nombre = request.form['cliente']
        correo = request.form['correo']
        estado = request.form['estado']
        fecha_str = request.form.get('fecha')
        total = float(request.form.get('total', 0))
        fecha = date.fromisoformat(fecha_str) if fecha_str else date.today()

        # Verificar que el usuario exista
        usuario = Usuario.query.filter_by(nombre=nombre, email=correo).first()
        if not usuario:
            return "Error: Usuario no encontrado con ese nombre y correo", 400

        # Si se especificó ID manual, verificar que no exista ya
        if id_manual:
            id_manual = int(id_manual)
            if Pedido.query.get(id_manual):
                return f"Error: Ya existe un pedido con ID {id_manual}", 400
            nuevo = Pedido(id=id_manual, usuario_id=usuario.id, estado=estado, fecha=fecha, total=total)
        else:
            nuevo = Pedido(usuario_id=usuario.id, estado=estado, fecha=fecha, total=total)

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('pedidos.listar_pedidos_html'))

    except Exception as e:
        db.session.rollback()
        return f"Error al crear el pedido: {str(e)}", 500


# ----------------------------
# HTML: Editar pedido existente
# ----------------------------
@pedidos_bp.route('/editar/<int:id>', methods=['POST'])
def editar_pedido(id):
    try:
        pedido = Pedido.query.get_or_404(id)
        pedido.estado = request.form['estado']
        fecha_str = request.form.get('fecha')
        pedido.fecha = date.fromisoformat(fecha_str) if fecha_str else pedido.fecha
        pedido.total = float(request.form.get('total', pedido.total))
        db.session.commit()
        return redirect(url_for('pedidos.listar_pedidos_html'))
    except Exception as e:
        db.session.rollback()
        return f"Error al editar el pedido: {str(e)}", 500


# ----------------------------
# HTML: Eliminar pedido
# ----------------------------
@pedidos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_pedido(id):
    try:
        pedido = Pedido.query.get_or_404(id)
        db.session.delete(pedido)
        db.session.commit()
        return redirect(url_for('pedidos.listar_pedidos_html'))
    except Exception as e:
        db.session.rollback()
        return f"Error al eliminar el pedido: {str(e)}", 500