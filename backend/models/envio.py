from extensions import db

class Envio(db.Model):
    __tablename__ = 'envios'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey('direcciones.id'), nullable=False)
    transportista = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    # Relaciones con Pedido y Direccion
    direccion = db.relationship('Direccion', backref='envios', lazy=True)

    def __repr__(self):
        return f'<Envio {self.id} - Pedido {self.pedido_id} - Estado: {self.estado}>'