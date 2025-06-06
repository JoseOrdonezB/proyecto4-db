from flask import Blueprint, jsonify
from models.vista_usuarios_roles import VistaUsuariosRoles
from models.vista_productos_detalle import VistaProductoDetalle
from models.vista_pedidos_completos import VistaPedidosCompletos

vistas_bp = Blueprint('vistas', __name__, url_prefix='/vistas')

# Vista: usuarios con roles
@vistas_bp.route('/usuarios_roles', methods=['GET'])
def vista_usuarios_roles():
    datos = VistaUsuariosRoles.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'fecha_registro': u.fecha_registro.isoformat(),
        'roles': u.roles
    } for u in datos])

# Vista: productos con proveedores y categorías
@vistas_bp.route('/productos_detalle', methods=['GET'])
def vista_productos_detalle():
    datos = VistaProductoDetalle.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'precio': float(p.precio),
        'stock': p.stock,
        'estado': p.estado,
        'categorias': p.categorias,
        'proveedores': p.proveedores
    } for p in datos])

# Vista: pedidos con info de usuario
@vistas_bp.route('/pedidos_completos', methods=['GET'])
def vista_pedidos_completos():
    datos = VistaPedidosCompletos.query.all()
    return jsonify([{
        'pedido_id': d.pedido_id,
        'cliente': d.cliente,
        'email': d.email,
        'total': float(d.total),
        'fecha': d.fecha.isoformat(),
        'estado': d.estado
    } for d in datos])