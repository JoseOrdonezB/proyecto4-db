from extensions import db
from sqlalchemy.orm import relationship

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relación con productos a través de la tabla intermedia
    productos = relationship('ProductoCategoria', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class ProductoCategoria(db.Model):
    __tablename__ = 'productos_categorias'

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), primary_key=True)

    # Relación con Producto (opcional pero útil)
    producto = relationship('Producto', backref='categoria_asociaciones', lazy=True)

    def __repr__(self):
        return f'<ProductoCategoria Producto={self.producto_id} Categoria={self.categoria_id}>'