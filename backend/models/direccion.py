from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Enum ya creado en PostgreSQL
tipo_direccion_enum = ENUM(
    'facturacion', 'envio',
    name='tipo_direccion',
    create_type=False
)

class Direccion(db.Model):
    __tablename__ = 'direcciones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    tipo = db.Column(tipo_direccion_enum, nullable=False)

    # Relación bidireccional con Usuario
    usuario = relationship('Usuario', back_populates='direcciones', lazy=True)

    # Relación con envíos (si usas back_populates en Envio)
    envios = relationship('Envio', back_populates='direccion', lazy=True)

    def __repr__(self):
        return f'<Direccion {self.tipo} - Usuario {self.usuario_id}>'