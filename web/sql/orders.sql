CREATE OR REPLACE FUNCTION create_order(
  p_product_id INT, 
  p_target_address_id INT, 
  p_customer_id INT
)
RETURNS TABLE(status_code INT, order_id INT) AS $$
DECLARE
    v_order_id INT;
    v_price NUMERIC;
BEGIN
    -- Check if the product exists
    IF NOT EXISTS (SELECT 1 FROM products WHERE id = p_product_id) THEN
        -- Return status code 1 for 'Product does not exist'
        RETURN QUERY SELECT 1, NULL::INT;
        RETURN;
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

    -- Return status code 0 for 'Success' and the order_id
    RETURN QUERY SELECT 0, v_order_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_order(
  p_order_id INT
)
RETURNS TABLE (
  status_code INT,
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
  IF NOT EXISTS (SELECT 1 FROM orders WHERE orders.id = p_order_id) THEN
    -- Return status code 1 for 'Order does not exist'
    RETURN QUERY SELECT 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL;
  ELSE
    RETURN QUERY 
    SELECT 
      0, -- Return status code 0 for 'Success'
      * 
    FROM 
      orders 
    WHERE 
      orders.id = p_order_id;
  END IF;
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
RETURNS INT AS $$
DECLARE
    v_count INT;
BEGIN
    -- Check if the order exists
    IF NOT EXISTS (SELECT 1 FROM orders WHERE id = p_order_id) THEN
        -- Return status code 1 for 'Order does not exist'
        RETURN 1;
    END IF;

    -- Update the order status
    UPDATE 
      orders 
    SET 
      status = p_status 
    WHERE id = p_order_id;

    -- Check if the update was successful
    GET DIAGNOSTICS v_count = ROW_COUNT;
    IF v_count = 0 THEN
        -- Return status code 2 for 'Update failed'
        RETURN 2;
    END IF;

    -- Return status code 0 for 'Success'
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

