from extensions import db
from sqlalchemy.orm import relationship

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))

    # Relación con productos_proveedores (intermedia)
    productos = relationship('ProductoProveedor', back_populates='proveedor')

    def __repr__(self):
        return f'<Proveedor {self.nombre}>'

class ProductoProveedor(db.Model):
    __tablename__ = 'productos_proveedores'

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), primary_key=True)

    # Relaciones bidireccionales
    producto = relationship('Producto', back_populates='proveedores')
    proveedor = relationship('Proveedor', back_populates='productos')

    def __repr__(self):
        return f'<ProductoProveedor Producto={self.producto_id} Proveedor={self.proveedor_id}>'