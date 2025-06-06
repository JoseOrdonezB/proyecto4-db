from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Enum ya definido en PostgreSQL
rol_usuario_enum = ENUM(
    'cliente', 'admin', 'vendedor',
    name='rol_usuario',
    create_type=False
)

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(rol_usuario_enum, nullable=False)

    # Relación con UsuarioRol
    usuarios = relationship('UsuarioRol', back_populates='rol', lazy=True)

    def __repr__(self):
        return f'<Rol {self.rol}>'

class UsuarioRol(db.Model):
    __tablename__ = 'usuarios_roles'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    # Relaciones explícitas con Usuario y Rol
    usuario = relationship('Usuario', back_populates='roles', lazy=True)
    rol = relationship('Rol', back_populates='usuarios', lazy=True)

    def __repr__(self):
        return f'<UsuarioRol Usuario={self.usuario_id} Rol={self.rol_id}>'