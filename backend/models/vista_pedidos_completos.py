from extensions import db

class VistaPedidosCompletos(db.Model):
    __tablename__ = 'vista_pedidos_completos'

    pedido_id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<VistaPedidosCompletos Pedido={self.pedido_id} Cliente={self.cliente}>'