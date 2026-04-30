SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

INSERT INTO ROLES VALUES 
(null, 'Admin'),
(null, 'Almacen'),
(null, 'Tecnico'),
(null, 'Cliente');

INSERT INTO CITIES VALUES
(null, 'Bogotá'),
(null, 'Medellin'),
(null, 'Miami'),
(null, 'Barranquilla'),
(null, 'Cali'),
(null, 'Cartagena');


INSERT INTO USERS VALUES 
(1, null, 'Albeiro', 'Ramos', 'Villalba','3001112223', 'profealbeiro2020@gmail.com', 'KR 12 NO 20-245', sha1('12345'), 1, '2026-01-10', 2),
(1, null, 'Juan', 'Pérez', 'García', '3004567890', 'juan.perez1@example.com', 'Calle 123 #45-67', sha1('hash_password_1'), 1, '2026-01-20', 2),
(2, null, 'María', 'López', 'Rodríguez', '3112345678', 'maria.lopez23@example.com', 'Carrera 10 #20-30', sha1('hash_password_2'), 1, '2026-01-19', 2),
(2, null, 'María', 'López', 'Rodríguez', '3112345678', 'maria.lopez23@example.com', 'Carrera 10 #20-30', sha1('hash_password_2'), 1, '2026-01-19', 2),
(2, null, 'Carlos', 'García', 'Moreno', '3101112233', 'carlos.garcia@example.com', 'Calle 45 #12-30', sha1('hash_password_18'), 1, '2026-01-20', 2),
(2, null, 'Andrea', 'López', 'Pérez', '3124445566', 'andrea.lopez@example.com', 'Carrera 20 #5-18', sha1('hash_password_19'), 1, '2026-01-21', 2),
(2, null, 'Felipe', 'Ramírez', 'Torres', '3157778899', 'felipe.ramirez@example.com', 'Av. Siempre Viva 742', sha1('hash_password_20'), 1, '2026-01-22', 2),
(2, null, 'Paola', 'Martínez', 'Guzmán', '3163334455', 'paola.martinez@example.com', 'Transv. 56 #34-90', sha1('hash_password_21'), 1, '2026-01-23', 2),
(2, null, 'Jorge', 'Hernández', 'Suárez', '3176667788', 'jorge.hernandez@example.com', 'Cl. 100 #45-12', sha1('hash_password_22'), 1, '2026-01-24', 2),
(3, null, 'Carlos', 'Ramírez', 'Torres', '3229876543', 'carlos.ramirez45@example.com', 'Av. Siempre Viva 742', sha1('hash_password_3'), 1, '2026-01-18', 2),
(3, null, 'Ana', 'Torres', 'Martínez', '3012765432', 'ana.torres12@example.com', 'Calle 50 #10-25', sha1('hash_password_4'), 1, '2026-01-17', 2),
(3, null, 'Diana', 'Morales', 'Rincón', '3189990011', 'diana.morales@example.com', 'Bodega Central Km 7', sha1('hash_password_23'), 1, '2026-01-25', 2),
(3, null, 'Ricardo', 'Suárez', 'Castaño', '3192223344', 'ricardo.suarez@example.com', 'Cl. 80 #10-55', sha1('hash_password_24'), 1, '2026-01-26', 2),
(3, null, 'Lucía', 'Fernández', 'Quintero', '3205556677', 'lucia.fernandez@example.com', 'Carrera 15 #8-44', sha1('hash_password_25'), 1, '2026-01-27', 2),
(3, null, 'Santiago', 'Rojas', 'Bedoya', '3218889900', 'santiago.rojas@example.com', 'Cl. 30 #22-18', sha1('hash_password_26'), 1, '2026-01-28', 2),
(3, null, 'Valentina', 'Cárdenas', 'Prieto', '3221112233', 'valentina.cardenas@example.com', 'Zona Industrial 4', sha1('hash_password_27'), 1, '2026-01-29', 2),
(4, null, 'Luis', 'Gómez', 'Fernández', '3127654321', 'luis.gomez33@example.com', 'Carrera 30 #15-22', sha1('hash_password_5'), 1, '2026-01-16', 2),
(4, null, 'Juan', 'Perez', 'Lopez', '3151234567', 'juanperez@gmail.com', 'Calle 50 #10-25', sha1('5678'), 1, '2026-01-21', 2),
(4, null, 'Ana', 'Gomez', ',Martinez', '3109876543', 'anagomez@yahoo.com', 'Calle 50 #10-25', sha1('1234'), 1, '2026-01-10', 2),
(4, null, 'Carlos', 'Ruiz', 'Garcia', '3123456789', 'carlosr@hotmail.com', 'Calle 50 #10-25', sha1('8765'), 1, '2026-01-15', 2),
(4, null, 'Laura', 'Jimenez', 'Rodriguez', '3198765432', 'laurajim@gmail.com', 'Calle 50 #10-25', sha1('4321'), 1, '2026-01-30', 2),
(4, null, 'Pedro', 'Torres', 'Castillo', '3134567890', 'pedrotorres@mail.com', 'Calle 50 #10-25', sha1('9876'), 1, '2026-01-22', 2),
(4, null, 'Sofia', 'Fernandez', 'Mendez', '3145678901', 'sofiaf@hotmail.com', 'Calle 50 #10-25', sha1('3456'), 1, '2026-02-14', 2),
(4, null, 'Luis', 'Alvarez', 'Ortiz', '3167890123', 'luisalvarez@gmail.com', 'Calle 50 #10-25', sha1('6543'), 1, '2026-02-05', 2),
(4, null, 'Martha', 'Vargas', 'Ramos', '3178901234', 'marthav@yahoo.com', 'Calle 50 #10-25', sha1('7890'), 1, '2026-02-02', 2),
(4, null, 'Andres', 'Castro', 'Morales', '3189012345', 'andrescastro@mail.com', 'Calle 50 #10-25', sha1('2345'), 1, '2026-02-09', 2),
(4, null, 'Veronica', 'Medina', 'Salazar', '3190123456', 'veronicam@gmail.com', 'Calle 50 #10-25', sha1('6789'), 1, '2026-03-25', 2),
(4, null, 'Javier', 'Sanchez', 'Hernandez', '3101234567', 'javiers@yahoo.com', 'Calle 50 #10-25', sha1('3456'), 1, '2026-03-13', 2),
(4, null, 'Laura', 'Diaz', 'Vazquez', '3112345678', 'lauradiaz@gmail.com', 'Calle 50 #10-25', sha1('5678'), 1, '2026-04-03', 2),
(4, null, 'Miguel', 'Rojas', 'Castro', '3123456789', 'miguelr@mail.com', 'Calle 50 #10-25', sha1('4321'), 1, '2026-04-07', 2),
(4, null, 'Elena', 'Martinez', 'Sosa', '3134567890', 'elenam@hotmail.com', 'Calle 50 #10-25', sha1('1234'), 1, '2026-04-06', 2);


