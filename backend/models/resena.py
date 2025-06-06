from extensions import db

class Resena(db.Model):
    __tablename__ = 'resenas'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)

    def __repr__(self):
        return f'<Resena Producto={self.producto_id} Usuario={self.usuario_id} Puntuación={self.puntuacion}>'