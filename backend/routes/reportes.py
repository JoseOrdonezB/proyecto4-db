from flask import Blueprint, render_template, request
from models import VistaProductoDetalle, VistaUsuariosRoles, VistaPedidosCompletos
from extensions import db

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

# --------------------
# REPORTE: PRODUCTOS
# --------------------
@reportes_bp.route('/productos')
def reporte_productos():
    nombre = request.args.get('nombre')
    estado = request.args.get('estado')
    categoria = request.args.get('categoria')
    proveedor = request.args.get('proveedor')
    stock_min = request.args.get('stock_min')

    query = VistaProductoDetalle.query

    if nombre:
        query = query.filter(VistaProductoDetalle.nombre.ilike(f'%{nombre}%'))
    if estado:
        query = query.filter(VistaProductoDetalle.estado == estado)
    if categoria:
        query = query.filter(VistaProductoDetalle.categorias.any(categoria))
    if proveedor:
        query = query.filter(VistaProductoDetalle.proveedores.any(proveedor))
    if stock_min:
        query = query.filter(VistaProductoDetalle.stock >= int(stock_min))

    resultados = query.all()
    return render_template('reportes/productos.html', productos=resultados)

# --------------------
# REPORTE: USUARIOS
# --------------------
@reportes_bp.route('/usuarios')
def reporte_usuarios():
    nombre = request.args.get('nombre')
    email = request.args.get('email')
    rol = request.args.get('rol')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = VistaUsuariosRoles.query

    if nombre:
        query = query.filter(VistaUsuariosRoles.nombre.ilike(f'%{nombre}%'))
    if email:
        query = query.filter(VistaUsuariosRoles.email.ilike(f'%{email}%'))
    if rol:
        query = query.filter(VistaUsuariosRoles.roles.any(rol))
    if fecha_inicio:
        query = query.filter(VistaUsuariosRoles.fecha_registro >= fecha_inicio)
    if fecha_fin:
        query = query.filter(VistaUsuariosRoles.fecha_registro <= fecha_fin)

    resultados = query.all()
    return render_template('reportes/usuarios.html', usuarios=resultados)

# --------------------
# REPORTE: PEDIDOS
# --------------------
@reportes_bp.route('/pedidos')
def reporte_pedidos():
    cliente = request.args.get('cliente')
    email = request.args.get('email')
    estado = request.args.get('estado')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = VistaPedidosCompletos.query

    if cliente:
        query = query.filter(VistaPedidosCompletos.cliente.ilike(f'%{cliente}%'))
    if email:
        query = query.filter(VistaPedidosCompletos.email.ilike(f'%{email}%'))
    if estado:
        query = query.filter(VistaPedidosCompletos.estado == estado)
    if fecha_inicio:
        query = query.filter(VistaPedidosCompletos.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(VistaPedidosCompletos.fecha <= fecha_fin)

    resultados = query.all()
    return render_template('reportes/pedidos.html', pedidos=resultados)