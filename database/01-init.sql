
-- Tipos de datos personalizados
CREATE TYPE estado_producto AS ENUM ('activo', 'inactivo', 'eliminado');
CREATE TYPE rol_usuario AS ENUM ('cliente', 'admin', 'vendedor');
CREATE TYPE tipo_direccion AS ENUM ('facturacion', 'envio');
CREATE TYPE estado_pedido AS ENUM ('pendiente', 'pagado', 'enviado', 'cancelado');
CREATE TYPE tipo_pago AS ENUM ('tarjeta', 'efectivo', 'transferencia', 'paypal');

-- Usuarios y roles
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro DATE NOT NULL
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    rol rol_usuario NOT NULL
);

CREATE TABLE usuarios_roles (
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    rol_id INT REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, rol_id)
);

-- Productos, categorías y proveedores
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100)
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    sku VARCHAR(50) UNIQUE NOT NULL,
    estado estado_producto NOT NULL DEFAULT 'activo'
);

CREATE TABLE productos_proveedores (
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    proveedor_id INT REFERENCES proveedores(id) ON DELETE CASCADE,
    PRIMARY KEY (producto_id, proveedor_id)
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE productos_categorias (
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    categoria_id INT REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (producto_id, categoria_id)
);

CREATE TABLE imagenes_producto (
    id SERIAL PRIMARY KEY,
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    url VARCHAR(255) NOT NULL
);

-- Carritos y pedidos
CREATE TABLE carritos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    fecha_creacion DATE NOT NULL
);

CREATE TABLE carrito_productos (
    carrito_id INT REFERENCES carritos(id) ON DELETE CASCADE,
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    cantidad INT NOT NULL,
    PRIMARY KEY (carrito_id, producto_id)
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    total NUMERIC(10,2) NOT NULL,
    fecha DATE NOT NULL,
    estado estado_pedido NOT NULL
);

CREATE TABLE detalles_pedido (
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    cantidad INT NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (pedido_id, producto_id)
);

-- Envíos y direcciones
CREATE TABLE direcciones (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    direccion VARCHAR(255) NOT NULL,
    tipo tipo_direccion NOT NULL
);

CREATE TABLE envios (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    direccion_id INT REFERENCES direcciones(id) ON DELETE CASCADE,
    transportista VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL
);

-- Pagos y métodos
CREATE TABLE metodos_pago (
    id SERIAL PRIMARY KEY,
    tipo tipo_pago NOT NULL
);

CREATE TABLE pagos (
    id SERIAL PRIMARY KEY,
    pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
    metodo_pago_id INT REFERENCES metodos_pago(id) ON DELETE CASCADE,
    estado VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL
);

-- Reseñas y soporte
CREATE TABLE resenas (
    id SERIAL PRIMARY KEY,
    producto_id INT REFERENCES productos(id) ON DELETE CASCADE,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    puntuacion INT NOT NULL,
    comentario TEXT
);

CREATE TABLE tickets_soporte (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    motivo VARCHAR(255) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    prioridad VARCHAR(50) NOT NULL
);

CREATE TABLE respuestas_soporte (
    id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES tickets_soporte(id) ON DELETE CASCADE,
    agente VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    mensaje TEXT NOT NULL
);

-- Triggers funcionales
CREATE OR REPLACE FUNCTION descontar_stock()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE productos
  SET stock = stock - NEW.cantidad
  WHERE id = NEW.producto_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_descontar_stock
AFTER INSERT ON detalles_pedido
FOR EACH ROW
EXECUTE FUNCTION descontar_stock();

CREATE OR REPLACE FUNCTION validar_stock()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT stock FROM productos WHERE id = NEW.producto_id) < NEW.cantidad THEN
    RAISE EXCEPTION 'Stock insuficiente';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_stock
BEFORE INSERT ON detalles_pedido
FOR EACH ROW
EXECUTE FUNCTION validar_stock();

CREATE OR REPLACE FUNCTION asignar_fecha()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.fecha IS NULL THEN
    NEW.fecha := CURRENT_DATE;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_asignar_fecha
BEFORE INSERT ON pedidos
FOR EACH ROW
EXECUTE FUNCTION asignar_fecha();

-- Funciones
CREATE OR REPLACE FUNCTION total_pedidos_por_usuario(uid INT)
RETURNS INT AS $$
BEGIN
  RETURN (SELECT COUNT(*) FROM pedidos WHERE usuario_id = uid);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION monto_total_pedidos(uid INT)
RETURNS NUMERIC AS $$
BEGIN
  RETURN (SELECT SUM(total) FROM pedidos WHERE usuario_id = uid);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION listar_productos_bajo_stock(minimo INT)
RETURNS TABLE(id INT, nombre TEXT, stock INT) AS $$
BEGIN
  RETURN QUERY SELECT id, nombre, stock FROM productos WHERE stock <= minimo;
END;
$$ LANGUAGE plpgsql;

-- Vistas
CREATE OR REPLACE VIEW vista_productos_detalle AS
SELECT
    p.id,
    p.nombre,
    p.precio,
    p.stock,
    p.estado,
    array_agg(DISTINCT c.nombre) AS categorias,
    array_agg(DISTINCT pr.nombre) AS proveedores
FROM productos p
LEFT JOIN productos_categorias pc ON p.id = pc.producto_id
LEFT JOIN categorias c ON pc.categoria_id = c.id
LEFT JOIN productos_proveedores pp ON p.id = pp.producto_id
LEFT JOIN proveedores pr ON pp.proveedor_id = pr.id
GROUP BY p.id;

CREATE OR REPLACE VIEW vista_usuarios_roles AS
SELECT
    u.id,
    u.nombre,
    u.email,
    u.fecha_registro,
    array_agg(r.rol) AS roles
FROM usuarios u
LEFT JOIN usuarios_roles ur ON u.id = ur.usuario_id
LEFT JOIN roles r ON ur.rol_id = r.id
GROUP BY u.id;

CREATE OR REPLACE VIEW vista_pedidos_completos AS
SELECT
    p.id AS pedido_id,
    u.nombre AS cliente,
    u.email,
    p.total,
    p.fecha,
    p.estado
FROM pedidos p
JOIN usuarios u ON p.usuario_id = u.id;
