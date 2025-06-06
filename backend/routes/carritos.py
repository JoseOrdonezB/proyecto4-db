from flask import Blueprint, request, jsonify
from extensions import db
from models.carrito import Carrito, CarritoProducto
from models.usuario import Usuario
from models.producto import Producto

carritos_bp = Blueprint('carritos', __name__, url_prefix='/carritos')

# Obtener todos los carritos
@carritos_bp.route('/', methods=['GET'])
def listar_carritos():
    carritos = Carrito.query.all()
    return jsonify([{
        'id': c.id,
        'usuario_id': c.usuario_id,
        'fecha_creacion': c.fecha_creacion.isoformat()
    } for c in carritos])

# Obtener un carrito con sus productos
@carritos_bp.route('/<int:id>', methods=['GET'])
def obtener_carrito(id):
    carrito = Carrito.query.get_or_404(id)
    productos = [{
        'producto_id': cp.producto_id,
        'nombre': cp.producto.nombre,
        'cantidad': cp.cantidad
    } for cp in carrito.productos]
    
    return jsonify({
        'id': carrito.id,
        'usuario_id': carrito.usuario_id,
        'fecha_creacion': carrito.fecha_creacion.isoformat(),
        'productos': productos
    })

# Crear un nuevo carrito
@carritos_bp.route('/', methods=['POST'])
def crear_carrito():
    data = request.json
    nuevo = Carrito(
        usuario_id=data['usuario_id'],
        fecha_creacion=data.get('fecha_creacion')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Carrito creado', 'id': nuevo.id}), 201

# Agregar producto a un carrito
@carritos_bp.route('/<int:carrito_id>/agregar', methods=['POST'])
def agregar_producto(carrito_id):
    data = request.json
    item = CarritoProducto.query.get((carrito_id, data['producto_id']))
    if item:
        item.cantidad += data['cantidad']
    else:
        item = CarritoProducto(
            carrito_id=carrito_id,
            producto_id=data['producto_id'],
            cantidad=data['cantidad']
        )
        db.session.add(item)
    db.session.commit()
    return jsonify({'mensaje': 'Producto agregado al carrito'})

# Eliminar producto del carrito
@carritos_bp.route('/<int:carrito_id>/eliminar/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(carrito_id, producto_id):
    item = CarritoProducto.query.get_or_404((carrito_id, producto_id))
    db.session.delete(item)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado del carrito'})