from extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, ENUM

# Enum definido previamente en PostgreSQL
rol_usuario_enum = ENUM(
    'cliente', 'admin', 'vendedor',
    name='rol_usuario',
    create_type=False
)

class VistaUsuariosRoles(db.Model):
    __tablename__ = 'vista_usuarios_roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.Date, nullable=False)
    roles = db.Column(ARRAY(rol_usuario_enum), nullable=False)

    def __repr__(self):
        return f'<VistaUsuariosRoles {self.nombre} ({self.email}) Roles={self.roles}>'