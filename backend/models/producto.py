from extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

# Enum ya definido en PostgreSQL
estado_producto_enum = ENUM(
    'activo', 'inactivo', 'eliminado',
    name='estado_producto',
    create_type=False  # Evita error si ya existe en la base de datos
)

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    estado = db.Column(estado_producto_enum, nullable=False, default='activo')

    # Relaciones bidireccionales con ondelete y cascade para mantener integridad
    proveedores = relationship(
        'ProductoProveedor',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    categorias = relationship(
        'ProductoCategoria',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    imagenes = relationship(
        'ImagenProducto',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    detalles_pedido = relationship(
        'DetallePedido',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    resenas = relationship(
        'Resena',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )
    carrito_items = relationship(
        'CarritoProducto',
        back_populates='producto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )

    def __repr__(self):
        return f'<Producto {self.nombre} - ${self.precio} - Estado: {self.estado}>'