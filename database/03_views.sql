-- Vista para obtener todos los usuarios
CREATE VIEW get_all_users AS
SELECT
    r.rol_name,
    u.user_id,
    u.user_name,
    u.user_first_surname,
    u.user_second_surname,
    u.user_phone,
    u.user_email,
    u.user_address,
    u.user_city,
    u.user_date
FROM USERS AS u
INNER JOIN ROLES AS r
ON u.rol_id = r.rol_id;

-- Vista para obtener todos los productos con sus categorias y subcategorias
CREATE VIEW get_all_products AS
SELECT
    io.input_order_id,
    pd.product_detail_date,
    io.input_order_bill,
    c.category_name,
    sc.subcategory_id,
    sc.subcategory_name,
    p.product_id,
    s.supplier_name,
    ps.product_serial,
    pm.product_model_name,
    pm.product_model_id,
    pm.product_model_description,
    pb.product_brand_id,
    pb.product_brand_name,
    ps.product_garanty_input,
    p.product_status
    FROM SUPPLIERS AS s
    INNER JOIN INPUT_ORDERS AS io
        ON s.supplier_id = io.supplier_id
    INNER JOIN PRODUCT_SERIALS AS ps
        ON io.input_order_id = ps.input_order_id
    INNER JOIN PRODUCTS as p
        ON ps.product_id = p.product_id
    INNER JOIN SUBCATEGORIES AS sc
        ON p.subcategory_id = sc.subcategory_id
    INNER JOIN CATEGORIES AS c
        ON sc.category_id = c.category_id
    INNER JOIN PRODUCT_DETAILS AS pd
        ON p.product_details_id = pd.product_details_id
    INNER JOIN PRODUCT_MODELS AS pm
        ON pd.product_model_id = pm.product_model_id
    INNER JOIN PRODUCT_BRANDS AS pb
        ON pm.product_brand_id = pb.product_brand_id;

-- Vista para obtener todas subcategorias con su categoria
CREATE VIEW get_all_subcategories AS
	SELECT
	c.category_name,
	sc.subcategory_name,
	sc.subcategory_id
	FROM CATEGORIES AS c
	INNER JOIN SUBCATEGORIES AS sc
	ON c.category_id=sc.category_id;

-- Estado de garantías (Sin completar, en proceso, completada)
CREATE VIEW get_warranties_status AS
    SELECT 
    warranty_status, 
    COUNT(*) AS total
    FROM WARRANTY_INCIDENTS
    GROUP BY warranty_status;

-- Salidas o "ventas" por mes
CREATE VIEW get_monthly_outputs AS
    SELECT
    YEAR(out_order_date) AS years,
    MONTH(out_order_date) AS months, 
    COUNT(*) AS total
    FROM OUTPUT_ORDERS
    GROUP BY YEAR(out_order_date), MONTH(out_order_date)
    ORDER BY years;

-- Entradas por proveedor
CREATE VIEW get_supplier_inputs AS
    SELECT s.supplier_name, 
    COUNT(*) AS orders
    FROM INPUT_ORDERS io
    JOIN SUPPLIERS s ON io.supplier_id = s.supplier_id
    GROUP BY s.supplier_id
    ORDER BY orders DESC;

-- Garantias por mes
CREATE VIEW get_monthly_warranties AS
    SELECT
    YEAR(warranty_date) AS years,
    MONTH(warranty_date) AS months, 
    COUNT(*) AS warranties
    FROM WARRANTY_INCIDENTS
    GROUP BY years, months;


-- Salidas de productos
CREATE VIEW get_output_products AS
    SELECT
    oo.out_order_id,
    oo.out_order_date,
    oo.out_order_status,
    od.output_details_id,
    od.product_serial,
    od.out_product_garanty,
    od.product_transformation,
    pm.product_model_description,
    pm.product_model_name,
    pb.product_brand_name
    FROM OUTPUT_DETAILS AS od 
    INNER JOIN OUTPUT_ORDERS AS oo
    ON oo.out_order_id = od.out_order_id
    INNER JOIN PRODUCT_SERIALS AS ps
    ON od.product_serial = ps.product_serial
    INNER JOIN PRODUCTS AS p
    ON ps.product_id = p.product_id
    INNER JOIN PRODUCT_DETAILS AS pd
    ON p.product_details_id = pd.product_details_id
    INNER JOIN PRODUCT_MODELS AS pm
    ON pd.product_model_id = pm.product_model_id 
    INNER JOIN PRODUCT_BRANDS AS pb
    ON pm.product_brand_id = pb.product_brand_id;
    
CREATE VIEW get_all_products_with_stock AS
SELECT 
    v.*,
    IFNULL(stock.stock, 0) AS stock
FROM get_all_products v
LEFT JOIN (
    SELECT 
        p.product_id,
        COUNT(ps.product_serial) AS stock
    FROM PRODUCTS p
    LEFT JOIN PRODUCT_SERIALS ps 
        ON ps.product_id = p.product_id
    GROUP BY p.product_id
) AS stock
ON v.product_id = stock.product_id;

-- Vista para obtener todos los productos con sus categorias y subcategorias
CREATE VIEW get_all_products_null AS
SELECT
    io.input_order_id,
    io.input_order_date,
    io.input_order_bill,
    c.category_name,
    sc.subcategory_name,
    p.product_id,
    s.supplier_name,
    ps.product_serial,
    pm.product_model_name,
    pm.product_model_id,
    pm.product_model_description,
    pb.product_brand_name,
    ps.product_garanty_input
    FROM SUPPLIERS AS s
    LEFT JOIN INPUT_ORDERS AS io
    ON s.supplier_id = io.supplier_id
    LEFT JOIN PRODUCT_SERIALS AS ps
    ON io.input_order_id = ps.input_order_id
    LEFT JOIN PRODUCTS as p
    ON ps.product_id = p.product_id
    LEFT JOIN SUBCATEGORIES AS sc
    ON p.subcategory_id = sc.subcategory_id
    LEFT JOIN CATEGORIES AS c
    ON sc.category_id = c.category_id
    LEFT JOIN PRODUCT_DETAILS AS pd
    ON p.product_details_id = pd.product_details_id
    INNER JOIN PRODUCT_MODELS AS pm
    ON pd.product_model_id = pm.product_model_id
    LEFT JOIN PRODUCT_BRANDS AS pb
    ON pm.product_brand_id = pb.product_brand_id
    ORDER BY p.product_id;