INSERT INTO CATEGORIES VALUES 
(null, 'Computadores', 'Computadores', '2026-01-01', 2),
(null, 'Televisores', 'Televisores', '2026-01-01', 2),
(null, 'Monitores', 'Monitores', '2026-01-01', 2),
(null, 'Impresoras', 'Impresoras', '2026-02-01', 2),
(null, 'Cámaras', 'Cámaras', '2026-02-01', 2),
(null, 'Servidores', 'Servidores', '2026-02-01', 2),
(null, 'Soportes', 'Soportes', '2026-02-01', 2),
(null, 'Teclados', 'Teclados', '2026-02-01', 2),
(null, 'Mouses', 'Mouses', '2026-02-01', 2),
(null, 'Auriculares', 'Auriculares', '2026-03-01', 2),
(null, 'Redes', 'Redes', '2026-03-01', 2),
(null, 'Discos Duros', 'Discos Duros', '2026-03-01', 2),
(null, 'Memorias RAM', 'Memorias RAM', '2026-03-01', 2);


INSERT INTO SUBCATEGORIES VALUES 
(null, 1, 'Portatiles', '2026-01-01', 2),
(null, 1, 'All in one', '2026-01-01', 2),
(null, 1, 'Torres', '2026-01-01', 2),
(null, 2, 'LCD', '2026-01-01', 2),
(null, 2, 'LED', '2026-01-01', 2),
(null, 2, 'OLED', '2026-01-01', 2),
(null, 2, 'QLED', '2026-01-01', 2),
(null, 3, 'TN', '2026-02-01', 2),
(null, 3, 'VA', '2026-02-01', 2),
(null, 3, 'IPS', '2026-02-01', 2),
(null, 3, 'OLED', '2026-02-01', 2),
(null, 4, 'Impresora a color', '2026-02-01', 2),
(null, 4, 'Impresora a laser', '2026-02-01', 2),
(null, 4, 'Impresora de tanques', '2026-02-01', 2),
(null, 4, 'Impresora a térmica', '2026-02-01', 2),
(null, 5, 'Camaras sin espejo', '2026-02-01', 2),
(null, 5, 'Camaras a réflex digitales', '2026-02-01', 2),
(null, 5, 'Camaras a compactas', '2026-02-01', 2),
(null, 5, 'Camaras de accion', '2026-02-01', 2),
(null, 5, 'Camaras de Instantáneas', '2026-02-01', 2),
(null, 5, 'Camaras de Teléfonos móviles', '2026-02-01', 2),
(null, 5, 'Camaras de Formato medio y gran formato', '2026-02-01', 2),
(null, 6, 'Servidores de Archivos', '2026-02-01', 2),
(null, 6, 'Servidores de torre', '2026-02-01', 2),
(null, 6, 'Servidores de rack', '2026-02-01', 2),
(null, 6, 'Servidores de blade', '2026-02-01', 2),
(null, 6, 'Servidores de miniatura', '2026-02-01', 2),
(null, 6, 'Servidores de Ultra densos', '2026-02-01', 2),
(null, 7, 'Soportes de articulados', '2026-02-01', 2),
(null, 7, 'Soporte de Fijos', '2026-02-01', 2),
(null, 8, 'Teclados Mecanicos', '2026-02-01', 2),
(null, 9, 'Mouse Gamers', '2026-02-01', 2),
(null, 10, 'Auriculares Gamers', '2026-02-01', 2),
(null, 11, 'Routers', '2026-03-01', 2),
(null, 11, 'Switches', '2026-03-01', 2),
(null, 11, 'Cables de red', '2026-03-01', 2),
(null, 12, 'HDD', '2026-03-01', 2),
(null, 12, 'SDD', '2026-03-01', 2),
(null, 12, 'NVMe', '2026-04-01', 2),
(null, 13, 'Memorias RAM DDR4', '2026-04-01', 2),
(null, 13, 'Memorias RAM DDR5', '2026-04-01', 2);


