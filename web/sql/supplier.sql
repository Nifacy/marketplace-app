CREATE OR REPLACE FUNCTION get_supplier(supplier_id INT)
RETURNS TABLE (
    id INT,
    name VARCHAR(50),
    contacts INT,
    address INT
) AS $$
BEGIN
    RETURN QUERY SELECT suppliers.* FROM suppliers WHERE suppliers.id = supplier_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_supplier(
    p_name VARCHAR(50),
    p_contacts INT,
    p_address INT
) RETURNS INT AS $$ -- Не уверен нужно будет ретурнить id. Оставлю здесь комментарий.
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

CREATE OR REPLACE FUNCTION login_supplier(username TEXT, password TEXT)
RETURNS INT AS $$
DECLARE
    supplier_id INT;
BEGIN
    SELECT account_id 
    FROM supplier_credentials 
    WHERE login = login_supplier.username AND password = crypt(login_supplier.password, password) 
    INTO supplier_id;
    RETURN supplier_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION register_supplier(username TEXT, password TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    supplier_id INT;
BEGIN
    -- Проверяем, существует ли уже учетная запись с таким именем пользователя
    SELECT account_id FROM supplier_credentials WHERE login = register_supplier.username INTO supplier_id;
    IF supplier_id IS NOT NULL THEN
        RETURN FALSE;
    END IF;
    
    -- Если нет, создаем новую учетную запись
    supplier_id := nextval('suppliers_id_seq');
    INSERT INTO supplier_credentials (login, password, account_id) 
    VALUES (register_supplier.username, crypt(register_supplier.password, gen_salt('bf', 8)), supplier_id);
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_supplier(supplier_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM suppliers WHERE id = supplier_id;
END;
$$ LANGUAGE plpgsql;