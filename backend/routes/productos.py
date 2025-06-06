from flask import Blueprint, request, jsonify
from extensions import db
from models.producto import Producto

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

# Listar todos los productos
@productos_bp.route('/', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'descripcion': p.descripcion,
        'precio': float(p.precio),
        'stock': p.stock,
        'sku': p.sku,
        'estado': p.estado
    } for p in productos])

# Obtener un producto por ID
@productos_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio': float(producto.precio),
        'stock': producto.stock,
        'sku': producto.sku,
        'estado': producto.estado
    })

# Crear un nuevo producto
@productos_bp.route('/', methods=['POST'])
def crear_producto():
    data = request.json
    nuevo = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=data['precio'],
        stock=data['stock'],
        sku=data['sku'],
        estado=data.get('estado', 'activo')  # por defecto 'activo'
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Producto creado', 'id': nuevo.id}), 201

# Actualizar un producto existente
@productos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.json

    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.sku = data.get('sku', producto.sku)
    producto.estado = data.get('estado', producto.estado)

    db.session.commit()
    return jsonify({'mensaje': 'Producto actualizado'})

# Eliminar un producto
@productos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado'})