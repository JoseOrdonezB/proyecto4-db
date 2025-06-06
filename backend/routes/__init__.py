from .usuarios import usuarios_bp
from .productos import productos_bp
from .pedidos import pedidos_bp
from .carritos import carritos_bp
from .pagos import pagos_bp
from .soporte import soporte_bp
from .vistas import vistas_bp  # para vistas SQL

def register_routes(app):
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(carritos_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(soporte_bp)
    app.register_blueprint(vistas_bp)