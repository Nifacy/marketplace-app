CREATE OR REPLACE FUNCTION create_order(
  p_product_id INT, 
  p_target_address_id INT, 
  p_customer_id INT
)
RETURNS INT AS $$
DECLARE
    v_order_id INT;
    v_price NUMERIC;
BEGIN
    -- Check if the product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE id = p_product_id) THEN
        RAISE EXCEPTION 'Product does not exist';
    END IF;

    -- Get the price of the product
    SELECT price INTO v_price FROM products WHERE id = p_product_id;

    -- Create the order with the obtained price
    INSERT 
    INTO orders(
      status, 
      product_id, 
      price,
      target_address, 
      customer_id, 
      creation_datetime
    )
    VALUES (
      'CREATED', 
      p_product_id, 
      v_price,
      p_target_address_id, 
      p_customer_id, 
      NOW()
    )
    RETURNING id INTO v_order_id;

    RETURN v_order_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_order(
  p_order_id INT
)
RETURNS TABLE (
  id INT,
  status public.order_status,
  cancel_description TEXT,
  price NUMERIC,
  product_id INT,
  creation_datetime TIMESTAMP,
  target_address INT,
  customer_id INT
) AS $$
BEGIN
  RETURN QUERY 
  SELECT 
    * 
  FROM 
    orders 
  WHERE 
    orders.id = p_order_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_orders(
  p_order_id INT DEFAULT NULL,
  p_supplier_id INT DEFAULT NULL,
  p_customer_id INT DEFAULT NULL
)
RETURNS TABLE (
  id INT,
  status public.order_status,
  cancel_description TEXT,
  price NUMERIC,
  product_id INT,
  creation_datetime TIMESTAMP,
  target_address INT,
  customer_id INT
) AS $$
BEGIN
  RETURN QUERY 
  SELECT 
    orders.* 
  FROM 
    orders 
  JOIN products ON orders.product_id = products.id
  WHERE 
    (p_order_id IS NULL OR orders.id = p_order_id) AND
    (p_supplier_id IS NULL OR products.suppliers_id = p_supplier_id) AND
    (p_customer_id IS NULL OR orders.customer_id = p_customer_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_order_status(
  p_order_id INT, 
  p_status order_status
)
RETURNS VOID AS $$
BEGIN
    UPDATE 
      orders 
    SET 
      status = p_status 
    WHERE id = p_order_id;
END;
$$ LANGUAGE plpgsql;
