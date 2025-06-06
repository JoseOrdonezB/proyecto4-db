from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Enum ya definido en PostgreSQL
estado_pedido_enum = ENUM(
    'pendiente', 'pagado', 'enviado', 'cancelado',
    name='estado_pedido',
    create_type=False
)

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(estado_pedido_enum, nullable=False)

    # Relaciones
    detalles = relationship('DetallePedido', backref='pedido', lazy=True)
    envio = relationship('Envio', backref='pedido', uselist=False, lazy=True)
    pago = relationship('Pago', backref='pedido', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id} - Usuario {self.usuario_id} - Estado {self.estado}>'

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    producto = relationship('Producto', backref='detalles_pedido', lazy=True)

    def __repr__(self):
        return f'<DetallePedido Pedido={self.pedido_id} Producto={self.producto_id} Cantidad={self.cantidad}>'