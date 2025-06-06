from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

# Enum reutilizable ya creado en PostgreSQL
estado_pedido_enum = ENUM(
    'pendiente', 'pagado', 'enviado', 'cancelado',
    name='estado_pedido',
    create_type=False  # No volver a crear si ya existe
)

class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(estado_pedido_enum, nullable=False)

    # Relaciones
    detalles = relationship(
        'DetallePedido',
        back_populates='pedido',
        cascade='all, delete-orphan',
        lazy=True
    )
    envio = relationship('Envio', back_populates='pedido', uselist=False, lazy='joined')
    pago = relationship('Pago', back_populates='pedido', uselist=False, lazy='joined')
    usuario = relationship('Usuario', back_populates='pedidos', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id} - Usuario {self.usuario_id} - Estado {self.estado}>'

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey('pedidos.id', ondelete='CASCADE'),
        primary_key=True
    )
    producto_id = db.Column(
        db.Integer,
        db.ForeignKey('productos.id', ondelete='CASCADE'),
        primary_key=True
    )
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = relationship('Pedido', back_populates='detalles', lazy=True)
    producto = relationship('Producto', back_populates='detalles_pedido', lazy=True)

    def __repr__(self):
        return f'<DetallePedido Pedido={self.pedido_id} Producto={self.producto_id} Cantidad={self.cantidad}>'