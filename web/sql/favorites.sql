-- Function to add products to "favorites"
-- Input parameters:
--   p_customer_id - Customer ID
--   p_product_id - Product ID
-- Return values:
--   0 - Success
--   1 - The customer with the specified id does not exist
--   2 - The product with the specified id does not exist

CREATE OR REPLACE FUNCTION add_to_favorite(p_customer_id INT, p_product_id INT)
RETURNS INT AS $$
DECLARE
  v_exists INT;
BEGIN
  SELECT COUNT(*) INTO v_exists FROM customers WHERE id = p_customer_id;
  IF v_exists = 0 THEN
    RETURN 1;
  END IF;

  SELECT COUNT(*) INTO v_exists FROM products WHERE id = p_product_id;
  IF v_exists = 0 THEN
    RETURN 2;
  END IF;

  SELECT COUNT(*) INTO v_exists FROM favorite_products WHERE customer_id = p_customer_id AND product_id = p_product_id;
  IF v_exists = 0 THEN
    INSERT INTO favorite_products (customer_id, product_id) VALUES (p_customer_id, p_product_id);
  END IF;

  RETURN 0;
END;
$$ LANGUAGE plpgsql;


-- Function to get favorite products for a customer
-- Input parameters:
--   p_customer_id - Customer ID
-- Return values:
-- SETOF product_object - A set of product objects representing the favorite products of the customer

CREATE OR REPLACE FUNCTION get_favorites(p_customer_id INT)
RETURNS SETOF product_object AS $$
DECLARE
    product_id INT;
BEGIN
  FOR product_id IN
    SELECT 
      p.product_id
    FROM favorite_products p
    WHERE (p.customer_id = p_customer_id)
  LOOP
    RETURN QUERY SELECT * FROM build_product_object(product_id);
  END LOOP;
END; $$
LANGUAGE plpgsql;
