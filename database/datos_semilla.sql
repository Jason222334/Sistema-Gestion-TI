-- Limpiar datos existentes (opcional, para evitar duplicados si lo corres varias veces)
TRUNCATE TABLE notificaciones, movimientos_equipos, mantenimientos, contratos, equipos, usuarios, proveedores, ubicaciones, categorias_equipos RESTART IDENTITY CASCADE;

-- 1. Insertar Categorías
INSERT INTO categorias_equipos (nombre, vida_util_anos, descripcion) VALUES 
('Laptops', 4, 'Computadoras portátiles para personal y laboratorios'),
('Desktops', 5, 'Computadoras de escritorio para administración'),
('Servidores', 7, 'Equipos de centro de datos'),
('Impresoras', 5, 'Impresoras láser y multifuncionales'),
('Redes', 6, 'Switches, Routers y Access Points'),
('Periféricos', 3, 'Monitores, teclados, mouse');

-- 2. Insertar Ubicaciones
INSERT INTO ubicaciones (edificio, piso, aula_oficina, descripcion) VALUES 
('Edificio A', '1', 'Lab 101', 'Laboratorio de Computación General'),
('Edificio A', '2', 'Aula 204', 'Aula Multimedia'),
('Edificio B', '1', 'Oficina TI', 'Centro de Datos y Soporte'),
('Edificio B', '3', 'Administración', 'Oficinas Administrativas'),
('Biblioteca', '1', 'Sala de Lectura', 'Computadoras de consulta');

-- 3. Insertar Proveedores
INSERT INTO proveedores (razon_social, ruc, direccion, telefono, email, contacto_nombre, sitio_web) VALUES 
('Tecnología Global S.A.', '20123456789', 'Av. Tecnológica 123', '555-0101', 'ventas@tecglobal.com', 'Juan Perez', 'www.tecglobal.com'),
('CompuMundo Import', '20987654321', 'Jr. Hardware 456', '555-0202', 'contacto@compumundo.com', 'Maria Garcia', 'www.compumundo.com'),
('Redes y Soluciones', '20555666777', 'Calle Conectividad 789', '555-0303', 'soporte@redessoluciones.com', 'Carlos Lopez', 'www.redessoluciones.com');

-- 4. Insertar Usuarios
INSERT INTO usuarios (username, email, nombre_completo, rol) VALUES 
('admin', 'admin@universidad.edu', 'Administrador del Sistema', 'admin'),
('jrodriguez', 'jrodriguez@universidad.edu', 'Juan Rodriguez', 'tecnico'),
('mlopez', 'mlopez@universidad.edu', 'Marta Lopez', 'docente'),
('soporte1', 'soporte1@universidad.edu', 'Tecnico de Soporte 1', 'tecnico');

