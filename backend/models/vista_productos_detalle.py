from extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, ENUM

# Enum ya creado en PostgreSQL
estado_producto_enum = ENUM(
    'activo', 'inactivo', 'eliminado',
    name='estado_producto',
    create_type=False
)

class VistaProductoDetalle(db.Model):
    __tablename__ = 'vista_productos_detalle'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    estado = db.Column(estado_producto_enum, nullable=False)
    categorias = db.Column(ARRAY(db.String), nullable=False)
    proveedores = db.Column(ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f'<VistaProductoDetalle {self.nombre} (${self.precio})>'