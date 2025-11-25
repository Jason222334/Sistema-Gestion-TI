-- Tablas base
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    razon_social VARCHAR(255) NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(50),
    email VARCHAR(100),
    contacto_nombre VARCHAR(100),
    contacto_telefono VARCHAR(50),
    sitio_web VARCHAR(255),
    calificacion DECIMAL(3,2),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

CREATE TABLE categorias_equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    vida_util_anos INTEGER,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    edificio VARCHAR(100),
    piso VARCHAR(50),
    aula_oficina VARCHAR(100),
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    nombre_completo VARCHAR(200),
    rol VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    codigo_inventario VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    numero_serie VARCHAR(100),
    categoria_id INTEGER REFERENCES categorias_equipos(id),
    especificaciones JSONB,
    proveedor_id INTEGER REFERENCES proveedores(id),
    fecha_compra DATE,
    costo_compra DECIMAL(12,2),
    fecha_garantia_fin DATE,
    ubicacion_actual_id INTEGER REFERENCES ubicaciones(id),
    estado_operativo VARCHAR(50) DEFAULT 'operativo', -- operativo, en_reparacion, obsoleto, dado_baja
    estado_fisico VARCHAR(50),
    asignado_a_id INTEGER REFERENCES usuarios(id),
    notas TEXT,
    imagen_url VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimientos_equipos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id),
    ubicacion_origen_id INTEGER REFERENCES ubicaciones(id),
    ubicacion_destino_id INTEGER REFERENCES ubicaciones(id),
    usuario_responsable_id INTEGER REFERENCES usuarios(id),
    motivo TEXT,
    observaciones TEXT,
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mantenimientos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id),
    tipo VARCHAR(50), -- preventivo, correctivo
    fecha_programada DATE,
    fecha_realizada DATE,
    descripcion TEXT,
    costo DECIMAL(10,2),
    estado VARCHAR(50), -- programado, en_proceso, completado
    prioridad VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER REFERENCES proveedores(id),
    numero_contrato VARCHAR(100),
    tipo VARCHAR(50),
    fecha_inicio DATE,
    fecha_fin DATE,
    monto_total DECIMAL(12,2),
    estado VARCHAR(50),
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id),
    mantenimiento_id INTEGER REFERENCES mantenimientos(id),
    tipo VARCHAR(50),
    titulo VARCHAR(200),
    mensaje TEXT,
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_lectura TIMESTAMP
);

-- Datos Semilla (Seed Data) para pruebas
INSERT INTO categorias_equipos (nombre, vida_util_anos) VALUES ('Laptops', 4), ('Impresoras', 5), ('Servidores', 7);
INSERT INTO ubicaciones (edificio, aula_oficina) VALUES ('Edificio A', 'Lab 101'), ('Edificio B', 'Oficina TI');