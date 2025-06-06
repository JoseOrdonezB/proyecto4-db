from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Enum ya definido en PostgreSQL
tipo_pago_enum = ENUM(
    'tarjeta', 'efectivo', 'transferencia', 'paypal',
    name='tipo_pago',
    create_type=False
)

class MetodoPago(db.Model):
    __tablename__ = 'metodos_pago'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(tipo_pago_enum, nullable=False)

    # Relación explícita con Pago
    pagos = relationship('Pago', back_populates='metodo_pago', lazy=True)

    def __repr__(self):
        return f'<MetodoPago {self.tipo}>'

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodos_pago.id'), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    # Relaciones explícitas
    metodo_pago = relationship('MetodoPago', back_populates='pagos', lazy=True)
    pedido = relationship('Pedido', back_populates='pago', lazy=True)

    def __repr__(self):
        return f'<Pago Pedido={self.pedido_id} Método={self.metodo_pago_id} Estado={self.estado}>'