from flask import Blueprint, request, jsonify
from extensions import db
from models.pedido import Pedido, DetallePedido
from models.producto import Producto

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

# Listar todos los pedidos
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

# Obtener un pedido con sus detalles
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

# Crear un nuevo pedido con detalles
@pedidos_bp.route('/', methods=['POST'])
def crear_pedido():
    data = request.json
    detalles = data.get('detalles', [])
    if not detalles:
        return jsonify({'error': 'Debe incluir detalles del pedido'}), 400

    total = sum(d['cantidad'] * d['precio_unitario'] for d in detalles)

    nuevo = Pedido(
        usuario_id=data['usuario_id'],
        total=total,
        fecha=data.get('fecha'),  # o puedes usar datetime.date.today()
        estado=data['estado']
    )
    db.session.add(nuevo)
    db.session.flush()  # Obtener ID sin commit completo aún

    for d in detalles:
        detalle = DetallePedido(
            pedido_id=nuevo.id,
            producto_id=d['producto_id'],
            cantidad=d['cantidad'],
            precio_unitario=d['precio_unitario']
        )
        db.session.add(detalle)

    db.session.commit()
    return jsonify({'mensaje': 'Pedido creado', 'id': nuevo.id}), 201