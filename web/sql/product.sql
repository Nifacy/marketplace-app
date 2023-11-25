CREATE OR REPLACE FUNCTION get_product(p_product_id INT)
RETURNS TABLE (
    id INT,
    images TEXT[],
    price NUMERIC(10, 2),
    product_name VARCHAR(50),
    description TEXT,
    supplier_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        ARRAY(SELECT url FROM product_images WHERE product = p.id),
        p.price,
        p.product_name,
        p.description,
        p.suppliers_id
    FROM 
        products p
    WHERE 
        p.id = p_product_id;
END; $$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_product(
    p_images VARCHAR[],
    p_name VARCHAR(50),
    p_price NUMERIC(10, 2),
    p_description TEXT,
    p_supplier_id INT
)
RETURNS INT AS $$
DECLARE
    v_product_id INT;
BEGIN
    -- create new product record
    INSERT INTO products(
        price,
        product_name,
        description,
        suppliers_id,
        is_for_sale
    )
    VALUES (
        p_price,
        p_name,
        p_description,
        p_supplier_id,
        true
    )
    RETURNING id INTO v_product_id;

    -- insert product images
    FOR i IN 1..array_length(p_images, 1)
    LOOP
        INSERT INTO product_images(
            product,
            url
        )
        VALUES (
            v_product_id,
            p_images[i]
        );
    END LOOP;

    RETURN v_product_id;
END; $$
LANGUAGE plpgsql;
