from flask import Flask, render_template
from config import Config
from extensions import db, migrate
from flask_cors import CORS

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
migrate.init_app(app, db)
CORS(app)

# Importar modelos (esto registra las tablas en SQLAlchemy)
from models import *

# Registrar blueprints
from routes.usuarios import usuarios_bp
from routes.productos import productos_bp
from routes.pedidos import pedidos_bp
from routes.carritos import carritos_bp
from routes.pagos import pagos_bp
from routes.soporte import soporte_bp
from routes.vistas import vistas_bp
from routes.reportes import reportes_bp

app.register_blueprint(usuarios_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(carritos_bp)
app.register_blueprint(pagos_bp)
app.register_blueprint(soporte_bp)
app.register_blueprint(vistas_bp)
app.register_blueprint(reportes_bp)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])