INSERT INTO PRODUCT_BRANDS VALUES
(null, 'Zebra'),
(null, 'Canon'),
(null, 'Epson'),
(null, 'Hp'),
(null, 'Brother'),
(null, 'Makita'),
(null, 'LG'),
(null, 'Samsung'),
(null, 'Sony'),
(null, 'Lenovo'),
(null, 'Asus'),
(null, 'Panasonic'),
(null, 'Ricoh'),
(null, 'Genius'),
(null, 'Challenger'),
(null, 'WESTERN DIGITAL WD'),
(null, 'Kioxia'),
(null, 'Kingston'),
(null, 'Crucial'),
(null, 'Logitech'),
(null, 'Razer'),
(null, 'HyperX'),
(null, 'TP-Link'),
(null, 'Cisco'),
(null, 'Apple');

INSERT INTO PRODUCT_MODELS VALUES
(null, 'Zebra ZD420', 'Impresora térmica para puntos de venta', 1),
(null, 'HP 110', 'Impresora térmica compacta para etiquetas', 4),
(null, 'Epson TM-T20', 'Impresora térmica rápida y eficiente', 3),
(null, 'Epson L3150', 'Multifuncional con sistema de tinta continua', 3),
(null, 'Canon G2010', 'Impresora continua con escáner', 2),
(null, 'HP Ink Tank 415', 'Impresora con tinta recargable inalámbrica', 4),
(null, 'LaserJet Pro M15w', 'Impresora láser compacta y rápida', 4),
(null, 'Brother HL-L2350DW', 'Impresora láser monocromo', 5),
(null, 'Samsung Xpress M2020W', 'Impresora láser inalámbrica', 8),
(null, 'QLED 55Q60A', 'Smart TV Samsung de 55" con resolución 4K', 8),
(null, 'Bravia XR-55A80K', 'Sony Smart TV OLED 55" 4K', 9),
(null, 'LED TV 43LM6370', 'LG TV LED 43" Full HD', 7),
(null, 'OLED TV 65C1', 'TV OLED LG 65" 4K UHD', 7),
(null, 'WD My Passport 1TB', 'Disco duro externo portátil con USB 3.0', 16),
(null, 'Logitech MX Keys', 'Teclado inalámbrico retroiluminado', 20),
(null, 'Razer DeathAdder V2', 'Mouse gamer ergonómico', 21),
(null, 'HyperX Cloud II', 'Auriculares gamer con sonido envolvente', 22),
(null, 'TP-Link Archer AX50', 'Router WiFi 6 de alta velocidad', 23),
(null, 'Cisco SG350-28', 'Switch gestionable de 28 puertos', 24),
(null, 'Cable Cat6 UTP', 'Cable de red de 2 metros', 24),
(null, 'Lenovo ThinkPad X1 Carbon', 'Portátil ultraligero con procesador Intel i7 y 16GB RAM', 10),
(null, 'Asus ROG Strix G15', 'Laptop gamer con RTX 3060 y 16GB RAM', 11),
(null, 'MacBook Pro 14"', 'Laptop Apple con chip M1 Pro y pantalla Retina', 25),
(null, 'LG NanoCell 55NANO80', 'Smart TV LG 55” con tecnología NanoCell 4K', 7),
(null, 'Kioxia Exceria 500GB', 'Disco SSD NVMe de alta velocidad', 17),
(null, 'Kingston Fury Beast 16GB DDR4', 'Memoria RAM para alto rendimiento', 18),
(null, 'Crucial Ballistix 32GB DDR5', 'Memoria RAM DDR5 para gaming y servidores', 19),
(null, 'Logitech G Pro X', 'Teclado mecánico gamer con switches intercambiables', 20),
(null, 'Razer Viper Ultimate', 'Mouse inalámbrico gamer ultraligero con 20K DPI', 21),
(null, 'HyperX Alpha Wireless', 'Auriculares inalámbricos gamer con batería de 300h', 22),
(null, 'TP-Link Deco X60', 'Sistema WiFi Mesh con cobertura para hogares grandes', 23),
(null, 'Cisco Catalyst 9300', 'Switch empresarial de alto rendimiento', 24);



