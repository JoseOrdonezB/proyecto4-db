from extensions import db

class ImagenProducto(db.Model):
    __tablename__ = 'imagenes_producto'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<ImagenProducto {self.id} - Producto {self.producto_id}>'