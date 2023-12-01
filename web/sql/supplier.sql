CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION get_supplier(p_supplier_id INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(50),
    contacts INT,
    address INT
) AS $$
BEGIN
    RETURN QUERY 
    SELECT 
        s.* 
    FROM 
        suppliers AS s
    WHERE 
        s.id = p_supplier_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_supplier(
    p_name VARCHAR(50),
    p_contacts INT,
    p_address INT
) RETURNS INT AS $$ 
DECLARE
    v_supplier_id INT;
BEGIN
    INSERT INTO suppliers(
        name, 
        contacts, 
        address
    )
    VALUES (
        p_name, 
        p_contacts, 
        p_address
    )
    RETURNING id INTO v_supplier_id;

    RETURN v_supplier_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION login_supplier(p_username TEXT, p_password TEXT)
RETURNS INT AS $$
DECLARE
    v_supplier_id INT;
BEGIN
    SELECT 
        sc.account_id 
    FROM 
        supplier_credentials AS sc
    WHERE 
        sc.login = p_username AND 
        sc.password = crypt(p_password, sc.password) 
    INTO v_supplier_id;
    
    RETURN v_supplier_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION register_supplier(p_username TEXT, p_password TEXT, p_supplier_id INT)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO supplier_credentials(
        login, 
        password, 
        account_id
    ) 
    VALUES(
        p_username, 
        crypt(p_password, gen_salt('bf', 8)), 
        p_supplier_id
    );
    
    RETURN 'Supplier registration successful';
END;
$$ LANGUAGE plpgsql;

-- TODO: Check `REFERENCE suppliers` tables and fix for proper deletion
CREATE OR REPLACE FUNCTION delete_supplier(p_supplier_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM suppliers WHERE id = p_supplier_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_supplier_upon_registration(p_supplier_id INT)
RETURNS VOID AS $$
DECLARE
    p_contacts_id INT;
    p_address_id INT;
BEGIN
    SELECT contacts, address INTO p_contacts_id, p_address_id FROM suppliers WHERE id = p_supplier_id;

    DELETE FROM suppliers WHERE id = p_supplier_id;

    IF NOT EXISTS (SELECT 1 FROM suppliers WHERE contacts = p_contacts_id) THEN
        DELETE FROM contacts WHERE id = p_contacts_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM suppliers WHERE address = p_address_id) THEN
        DELETE FROM addresses WHERE id = p_address_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
