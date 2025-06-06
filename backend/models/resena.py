from extensions import db
from sqlalchemy.orm import relationship

class Resena(db.Model):
    __tablename__ = 'resenas'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)

    # Relaciones bidireccionales
    producto = relationship('Producto', back_populates='resenas')
    usuario = relationship('Usuario', back_populates='resenas')

    def __repr__(self):
        return f'<Resena Producto={self.producto_id} Usuario={self.usuario_id} Puntuación={self.puntuacion}>'