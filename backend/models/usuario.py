from extensions import db
from sqlalchemy.orm import relationship

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)

    # Relaciones
    carritos = relationship('Carrito', backref='usuario', lazy=True)
    pedidos = relationship('Pedido', backref='usuario', lazy=True)
    direcciones = relationship('Direccion', backref='usuario', lazy=True)
    resenas = relationship('Resena', backref='usuario', lazy=True)
    tickets_soporte = relationship('TicketSoporte', backref='usuario', lazy=True)
    roles = relationship('UsuarioRol', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nombre} ({self.email})>'