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

CREATE OR REPLACE FUNCTION login_customer(p_username TEXT, p_password TEXT)
RETURNS INT AS $$
DECLARE
    v_customer_id INT;
BEGIN
    SELECT 
        sc.account_id 
    FROM 
        customer_credentials AS sc
    WHERE 
        sc.login = p_username AND 
        sc.password = crypt(p_password, sc.password) 
    INTO v_customer_id;
    
    RETURN v_customer_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION register_customer(p_username TEXT, p_password TEXT, p_customer_id INT)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO customer_credentials(
        login, 
        password, 
        account_id
    ) 
    VALUES(
        p_username, 
        crypt(p_password, gen_salt('bf', 8)), 
        p_customer_id
    );
    
    RETURN 'Customer registration successful';
END;
$$ LANGUAGE plpgsql;

-- TODO: Check `REFERENCE customers` tables and fix for proper deletion
CREATE OR REPLACE FUNCTION delete_customer(p_customer_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM customers WHERE id = p_customer_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_customer_upon_registration(p_customer_id INT)
RETURNS VOID AS $$
DECLARE
    p_contacts_id INT;
    p_address_id INT;
BEGIN
    SELECT contacts, address INTO p_contacts_id, p_address_id FROM customers WHERE id = p_customer_id;

    DELETE FROM customers WHERE id = p_customer_id;

    IF NOT EXISTS (SELECT 1 FROM customers WHERE contacts = p_contacts_id) THEN
        DELETE FROM contacts WHERE id = p_contacts_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM customers WHERE address = p_address_id) THEN
        DELETE FROM addresses WHERE id = p_address_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