-- 5. Insertar Equipos (Variedad de estados para el Dashboard)
INSERT INTO equipos (codigo_inventario, nombre, marca, modelo, numero_serie, categoria_id, proveedor_id, fecha_compra, costo_compra, fecha_garantia_fin, ubicacion_actual_id, estado_operativo, asignado_a_id) VALUES 
-- Laptops Operativas
('LAP-001', 'Laptop Dell Latitude', 'Dell', 'Latitude 5420', 'SN001', 1, 1, CURRENT_DATE - INTERVAL '6 months', 1200.00, CURRENT_DATE + INTERVAL '2 years', 3, 'operativo', 2),
('LAP-002', 'Laptop HP ProBook', 'HP', 'ProBook 450', 'SN002', 1, 1, CURRENT_DATE - INTERVAL '1 year', 1100.00, CURRENT_DATE + INTERVAL '1 year', 3, 'operativo', 4),
-- Desktops en Laboratorio
('PC-101', 'Desktop Lenovo ThinkCentre', 'Lenovo', 'M70q', 'SN101', 2, 2, CURRENT_DATE - INTERVAL '2 years', 850.00, CURRENT_DATE + INTERVAL '1 year', 1, 'operativo', NULL),
('PC-102', 'Desktop Lenovo ThinkCentre', 'Lenovo', 'M70q', 'SN102', 2, 2, CURRENT_DATE - INTERVAL '2 years', 850.00, CURRENT_DATE + INTERVAL '1 year', 1, 'operativo', NULL),
('PC-103', 'Desktop Lenovo ThinkCentre', 'Lenovo', 'M70q', 'SN103', 2, 2, CURRENT_DATE - INTERVAL '2 years', 850.00, CURRENT_DATE + INTERVAL '1 year', 1, 'en_reparacion', NULL),
-- Servidor
('SRV-001', 'Servidor Dell PowerEdge', 'Dell', 'R740', 'SN999', 3, 1, CURRENT_DATE - INTERVAL '3 years', 5000.00, CURRENT_DATE - INTERVAL '1 month', 3, 'operativo', 1),
-- Impresora con problemas
('PRN-001', 'Impresora HP LaserJet', 'HP', 'M404n', 'SNPRN1', 4, 2, CURRENT_DATE - INTERVAL '4 years', 400.00, CURRENT_DATE - INTERVAL '1 year', 4, 'en_reparacion', NULL),
-- Equipos Obsoletos
('PC-OLD-01', 'PC Pentium Dual Core', 'Generic', 'Clone', 'OLD001', 2, 2, CURRENT_DATE - INTERVAL '8 years', 300.00, CURRENT_DATE - INTERVAL '7 years', 2, 'obsoleto', NULL),
('LAP-OLD-01', 'Laptop Toshiba Satellite', 'Toshiba', 'A200', 'OLD002', 1, 2, CURRENT_DATE - INTERVAL '10 years', 600.00, CURRENT_DATE - INTERVAL '9 years', 2, 'dado_baja', NULL);

-- 6. Insertar Mantenimientos (Pasados y Futuros para alertas)
INSERT INTO mantenimientos (equipo_id, tipo, fecha_programada, fecha_realizada, descripcion, costo, estado, prioridad) VALUES 
-- Mantenimiento completado
(1, 'preventivo', CURRENT_DATE - INTERVAL '3 months', CURRENT_DATE - INTERVAL '3 months', 'Limpieza general y actualización', 50.00, 'completado', 'media'),
-- Mantenimiento programado PRÓXIMO (Alerta de 7 días)
(2, 'preventivo', CURRENT_DATE + INTERVAL '5 days', NULL, 'Mantenimiento semestral programado', 0.00, 'programado', 'media'),
-- Mantenimiento URGENTE (Alerta de 3 días o vencido)
(5, 'correctivo', CURRENT_DATE - INTERVAL '2 days', NULL, 'Falla en disco duro principal', 0.00, 'programado', 'urgente'),
-- Mantenimiento futuro lejano
(3, 'preventivo', CURRENT_DATE + INTERVAL '2 months', NULL, 'Revisión anual', 0.00, 'programado', 'baja');

-- 7. Insertar Contratos
INSERT INTO contratos (proveedor_id, numero_contrato, tipo, fecha_inicio, fecha_fin, monto_total, estado, descripcion) VALUES 
(1, 'CTR-2024-001', 'Soporte y Garantía', CURRENT_DATE - INTERVAL '6 months', CURRENT_DATE + INTERVAL '6 months', 12000.00, 'vigente', 'Contrato de soporte técnico anual'),
(2, 'CTR-2023-099', 'Adquisición Lote 2', CURRENT_DATE - INTERVAL '18 months', CURRENT_DATE - INTERVAL '6 months', 25000.00, 'vencido', 'Compra de equipos de laboratorio');

-- 8. Insertar Movimientos
INSERT INTO movimientos_equipos (equipo_id, ubicacion_origen_id, ubicacion_destino_id, usuario_responsable_id, motivo, observaciones) VALUES 
(1, 3, 2, 2, 'Préstamo para clase', 'Devolver al finalizar el día'),
(5, 1, 3, 1, 'Traslado a taller por falla', 'Disco duro haciendo ruido');