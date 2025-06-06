from extensions import db
from sqlalchemy.orm import relationship

class Carrito(db.Model):
    __tablename__ = 'carritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)

    # Relación con productos del carrito
    productos = relationship('CarritoProducto', backref='carrito', lazy=True)

    def __repr__(self):
        return f'<Carrito {self.id} - Usuario {self.usuario_id}>'

class CarritoProducto(db.Model):
    __tablename__ = 'carrito_productos'

    carrito_id = db.Column(db.Integer, db.ForeignKey('carritos.id'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

    # Relación con el modelo Producto
    producto = relationship('Producto', backref='carrito_items', lazy=True)

    def __repr__(self):
        return f'<CarritoProducto Carrito={self.carrito_id} Producto={self.producto_id} Cantidad={self.cantidad}>'