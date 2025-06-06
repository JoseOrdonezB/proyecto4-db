from extensions import db
from sqlalchemy.orm import relationship

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))

    # Relación con productos a través de tabla intermedia
    productos = relationship('ProductoProveedor', backref='proveedor', lazy=True)

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'

class ProductoProveedor(db.Model):
    __tablename__ = 'productos_proveedores'

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), primary_key=True)

    # Relación con Producto (opcional pero útil)
    producto = relationship('Producto', backref='proveedor_asociaciones', lazy=True)

    def __repr__(self):
        return f'<ProductoProveedor Producto={self.producto_id} Proveedor={self.proveedor_id}>'