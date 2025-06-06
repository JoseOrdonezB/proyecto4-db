from extensions import db
from sqlalchemy.orm import relationship

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)

    # Relaciones bidireccionales usando back_populates
    carritos = relationship('Carrito', back_populates='usuario', lazy=True)
    pedidos = relationship('Pedido', back_populates='usuario', lazy=True)
    direcciones = relationship('Direccion', back_populates='usuario', lazy=True)
    resenas = relationship('Resena', back_populates='usuario', lazy=True)
    tickets_soporte = relationship('TicketSoporte', back_populates='usuario', lazy=True)
    roles = relationship('UsuarioRol', back_populates='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.email})>'