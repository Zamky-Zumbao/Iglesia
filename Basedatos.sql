-- PRODUCTOS
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 4,  -- ← valor crítico
    unidad TEXT DEFAULT 'unidades',
    ubicacion TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- MOVIMIENTOS
CREATE TABLE movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    tipo TEXT CHECK(tipo IN ('ENTRADA', 'SALIDA', 'AJUSTE')),
    cantidad INTEGER,
    stock_anterior INTEGER,
    stock_nuevo INTEGER,
    motivo TEXT,
    documento TEXT,  -- factura/guía
    usuario_id INTEGER,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- USUARIOS
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol TEXT CHECK(rol IN ('ADMIN', 'ENCARGADO')),
    clave TEXT,
    activo BOOLEAN DEFAULT 1
);

-- CONFIGURACIÓN (valores por defecto)
CREATE TABLE configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT UNIQUE,
    valor TEXT,
    descripcion TEXT
);

-- Insertar configuración inicial
INSERT INTO configuracion (clave, valor, descripcion) 
VALUES ('stock_critico', '4', 'Valor mínimo para alerta crítica');