INSERT INTO PRODUCT_DETAILS VALUES
(null, 1, '2026-01-05'),
(null, 2, '2026-01-05'),
(null, 3, '2026-01-05'),
(null, 4, '2026-03-05'),
(null, 5, '2026-03-05'),
(null, 6, '2026-03-05'),
(null, 7, '2026-03-05'),
(null, 8, '2026-03-05'),
(null, 9, '2026-03-05'),
(null, 10, '2026-03-05'),
(null, 11, '2026-04-05'),
(null, 12, '2026-04-05'),
(null, 13, '2026-04-05'),
(null, 14, '2026-04-05'),
(null, 15, '2026-04-05'),
(null, 16, '2026-04-05'),
(null, 17, '2026-04-05'),
(null, 18, '2026-04-05'),
(null, 19, '2026-04-05'),
(null, 20, '2026-04-05'),
(null, 21, '2026-04-05'),
(null, 22, '2026-04-05'),
(null, 23, '2026-04-05'),
(null, 24, '2026-04-05'),
(null, 25, '2026-04-05'),
(null, 26, '2026-04-05'),
(null, 27, '2026-04-05'),
(null, 28, '2026-04-05'),
(null, 29, '2026-04-05'),
(null, 30, '2026-04-05'),
(null, 31, '2026-04-05'),
(null, 32, '2026-04-05');


