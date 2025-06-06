# Usuario y roles
from .usuario import Usuario
from .rol import Rol, UsuarioRol

# Productos y relaciones
from .producto import Producto
from .proveedor import Proveedor, ProductoProveedor
from .categoria import Categoria, ProductoCategoria
from .imagen_producto import ImagenProducto
from .resena import Resena

# Carritos y productos en carrito
from .carrito import Carrito, CarritoProducto

# Pedidos y detalles
from .pedido import Pedido, DetallePedido

# Envíos y direcciones
from .direccion import Direccion
from .envio import Envio

# Pagos y métodos
from .pago import Pago, MetodoPago

# Soporte
from .soporte import TicketSoporte, RespuestaSoporte

# Vistas SQL (opcional si las usas como modelo)
from .vista_productos_detalle import VistaProductoDetalle
from .vista_usuarios_roles import VistaUsuariosRoles
from .vista_pedidos_completos import VistaPedidosCompletos