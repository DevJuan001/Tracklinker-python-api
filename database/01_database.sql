SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

DROP DATABASE IF EXISTS DB_TRACKLINKER;

CREATE SCHEMA DB_TRACKLINKER DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE DB_TRACKLINKER;

-- -----------------------------------------------------
-- Table ROLS
-- -----------------------------------------------------
CREATE TABLE ROLES (
  rol_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autogenerado para cada rol, llave primaria (INT, Not null))',
  rol_name VARCHAR(100) NOT NULL COMMENT 'Nombre de cada rol, De caracter obligatorio para poder clasificar cada rol (Varchar (45), Not null)',
  PRIMARY KEY (rol_id),
  UNIQUE INDEX rol_id_UNIQUE (rol_id ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table CITIES
-- -----------------------------------------------------

CREATE TABLE CITIES (
  city_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autgenerado para cada rol',
  city_name TEXT NOT NULL COMMENT 'Nombre de cada ciudad',
  PRIMARY KEY (city_id),
  UNIQUE INDEX city_id_UNIQUE (city_id ASC)
)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table USERS
-- -----------------------------------------------------
CREATE TABLE USERS (
  rol_id INT NOT NULL COMMENT 'Identificador autogenerado para cada rol (INT, Not null)',
  user_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autogenerado para cada usuario, Llave primaria (INT, Not null)',
  user_name VARCHAR(255) NOT NULL COMMENT ' (VARCHAR, Not null)',
  user_first_surname VARCHAR(255) NOT NULL COMMENT 'Primer apellido del usuario, se separa el apellido en dos partes para que al momento de hacer búsquedas sea más sencillo encontrar el usuario (VARCHAR, Not null)',
  user_second_surname VARCHAR(255) NOT NULL COMMENT 'Segundo apellido del usuario (VARCHAR, Not null)',
  user_phone VARCHAR(255) NOT NULL COMMENT 'Número de teléfono del usuario (VARCHAR, Not null)',
  user_email VARCHAR(255) NOT NULL COMMENT 'Correo electrónico del usuario (VARCHAR, Not null)',
  user_address VARCHAR(255) NOT NULL COMMENT 'Dirección del usuario (VARCHAR, Not null)',
  user_password VARCHAR(255) NOT NULL COMMENT 'Contrasena del usuario, se debe almacenar hasheada para mayor seguridad (VARCHAR, Not null)',
  user_city INT NOT NULL COMMENT 'Ciudad en la que se encuentra el usuario',
  user_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del usuario (DATE, Not null)',
  user_status INT NOT NULL DEFAULT 2 COMMENT "Estado en el que se encuentra el usuario 1 = deshabilitado, 2 = activo",
  PRIMARY KEY (user_id),
  INDEX fk_rol_users_idx (rol_id ASC),
  UNIQUE INDEX users_id_UNIQUE (user_id ASC),
  CONSTRAINT fk_rol_user
    FOREIGN KEY (rol_id)
    REFERENCES ROLES (rol_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_city_user
    FOREIGN KEY (user_city)
    REFERENCES CITIES (city_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table PRODUCT_BRAND
-- -----------------------------------------------------
CREATE TABLE PRODUCT_BRANDS (
  product_brand_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador de marca de producto\n.\nClave primaria única que identifica cada marca registrada en el sistema. Este campo se genera automáticamente de forma secuencial y no puede repetirse ni quedar vacío. Se utiliza para establecer una relación entre los productos y sus marcas correspondientes.',
  product_brand_name TEXT NOT NULL COMMENT 'Nombre de la marca del producto\n.\nNombre oficial o comercial de la marca asociada a un producto. Este campo permite identificar y categorizar los productos por su fabricante, proveedor o casa comercial. Es obligatorio para asegurar que cada marca registrada tenga un nombre definido.',
  PRIMARY KEY (product_brand_id),
  UNIQUE INDEX product_brand_id_UNIQUE (product_brand_id ASC))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table PRODUCT_MODELS
-- -----------------------------------------------------
CREATE TABLE PRODUCT_MODELS (
  product_model_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador del modelo de producto',
  product_model_name TEXT NOT NULL COMMENT 'Nombre de la modelo del producto',
  product_model_description TEXT NOT NULL COMMENT 'Descripcion detallada del producto',
  product_brand_id INT NOT NULL COMMENT 'Marca a la que pertenece este modelo',
  PRIMARY KEY (product_model_id),
  UNIQUE INDEX product_model_id_UNIQUE (product_model_id ASC),
  INDEX fk_product_models_product_brand_idx (product_brand_id ASC),
  CONSTRAINT fk_product_details_product_brand
    FOREIGN KEY (product_brand_id)
    REFERENCES PRODUCT_BRANDS (product_brand_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table PRODUCT_DETAILS
-- -----------------------------------------------------
CREATE TABLE PRODUCT_DETAILS (
  product_details_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador de la lista de detalles del producto, llave primaria que identifica para lista de detalles (INT, Not null)',
  product_model_id INT NOT NULL COMMENT 'Modelo que tiene o maneja el producto, Se utiliza para diferenciarlo de otros productos o indicar los productos similares',
  product_detail_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha en la que se agrego el producto',
  PRIMARY KEY (product_details_id),
  INDEX fk_product_details_product_model_idx (product_model_id ASC),
  CONSTRAINT fk_product_details_product_model
    FOREIGN KEY (product_model_id)
    REFERENCES PRODUCT_MODELS (product_model_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table OUTPUT_ORDER
-- -----------------------------------------------------
CREATE TABLE OUTPUT_ORDERS (
  out_order_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autogenerado de las ordenes de salida (INT, Not null)',
  out_order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación de la orden de salida, se usa para manejar control de las salidas (DATE, Not null)',
  out_order_status INT NOT NULL DEFAULT 2 COMMENT "Estado en el que se encuentra la orden, 1 = Deshabilitada, 2 = Habilitada",
  PRIMARY KEY (out_order_id)
  )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table CUSTOMERS
-- -----------------------------------------------------
CREATE TABLE CUSTOMERS (
  user_id INT NOT NULL COMMENT 'Identifica de forma única a cada cliente. Not null',
  out_order_id INT NOT NULL COMMENT 'Identificador único de orden externa (proveniente de sistemas partners). Not null',
  INDEX fk_customers_id_out_order_id (user_id ASC),
  INDEX fk_customers_out_order_idx (out_order_id ASC),
  CONSTRAINT fk_customers_users
    FOREIGN KEY (user_id)
    REFERENCES USERS (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_customers_out_order
    FOREIGN KEY (out_order_id)
    REFERENCES OUTPUT_ORDERS (out_order_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table SUPPLIERS
-- -----------------------------------------------------
CREATE TABLE SUPPLIERS (
  supplier_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autogenerado para cada proveedor, llave primaria (INT, Not null)',
  supplier_name VARCHAR(255) NOT NULL COMMENT 'Nombre del proveedor (VARCHAR, Not null)',
  supplier_city VARCHAR(255) NOT NULL COMMENT 'Ciudad donde esta ubicado el proveedor (VARCHAR, Not null)',
  supplier_address VARCHAR(255) NOT NULL COMMENT 'Dirección del proveedor (VARCHAR, Not null)',
  supplier_email VARCHAR(255) NOT NULL COMMENT 'Correo electronico del proveedor (VARCHAR, Not null)',
  supplier_phone VARCHAR(255) NOT NULL COMMENT 'Número de teléfono del proveedor (VARCHAR, Not null)',
  supplier_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del proveedor (DATE, Not null)',
  supplier_status INT NOT NULL DEFAULT 2 COMMENT "Estado en el que se encuentra el proveedor 1 = deshabilitado, 2 = activo",
  PRIMARY KEY (supplier_id))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table INPUT_ORDER
-- -----------------------------------------------------
CREATE TABLE INPUT_ORDERS (
  input_order_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador único autogenerado para órdenes de entrada (PK). Clave primaria autoincremental. Requerido para todas las transacciones (NOT NULL, UNIQUE).',
  supplier_id INT NOT NULL COMMENT 'Identificador del proveedor asociado a la orden. not null ',
  input_order_bill VARCHAR(255) NOT NULL COMMENT 'Identificador único de factura (PK). Clave primaria para registro de documentos de compra. Requerido para todas las transacciones (NOT NULL).',
  input_order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha/hora de creación de la orden. Requerido por políticas de auditoría (NOT NULL). Captura automática del sistema',
  PRIMARY KEY (input_order_id, input_order_bill),
  UNIQUE INDEX idINPUT_ORDER_UNIQUE (input_order_id ASC),
  INDEX fk_input_order_supplier_idx ( supplier_id ASC),
  CONSTRAINT fk_input_order_supplier
    FOREIGN KEY (supplier_id)
    REFERENCES SUPPLIERS (supplier_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table CATEGORY
-- -----------------------------------------------------
CREATE TABLE CATEGORIES (
  category_id INT NOT NULL AUTO_INCREMENT COMMENT 'Es un Identificador único autogenerado para cada categoría de producto, (INT, Not null)',
  category_name VARCHAR(100) NOT NULL COMMENT 'Identificar y clasificar los productos tecnológicos en el sistema.',
  category_description TEXT NOT NULL COMMENT 'Razón por la cual la categoria fue creada o que tipo de productos almacena',
  category_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  category_status INT NOT NULL DEFAULT 2 COMMENT 'Estado 1 = deshabilitado, 2 = activa',
  UNIQUE INDEX category_id_UNIQUE (category_id ASC),
  PRIMARY KEY (category_id))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table SUBCATEGORY
-- -----------------------------------------------------
CREATE TABLE SUBCATEGORIES (
  subcategory_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador autogenerado de cada subcategoria (INT, Not null)',
  category_id INT NOT NULL COMMENT 'Es un Identificador único autogenerado para cada categoría de producto, (INT, Not null)',
  subcategory_name VARCHAR(100) NOT NULL COMMENT 'Nombre de cada subcategoria (VARCHAR, Not null)',
  subcategory_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subcategory_status INT NOT NULL DEFAULT 2 COMMENT 'Estado 1 = deshabilitado, 2 = activa',
  PRIMARY KEY (subcategory_id),
  UNIQUE INDEX subcategory_id_UNIQUE (subcategory_id ASC),
  INDEX fk_subcategory_category_idx (category_id ASC),
  CONSTRAINT fk_subcategory_category
    FOREIGN KEY (category_id)
    REFERENCES CATEGORIES (category_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table PRODUCTS
-- -----------------------------------------------------
CREATE TABLE PRODUCTS (
  product_id INT NOT NULL AUTO_INCREMENT COMMENT 'Identificador de cada producto, El cúal sirve para relacionar los productos con su respectivo serial (INT, Not Null, Auto Increment)',
  subcategory_id INT NOT NULL COMMENT 'Identificador de cada Subcategoria, Este campo sirve para relacionar los productos con las subcategorias y poder clasificarlos según el grupo que los agrupe (INT, Not null)',
  product_details_id INT NOT NULL COMMENT 'Identificador de detalles del producto\n.\nIdentificador único que referencia un conjunto específico de detalles asociados a un producto, como sus especificaciones técnicas, presentación, lote, ubicación, estado o características adicionales. Este campo es obligatorio para asegurar la trazabilidad y correcta asociación con los productos registrados.',
  product_status INT NOT NULL DEFAULT 2 COMMENT 'Estado actual del producto 1 = inactivo, 2 = activo, 3 = Vendido, 4 = En garantía',
  PRIMARY KEY (product_id),
  UNIQUE INDEX idPRODUCTS_UNIQUE (product_id ASC),
  INDEX fk_products_subcategory_idx (subcategory_id ASC),
  INDEX fk_products_product_details_idx (product_details_id ASC),
  CONSTRAINT fk_products_subcategory
    FOREIGN KEY (subcategory_id)
    REFERENCES SUBCATEGORIES (subcategory_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_products_product_details
    FOREIGN KEY (product_details_id)
    REFERENCES PRODUCT_DETAILS (product_details_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table PRODUCT_SERIALS
-- -----------------------------------------------------
CREATE TABLE PRODUCT_SERIALS (
  product_serial VARCHAR(255) NOT NULL UNIQUE COMMENT 'Identificador único de cada serial, sirve para diferenciar cada producto y sus detalles (INT, Not null, Unique)',
  product_id INT NOT NULL COMMENT 'Identificador de cada producto, El cúal sirve para relacionar los productos con su respectivo serial (INT, Not Null, Auto Increment)',
  input_order_id INT NOT NULL COMMENT 'Identificador de cada orden de entrada, Esta se relaciona en esta tabla para establecer fechas o facturas en las cuales se hizo el ingreso del producto (INT, Not null)',
  product_garanty_input DATE NOT NULL COMMENT 'Garantía del producto dada por el proveedor, este indica el tiempo de garantía actual, esta puede disminuir con el pasar del tiempo',
  PRIMARY KEY (product_serial),
  INDEX fk_product_serial_input_order_idx (input_order_id ASC),
  INDEX fk_product_serial_product_idx (product_id ASC),
  CONSTRAINT fk_product_serial_input_order
    FOREIGN KEY (input_order_id)
    REFERENCES INPUT_ORDERS (input_order_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_product_serial_products
    FOREIGN KEY (product_id)
    REFERENCES PRODUCTS (product_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table OUTPUT_DETAILS
-- -----------------------------------------------------
CREATE TABLE OUTPUT_DETAILS (
  out_order_id INT NOT NULL COMMENT 'Identificador de orden de salida, Clave única que identifica cada orden de salida registrada en el sistema. Esta orden agrupa una o varias salidas de productos desde el almacén, ya sea por venta, traslado, devolución o cualquier otro movimiento logístico.\n',
  product_serial VARCHAR(255) NOT NULL COMMENT '\nIdentificador de serie del producto.\n Número de serie único asignado a cada unidad individual de producto. Este identificador permite rastrear un producto específico durante todo su ciclo de vida, desde la fabricación o adquisición hasta su salida o desecho. Es obligatorio y no puede repetirse entre productos.',
  output_details_id INT NOT NULL AUTO_INCREMENT COMMENT ' Identificador de detalle de salida\n,  Clave primaria única que identifica cada registro individual en la tabla de detalles de salida. Este identificador se genera automáticamente por el sistema en orden secuencial y no puede ser nulo. Se utiliza para distinguir y rastrear cada línea o componente dentro de una orden de salida.',
  out_product_garanty DATE NOT NULL COMMENT 'Garantía del producto en salida\n\nIndica si el producto entregado o despachado cuenta con garantía activa o especifica el período de garantía ofrecido. Este campo es obligatorio, ya que permite hacer seguimiento a las condiciones de postventa o soporte del producto.',
  product_transformation VARCHAR(255) NOT NULL COMMENT 'Transformación del producto\n.\nIndica si el producto ha sido sometido a algún tipo de transformación antes de su salida del inventario. Esto puede incluir procesos como ensamblaje, personalización, reempaque, reparación, entre otros. El campo es obligatorio, ya que influye en el seguimiento de procesos logísticos y de control de calidad.',
  UNIQUE INDEX idOUTPUT_DETAILS_UNIQUE (product_serial ASC),
  INDEX fk_output_details_output_oder_idx (out_order_id ASC),
  PRIMARY KEY (output_details_id),
  CONSTRAINT fk_output_details_output_oder
    FOREIGN KEY (out_order_id)
    REFERENCES OUTPUT_ORDERS (out_order_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_output_details_product_serials
    FOREIGN KEY (product_serial)
    REFERENCES PRODUCT_SERIALS (product_serial)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table WARRANTY_INCIDENTS
-- -----------------------------------------------------
CREATE TABLE WARRANTY_INCIDENTS (
  warranty_incidents_id INT NOT NULL AUTO_INCREMENT COMMENT'Identificador único y autoincremental para los incidentes de garantía registrados en el sistema.',
  product_serial VARCHAR(255) NOT NULL COMMENT' Identificador autoincremental para cada número de serie registrado.',
  warranty_customer VARCHAR(100) NOT NULL COMMENT' Almacena la información de los clientes con garantías, incluyendo los detalles del producto y la fecha de expiración.',
  warranty_phone VARCHAR(255) NOT NULL COMMENT'Número de contacto principal para la gestión de la garantía.',
  warranty_address VARCHAR(255) NOT NULL COMMENT' Dirección del cliente para la gestión de la garantía.',
  warranty_description VARCHAR(100) NOT NULL COMMENT'Descripción detallada del problema o incidente reportado por el cliente.',
  warranty_link_attachments VARCHAR(255) NOT NULL COMMENT'Campo que contiene la URL o el path a los archivos adjuntos (imágenes, documentos) de la garantía, como facturas o fotos del producto.',
  warranty_city VARCHAR(100) NOT NULL COMMENT'Nombre de la ciudad del cliente. Utilizado para determinar la ubicación geográfica y asignar el caso a un centro de servicio local.' ,
  warranty_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora en que se reportó el incidente de garantía al sistema.' ,
  warranty_status INT NOT NULL DEFAULT 2 COMMENT 'Estado actual de la garantía , 1 = Sin Completar, 2 = En Proceso, 3 = Sin Completar, Al momento de ingresar la garantia nueva se le da un estado de 0 o Sin completar',
  PRIMARY KEY (warranty_incidents_id),
  UNIQUE INDEX warranty_incidents_id_UNIQUE (warranty_incidents_id ASC),
  INDEX fk_warranty_incidents_output_details_idx (product_serial ASC),
  CONSTRAINT fk_warranty_incidents_output_details
    FOREIGN KEY (product_serial)
    REFERENCES OUTPUT_DETAILS (product_serial)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table TECHNICAL
-- -----------------------------------------------------
CREATE TABLE TECHNICAL (
  user_id INT NOT NULL COMMENT 'Identificador único y primario del usuario. Esta columna se enlaza con la tabla de usuarios.',
  warranty_incidents_id INT NOT NULL  COMMENT 'Identificador único para cada incidente de garantía.',
  INDEX fk_technical_warranty_incidents_idx (warranty_incidents_id ASC),
  INDEX fk_technical_users_idx (user_id ASC),
  CONSTRAINT fk_technical_warranty_incidents
    FOREIGN KEY (warranty_incidents_id)
    REFERENCES WARRANTY_INCIDENTS (warranty_incidents_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_technical_users
    FOREIGN KEY (user_id)
    REFERENCES USERS (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table WAREHAUSEMAN
-- -----------------------------------------------------
CREATE TABLE WAREHAUSEMAN (
  users_id INT NOT NULL COMMENT'identificador unico para el usuario',
  input_order_id INT NOT NULL COMMENT'se utiliza para registrar la identificación de una orden (pedido) de compra de un cliente',
  INDEX fk_users_input_order_idx (users_id ASC),
  INDEX fk_warehouseman_input_order_idx (input_order_id ASC),
  CONSTRAINT fk_warehouseman_users
    FOREIGN KEY (users_id)
    REFERENCES USERS (user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_warehouseman_input_order
    FOREIGN KEY (input_order_id)
    REFERENCES INPUT_ORDERS (input_order_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;