INSERT INTO PRODUCTS VALUES 
(null, 15, 1, 2),    -- HP 110 .
(null, 15, 2, 1),    -- Zebra ZD420 
(null, 15, 3, 3),    -- Epson TM-T20 
(null, 12, 4, 4),    -- Epson L3150 
(null, 12, 5, 2),    -- Canon G2010 
(null, 12, 6, 2),    -- HP Ink Tank 415 
(null, 13, 7, 2),    -- LaserJet Pro 
(null, 13, 8, 2),    -- Brother HL 
(null, 13, 9, 2),    -- Samsung Xpress 
(null, 7, 10, 2),    -- QLED Samsung
(null, 6, 11, 2),    -- Bravia Sony 
(null, 5, 12, 2),    -- LG LED 
(null, 6, 13, 2),    -- LG OLED 
(null, 37, 14, 2),   -- WD My Passport 
(null, 31, 15, 2),   -- Logitech MX Keys 
(null, 32, 16, 2),   -- Razer DeathAdder 
(null, 33, 17, 2),   -- HyperX Cloud II 
(null, 34, 18, 2),   -- TP-Link Router 
(null, 35, 19, 2),   -- Cisco Switch 
(null, 36, 20, 2),  -- Cables Cat6 
(null, 1, 21, 2),    -- Lenovo ThinkPad 
(null, 1, 22, 2),    -- Asus ROG Strix 
(null, 1, 23, 2),    -- MacBook Pro 
(null, 4, 24, 2),    -- LG NanoCell TV
(null, 38, 25, 2),   -- Kioxia SSD
(null, 40, 26, 2),   -- Kingston RAM
(null, 41, 27, 2),   -- Crucial DDR5
(null, 32, 28, 2),   -- Logitech G Pro X
(null, 32, 29, 2),   -- Razer Viper Ultimate
(null, 33, 30, 2),   -- HyperX Alpha Wireless
(null, 34, 31, 2),   -- TP-Link Deco Mesh
(null, 35, 32, 2);   -- Cisco Catalyst


INSERT INTO SUPPLIERS VALUES
(null, 'Asus', 1,'Carrera 30 # 15 - 299', 'asus@asus.com', '1000000112', '2026-01-01', 2),
(null, 'Servicios Industriales', 1, 'Cra 50 #25-60, Barranquilla', 'contacto@sic.com', '3019873210', '2026-01-01', 2),
(null, 'Lenovo', 1, '1234 NW 107th Avenue, Miami, FL 33172', 'lenovo@lenovo.com', '3012141562', '2026-01-01', 2),
(null, 'Logitech', 1, 'Cra 45 #12-30', 'ventas@logitech.com', '3021234567', '2026-01-01', 2),
(null, 'Cisco', 1, 'Av. El Dorado #25-80', 'ventas@cisco.com', '3186543210', '2026-01-01', 2),
(null, 'TP-Link', 1, 'Cl. 5 #15-22', 'soporte@tplink.com', '3009998887', '2026-01-01', 2),
(null, 'Microsoft', 1, 'Cra 15 # 45-20', 'soporte@microsoft.com', '3104442233', '2026-01-01', 2),
(null, 'Razer', 1, 'Cl. 50 #30-12', 'contact@razer.com', '3115556677', '2026-01-01', 2),
(null, 'HyperX', 1, 'Av. 6N # 34-50', 'ventas@hyperx.com', '3129998877', '2026-02-01', 2),
(null, 'Crucial', 1, 'Zona Franca Industrial', 'sales@crucial.com', '3131112233', '2026-02-01', 2),
(null, 'Kingston', 1, '1234 Kingston Blvd', 'contact@kingston.com', '3145557788', '2026-02-01', 2),
(null, 'Western Digital', 1, 'Av. 68 #45-80', 'support@wd.com', '3157778899', '2026-02-01', 2),
(null, 'Sony', 1, 'Cl. 10 #20-33', 'ventas@sony.com', '3168889900', '2026-02-01', 2),
(null, 'LG', 1, 'Cra 45 # 25-15', 'lg@lg.com', '3172223344', '2026-03-01', 2),
(null, 'Samsung', 1, 'Cl. 26 #92-32', 'ventas@samsung.com', '3183334455', '2026-03-01', 2),
(null, 'Mayorista', 1, 'CL 124 #15-245', 'mayorista@mayorista.com', '3401232255', '2026-04-01', 2),
(null, 'HP', 1, 'Avenida El Dorado # 68C - 61', 'hp@hp.com', '1000000113', '2026-04-02', 2),
(null, 'Canon', 1, 'Calle 50 # 40 - 25', 'canon@canon.com', '1000000114', '2026-04-03', 2);


