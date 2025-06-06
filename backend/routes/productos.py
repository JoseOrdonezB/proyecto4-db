from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from extensions import db
from models.producto import Producto
from datetime import date

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

# ----------------------------
# API JSON: Listar todos los productos
# ----------------------------
@productos_bp.route('/', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'precio': float(p.precio),
        'stock': p.stock,
        'estado': p.estado
    } for p in productos])

# ----------------------------
# API JSON: Obtener producto por ID
# ----------------------------
@productos_bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': float(producto.precio),
        'stock': producto.stock,
        'descripcion': producto.descripcion,
        'sku': producto.sku,
        'estado': producto.estado
    })

# ----------------------------
# HTML: Listar productos con filtros
# ----------------------------
@productos_bp.route('/gestionar', methods=['GET'])
def gestionar_productos():
    nombre = request.args.get('nombre')
    estado = request.args.get('estado')
    stock_min = request.args.get('stock_min')
    stock_max = request.args.get('stock_max')

    query = Producto.query

    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if estado:
        query = query.filter_by(estado=estado)
    if stock_min:
        query = query.filter(Producto.stock >= int(stock_min))
    if stock_max:
        query = query.filter(Producto.stock <= int(stock_max))

    productos = query.all()
    return render_template('reportes/productos.html', productos=productos, editar=False, producto=None)

# ----------------------------
# HTML: Mostrar formulario de edición
# ----------------------------
@productos_bp.route('/editar/<int:id>', methods=['GET'])
def editar_producto_html(id):
    producto = Producto.query.get_or_404(id)
    return render_template('reportes/productos.html', productos=[], editar=True, producto=producto)

# ----------------------------
# HTML: Crear nuevo producto
# ----------------------------
@productos_bp.route('/crear', methods=['POST'])
def crear_producto_html():
    try:
        id_manual = request.form.get('id')
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion')
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        sku = request.form['sku']
        estado = request.form.get('estado', 'activo')

        if id_manual:
            id_manual = int(id_manual)
            if Producto.query.get(id_manual):
                return f"Error: Ya existe un producto con ID {id_manual}", 400
            nuevo = Producto(id=id_manual, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, sku=sku, estado=estado)
        else:
            nuevo = Producto(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, sku=sku, estado=estado)

        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('productos.gestionar_productos'))

    except Exception as e:
        db.session.rollback()
        return f"Error al crear el producto: {str(e)}", 500

# ----------------------------
# HTML: Editar producto existente
# ----------------------------
@productos_bp.route('/editar/<int:id>', methods=['POST'])
def actualizar_producto_html(id):
    try:
        producto = Producto.query.get_or_404(id)
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form.get('descripcion')
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])
        producto.sku = request.form['sku']
        producto.estado = request.form['estado']

        db.session.commit()
        return redirect(url_for('productos.gestionar_productos'))
    except Exception as e:
        db.session.rollback()
        return f"Error al editar el producto: {str(e)}", 500

# ----------------------------
# HTML: Eliminar producto
# ----------------------------
@productos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto_html(id):
    try:
        producto = Producto.query.get_or_404(id)

        # Limpiar relaciones N:M antes de borrar
        producto.proveedores.clear()
        producto.categorias.clear()
        db.session.commit()

        db.session.delete(producto)
        db.session.commit()
        return redirect(url_for('productos.gestionar_productos'))
    except Exception as e:
        db.session.rollback()
        return f"Error al eliminar el producto: {str(e)}", 500