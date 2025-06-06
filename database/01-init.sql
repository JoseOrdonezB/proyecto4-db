-- tipos de datos personalizados

create type estado_producto as enum ('activo', 'inactivo', 'eliminado');
create type rol_usuario as enum ('cliente', 'admin', 'vendedor');
create type tipo_direccion as enum ('facturacion', 'envio');
create type estado_pedido as enum ('pendiente', 'pagado', 'enviado', 'cancelado');
create type tipo_pago as enum ('tarjeta', 'efectivo', 'transferencia', 'paypal');

-- usuarios y roles

create table usuarios (
    id serial primary key,
    nombre varchar(100) not null,
    email varchar(100) unique not null,
    contrasena varchar(255) not null,
    fecha_registro date not null
);

create table roles (
    id serial primary key,
    rol rol_usuario not null
);

create table usuarios_roles (
    usuario_id int references usuarios(id) on delete cascade,
    rol_id int references roles(id) on delete cascade,
    primary key (usuario_id, rol_id)
);

-- productos, categorías y proveedores

create table proveedores (
    id serial primary key,
    nombre varchar(100) not null,
    contacto varchar(100)
);

create table productos (
    id serial primary key,
    nombre varchar(100) not null,
    descripcion text,
    precio numeric(10,2) not null,
    stock int not null,
    sku varchar(50) unique not null,
    estado estado_producto not null
);

create table productos_proveedores (
    producto_id int references productos(id) on delete cascade,
    proveedor_id int references proveedores(id) on delete cascade,
    primary key (producto_id, proveedor_id)
);

create table categorias (
    id serial primary key,
    nombre varchar(100) not null
);

create table productos_categorias (
    producto_id int references productos(id) on delete cascade,
    categoria_id int references categorias(id) on delete cascade,
    primary key (producto_id, categoria_id)
);

create table imagenes_producto (
    id serial primary key,
    producto_id int references productos(id) on delete cascade,
    url varchar(255) not null
);

-- carritos y pedidos

create table carritos (
    id serial primary key,
    usuario_id int references usuarios(id) on delete cascade,
    fecha_creacion date not null
);

create table carrito_productos (
    carrito_id int references carritos(id) on delete cascade,
    producto_id int references productos(id) on delete cascade,
    cantidad int not null,
    primary key (carrito_id, producto_id)
);

create table pedidos (
    id serial primary key,
    usuario_id int references usuarios(id) on delete cascade,
    total numeric(10,2) not null,
    fecha date not null,
    estado estado_pedido not null
);

create table detalles_pedido (
    pedido_id int references pedidos(id) on delete cascade,
    producto_id int references productos(id) on delete cascade,
    cantidad int not null,
    precio_unitario numeric(10,2) not null,
    primary key (pedido_id, producto_id)
);

-- envíos y direcciones

create table direcciones (
    id serial primary key,
    usuario_id int references usuarios(id) on delete cascade,
    direccion varchar(255) not null,
    tipo tipo_direccion not null
);

create table envios (
    id serial primary key,
    pedido_id int references pedidos(id),
    direccion_id int references direcciones(id),
    transportista varchar(100) not null,
    estado varchar(50) not null
);

-- pagos y métodos

create table metodos_pago (
    id serial primary key,
    tipo tipo_pago not null
);

create table pagos (
    id serial primary key,
    pedido_id int references pedidos(id),
    metodo_pago_id int references metodos_pago(id),
    estado varchar(50) not null,
    fecha date not null
);

-- reseñas y soporte

create table resenas (
    id serial primary key,
    producto_id int references productos(id) on delete cascade,
    usuario_id int references usuarios(id) on delete cascade,
    puntuacion int not null,
    comentario text
);

create table tickets_soporte (
    id serial primary key,
    usuario_id int references usuarios(id) on delete cascade,
    motivo varchar(255) not null,
    estado varchar(50) not null,
    prioridad varchar(50) not null
);

create table respuestas_soporte (
    id serial primary key,
    ticket_id int references tickets_soporte(id),
    agente varchar(100) not null,
    fecha date not null,
    mensaje text not null
);


-- producto con precio no negativo

alter table productos
add constraint chk_precio check (precio >= 0);

-- email único

alter table usuarios
add constraint unique_email unique (email);

-- stock no puede ser negativo

alter table productos
add constraint chk_stock check (stock >= 0);

-- estado por defecto

alter table productos
alter column estado set default 'activo';

-- Triggers funcionales
-- actualizar stock despues de pedido

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

-- validar stock antes de pedido
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

-- asignar fecha automaticamente
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