INSERT INTO INPUT_ORDERS VALUES
(null, 16, 'INP00001', '2024-01-05'),
(null, 2, 'INP00002', '2024-01-05'),
(null, 16, 'INP00002', '2024-01-05'),
(null, 16, 'INP00003', '2024-02-10'),
(null, 18, 'INP00005', '2024-02-15'),
(null, 17, 'INP00006', '2024-03-18'),
(null, 2, 'INP00007', '2024-03-20'),
(null, 2, 'INP00008', '2024-03-22'),
(null, 1, 'INP00009', '2024-03-25'),
(null, 2, 'INP00010', '2024-04-28'),
(null, 15, 'INP00011', '2024-04-01'),
(null, 16, 'INP00012', '2024-04-05'),
(null, 2, 'INP00013', '2024-05-08'),
(null, 2, 'INP00014', '2024-05-10'),
(null, 12, 'INP00015', '2024-05-15'),
(null, 4, 'INP00016', '2024-06-20'),
(null, 8, 'INP00017', '2024-06-25'),
(null, 2, 'INP00018', '2024-06-26'),
(null, 2, 'INP00019', '2024-07-01'),
(null, 5, 'INP00020', '2024-07-05'),
(null, 11, 'INP00021', '2024-07-15'),
(null, 9, 'INP00022', '2024-07-15'),
(null, 5, 'INP00023', '2024-07-15'),
(null, 10, 'INP00024', '2024-07-15'),
(null, 1, 'INP00025', '2024-07-15'),
(null, 3, 'INP00026', '2024-07-15');



INSERT INTO PRODUCT_SERIALS VALUES
('QTYC1123122', 1,  1, '2027-08-25'),
('QTYC2123123', 2,  1, '2027-08-20'),
('QTYC1223122', 14, 2, '2028-12-29'),
('QTYA9876543', 15, 3, '2029-01-15'),
('QTYB5554441', 3,  3, '2029-02-01'),
('QTYC3332220', 4,  4, '2029-02-10'),
('QTYD1234567', 5,  5, '2029-03-05'),
('QTYE9876543', 6,  6, '2029-03-20'),
('QTYF1112223', 7,  7, '2029-04-01'),
('QTYG7778889', 8,  8, '2029-04-18'),
('QTYH5556667', 9,  10, '2029-05-01'),
('QTYI9990001', 9, 10, '2029-05-15'),
('QTYJ1234567', 10, 11, '2029-06-01'),
('QTYK7654321', 11, 12, '2029-06-10'),
('QTYL9876543', 12, 13, '2029-06-25'),
('QTYM5556667', 13, 14, '2029-07-08'),
('QTYN1234567', 14, 15, '2030-01-01'),
('QTYO9876543', 15, 16, '2030-02-01'),
('QTYP5554441', 16, 17, '2030-03-01'),
('QTYQ3332220', 17, 18, '2030-04-01'),
('QTYR1234567', 18, 19, '2030-05-01'),
('QTYS7654321', 19, 20, '2030-06-01'),
('QTYS1234567', 20, 2, '2030-06-01'),
('QTYS9876543', 21, 26, '2030-06-01'),
('QTYS2468135', 22, 25, '2030-06-01'),
('QTYS1357924', 23, 2, '2030-06-01'),
('QTYS5647382', 24, 19, '2030-06-01'),
('QTYS1928374', 25, 19, '2030-06-01'),
('QTYS7654329', 26, 21, '2030-06-01'),
('QTYS9081726', 27, 24, '2030-06-01'),
('QTYS3847561', 28, 16, '2030-06-01'),
('QTYS6574830', 29, 17, '2030-06-01'),
('QTYS4829157', 30, 22, '2030-06-01'),
('QTYS7302648', 31, 23, '2030-06-01'),
('QTYS7300111', 32, 23, '2030-06-01');


