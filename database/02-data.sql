-- Insertar proveedores
INSERT INTO proveedores (id, nombre, contacto) VALUES
(1, 'Proveedor Alpha', 'alpha@example.com'),
(2, 'Proveedor Beta', 'beta@example.com');

-- Insertar categorías
INSERT INTO categorias (id, nombre) VALUES
(1, 'Electrónica'),
(2, 'Hogar');

-- Insertar productos
INSERT INTO productos (id, nombre, descripcion, precio, stock, sku, estado) VALUES
(1, 'Laptop XYZ', 'Laptop de alto rendimiento', 1200.00, 10, 'LAP123', 'activo'),
(2, 'Aspiradora Zeta', 'Aspiradora silenciosa', 250.00, 5, 'ASP456', 'activo'),
(3, 'Tablet Nova', 'Tablet liviana de 10 pulgadas', 300.00, 0, 'TAB789', 'inactivo');

-- Asociaciones producto-proveedor
INSERT INTO productos_proveedores (producto_id, proveedor_id) VALUES
(1, 1),
(2, 2),
(3, 1);

-- Asociaciones producto-categoría
INSERT INTO productos_categorias (producto_id, categoria_id) VALUES
(1, 1),  -- Laptop en Electrónica
(2, 2),  -- Aspiradora en Hogar
(3, 1);  -- Tablet en Electrónica

-- Imágenes
INSERT INTO imagenes_producto (id, producto_id, url) VALUES
(1, 1, 'https://example.com/laptop.jpg'),
(2, 2, 'https://example.com/aspiradora.jpg'),
(3, 3, 'https://example.com/tablet.jpg');

-- Insertar usuarios
INSERT INTO usuarios (id, nombre, email, contrasena, fecha_registro) VALUES
(1, 'Carlos Pérez', 'carlos@example.com', 'hashed_pass', '2024-01-10'),
(2, 'Ana Gómez', 'ana@example.com', 'hashed_pass', '2024-02-15'),
(3, 'Luis Ramírez', 'luis@example.com', 'hashed_pass', '2024-03-20');

-- Insertar roles
INSERT INTO roles (id, rol) VALUES
(1, 'cliente'),
(2, 'admin');

-- Asignar roles a usuarios
INSERT INTO usuarios_roles (usuario_id, rol_id) VALUES
(1, 1),
(2, 2),
(3, 1);

-- Insertar direcciones
INSERT INTO direcciones (id, usuario_id, direccion, tipo) VALUES
(1, 1, 'Calle 1, Zona 10', 'envio'),
(2, 1, 'Calle 1, Zona 10', 'facturacion'),
(3, 3, 'Avenida Reforma 5, Zona 9', 'envio');

-- Insertar pedidos
INSERT INTO pedidos (id, usuario_id, total, fecha, estado) VALUES
(1, 1, 159.99, '2024-04-10', 'pagado'),
(2, 3, 89.50, '2024-04-12', 'pendiente');

-- Insertar pagos
INSERT INTO metodos_pago (id, tipo) VALUES
(1, 'tarjeta'),
(2, 'paypal');

INSERT INTO pagos (id, pedido_id, metodo_pago_id, estado, fecha) VALUES
(1, 1, 1, 'completado', '2024-04-10'),
(2, 2, 2, 'pendiente', '2024-04-12');

-- Insertar envíos
INSERT INTO envios (id, pedido_id, direccion_id, transportista, estado) VALUES
(1, 1, 1, 'CargoExpress', 'enviado'),
(2, 2, 3, 'Guatex', 'pendiente');

-- Detalles de pedidos
INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 2, 49.99),
(1, 2, 1, 39.50),
(2, 2, 2, 39.50);