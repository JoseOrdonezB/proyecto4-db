# Proyecto Bases de Datos 1

Este proyecto consiste en la utilización del contenido visto durante el semestre, implementando esos conocimientos en un proyecto más cercano a un proyecto de la vida real.

## Demostración de funcionamiento
Por cualquier duda, problema o error, puedes ver este video para ver el proyecto en funcionamiento.

[Video de demostración](https://youtu.be/InZ9X7qKAVI)

## 🛠️ Tecnologías utilizadas

- **Backend:** Python, Flask, SQLAlchemy
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker + Docker Compose
- **ORM:** SQLAlchemy
- **Lenguaje SQL:** para funciones, vistas, triggers y validaciones

## ⚙️ Funcionalidades principales

### 📋 CRUDs implementados
- **Usuarios**
- **Productos**
- **Pedidos**

### 📈 Reportes
Se implementaron 3 reportes HTML con filtros y exportación a CSV:
1. **Usuarios:** filtros por nombre, email, fechas
2. **Productos:** filtros por nombre, SKU, estado, stock mínimo y máximo
3. **Pedidos:** filtros por cliente, correo, estado, fecha de inicio y fin

### 🧠 Reglas y validaciones
- Tipos personalizados definidos en PostgreSQL (`ENUM`)
- `CHECK` para stock y precio no negativos
- `UNIQUE` en correo y SKU
- Triggers:
  - Validación de stock antes del pedido
  - Descuento automático de stock
  - Asignación automática de fecha de pedido

### 🔍 Vistas y funciones SQL
- **Vistas:**
  - `vista_pedidos_completos`
  - `vista_productos_detalle`
  - `vista_usuarios_roles`
- **Funciones:**
  - `total_pedidos_por_usuario`
  - `monto_total_pedidos`
  - `listar_productos_bajo_stock`

## 🚀 Cómo ejecutar el proyecto

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JoseOrdonezB/proyecto4-db
   cd proyecto4-db
   ```

2. Levanta los servicios con Docker:
   ```bash
   docker-compose up --build
   ```

3. Accede al frontend:
   ```
   http://localhost:5173
   ```

4. Accede al backend (API):
   ```
   http://localhost:8000
   ```