INSERT INTO OUTPUT_ORDERS VALUES
(null, '2026-01-24', 2),
(null, '2026-01-22', 2),
(null, '2026-01-10', 2),
(null, '2026-01-15', 2),
(null, '2026-01-30', 2),
(null, '2026-02-18', 2),
(null, '2026-02-21', 2),
(null, '2026-02-12', 1),
(null, '2026-02-28', 2),
(null, '2026-03-05', 1),
(null, '2026-03-12', 2),
(null, '2026-03-09', 2),
(null, '2026-03-01', 2),
(null, '2026-04-07', 2),
(null, '2026-04-08', 2); 


INSERT INTO CUSTOMERS VALUES
(17, 1),
(17, 2),
(17, 3),
(18, 4),
(19, 5),
(20, 6),
(21, 7),
(22, 8),
(23, 9),
(24, 10),
(24, 11),
(26, 12),
(27, 13),
(28, 14),
(29, 15);


INSERT INTO OUTPUT_DETAILS VALUES
(1, 'QTYC1123122', null, '2028-12-29', 'No necesita'),
(2, 'QTYA9876543', null, '2029-01-15', 'Entregado'),
(3, 'QTYB5554441', null, '2029-02-01', 'Pendiente de revisión'),
(4, 'QTYC3332220', null, '2029-02-10', 'En ruta'),
(5, 'QTYD1234567', null, '2029-03-05', 'Entregado'),
(6, 'QTYE9876543', null, '2029-03-20', 'No necesita'),
(7, 'QTYF1112223', null, '2029-04-01', 'Pendiente de revisión'),
(8, 'QTYG7778889', null, '2029-04-18', 'En ruta'),
(9, 'QTYH5556667', null, '2029-05-01', 'Entregado'),
(10, 'QTYI9990001', null, '2029-05-15', 'No necesita'),
(11, 'QTYJ1234567', null, '2029-06-01', 'En ruta'),
(12, 'QTYK7654321', null, '2029-06-10', 'Pendiente de revisión'),
(13, 'QTYL9876543', null, '2029-06-25', 'Entregado'),
(14, 'QTYM5556667', null, '2029-07-08', 'No necesita'),
(15, 'QTYS7654329', null, '2029-07-09', 'No necesita');


INSERT INTO WARRANTY_INCIDENTS VALUES
(null, 'QTYC1123122', 'Juan Perez', '3008765432', 'Calle 50 #10-25', 'Problema con la impresión', '../warranties/images/WINC0001', 'Miami', '2026-01-15', 3),
(null, 'QTYA9876543', 'Ana Gomez', '3008765432', 'Calle 50 #10-25', 'Problema con la impresión', '../warranties/images/WINC0001', 'Miami', '2026-01-15', 3),
(null, 'QTYB5554441', 'Carlos Ruiz', '3002223344', 'Calle 80 #45-10', 'Teclado no enciende retroiluminación', '../warranties/images/WINC0002', 'Bogotá', '2026-01-01', 3),
(null, 'QTYC3332220', 'Laura Jimenez', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-01-02', 3),
(null, 'QTYD1234567', 'Laura Jimenez', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-01-02', 1),
(null, 'QTYE9876543', 'Laura Jimenez', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-01-02', 1),
(null, 'QTYF1112223', 'Pedro Torres', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-02-02', 1),
(null, 'QTYG7778889', 'Sofia Fernandez', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-02-02', 2),
(null, 'QTYH5556667', 'Luiz Alvarez', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-03-02', 2),
(null, 'QTYI9990001', 'Martha Vargas', '3015556677', 'Carrera 15 #22-55', 'Mouse con sensor defectuoso', '../warranties/images/WINC0003', 'Medellín', '2026-04-02', 2);


INSERT INTO TECHNICAL VALUES
(10, 1),
(10, 2),
(10, 3),
(11, 4),
(12, 5),
(13, 6),
(14, 7),
(15, 8),
(16, 9);


INSERT INTO WAREHAUSEMAN VALUES
(3, 1),
(4, 2),
(5, 3),
(6, 4),
(7, 5),
(8, 6),
(9, 7);