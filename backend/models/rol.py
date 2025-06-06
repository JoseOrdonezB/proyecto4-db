from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

rol_usuario_enum = ENUM(
    'cliente', 'admin', 'vendedor',
    name='rol_usuario',
    create_type=False  # Asegúrate de que ya esté creado en PostgreSQL
)

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(rol_usuario_enum, nullable=False)

    usuarios = relationship(
        'UsuarioRol',
        back_populates='rol',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )

    def __repr__(self):
        return f'<Rol {self.rol}>'


class UsuarioRol(db.Model):
    __tablename__ = 'usuarios_roles'

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id', ondelete='CASCADE'),
        primary_key=True
)
    rol_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    )

    usuario = relationship('Usuario', back_populates='roles', lazy=True)
    rol = relationship('Rol', back_populates='usuarios', lazy=True)

    def __repr__(self):
        return f'<UsuarioRol Usuario={self.usuario_id} Rol={self.rol_id}>'