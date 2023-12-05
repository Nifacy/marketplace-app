DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'product_object') THEN
        CREATE TYPE product_object AS (
            id INT,
            images TEXT[],
            price NUMERIC(10, 2),
            product_name VARCHAR(50),
            description TEXT,
            supplier_id INT,
            is_for_sale BOOLEAN
        );
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION build_product_object(p_id INTEGER)
RETURNS product_object AS $$
DECLARE
    obj product_object;
BEGIN
  SELECT 
    p.id,
    ARRAY(SELECT url FROM product_images WHERE product = p.id),
    p.price,
    p.product_name,
    p.description,
    p.suppliers_id,
    p.is_for_sale
  INTO obj
  FROM products p
  WHERE p.id = p_id;

  RETURN obj;
END; $$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_products(
    p_product_id   INTEGER DEFAULT NULL,
    p_name         TEXT DEFAULT NULL,
    p_owner_id     INTEGER DEFAULT NULL,
    p_is_for_sale  BOOLEAN DEFAULT NULL
)
RETURNS SETOF product_object AS $$
DECLARE
    product_id INT;
BEGIN
  FOR product_id IN
    SELECT 
      p.id
    FROM products p
    WHERE (p_product_id IS NULL OR p.id = p_product_id)
      AND (p_name IS NULL OR p.product_name LIKE '%' || p_name || '%')
      AND (p_owner_id IS NULL OR p.suppliers_id = p_owner_id)
      AND (p_is_for_sale IS NULL OR p.is_for_sale = p_is_for_sale)
    ORDER BY p.id
  LOOP
    RETURN QUERY SELECT * FROM build_product_object(product_id);
  END LOOP;
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


CREATE OR REPLACE FUNCTION update_product(
    p_id INT,
    p_price NUMERIC(10, 2),
    p_product_name VARCHAR(50),
    p_description TEXT,
    p_images TEXT[]
) RETURNS TEXT AS $$
DECLARE
    v_product_exists BOOLEAN;
BEGIN
    -- check, if product exists
    SELECT EXISTS(SELECT 1 FROM products WHERE id = p_id) INTO v_product_exists;
    IF NOT v_product_exists THEN
        RETURN 'error: product not exists';
    END IF;

    -- update product's info
    UPDATE products
    SET price = p_price,
        product_name = p_product_name,
        description = p_description
    WHERE id = p_id;

    -- delete old images
    DELETE FROM product_images WHERE product = p_id;

    -- add new images
    FOR i IN 1 .. array_length(p_images, 1)
    LOOP
        INSERT INTO product_images (product, url)
        VALUES (p_id, p_images[i]);
    END LOOP;

    RETURN 'ok';
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION remove_product_from_sale(p_product_id INT)
RETURNS VOID AS $$
BEGIN
    UPDATE products
    SET is_for_sale = false
    WHERE id = p_product_id;
END;
$$
LANGUAGE plpgsql;
