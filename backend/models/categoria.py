from extensions import db
from sqlalchemy.orm import relationship

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    productos = relationship('ProductoCategoria', back_populates='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class ProductoCategoria(db.Model):
    __tablename__ = 'productos_categorias'

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), primary_key=True)

    producto = relationship('Producto', back_populates='categorias', lazy=True)
    categoria = relationship('Categoria', back_populates='productos', lazy=True)

    def __repr__(self):
        return f'<ProductoCategoria Producto={self.producto_id} Categoria={self.categoria_id}>'