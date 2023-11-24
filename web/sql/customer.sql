CREATE OR REPLACE FUNCTION get_customer(customer_id INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    contacts INT,
    address INT
) AS $$
BEGIN
    RETURN QUERY SELECT customers.* FROM customers WHERE customers.id = customer_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_customer(
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_contacts INT,
    p_address INT
) RETURNS INT AS $$
DECLARE
    v_customer_id INT;
BEGIN
    INSERT INTO customers(
        first_name, 
        last_name, 
        contacts, 
        address
    )
    VALUES (
        p_first_name, 
        p_last_name, 
        p_contacts, 
        p_address
    )
    RETURNING id INTO v_customer_id;

    RETURN v_customer_id;
END; $$
LANGUAGE plpgsql;
