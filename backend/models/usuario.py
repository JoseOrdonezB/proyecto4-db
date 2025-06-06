from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

# Enum ya definido en PostgreSQL
rol_usuario_enum = ENUM(
    'cliente', 'admin', 'vendedor',
    name='rol_usuario',
    create_type=False
)

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)

    # Relaciones
    carritos = relationship('Carrito', back_populates='usuario', lazy=True)
    pedidos = relationship('Pedido', back_populates='usuario', lazy=True)
    direcciones = relationship('Direccion', back_populates='usuario', lazy=True)
    resenas = relationship('Resena', back_populates='usuario', lazy=True)
    tickets_soporte = relationship('TicketSoporte', back_populates='usuario', lazy=True)
    roles = relationship(
        'UsuarioRol',
        back_populates='usuario',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.email})>'
