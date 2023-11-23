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
    p_id INT,
    p_name VARCHAR(50),
    p_contacts INT,
    p_address INT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO suppliers(id, name, contacts, address)
    VALUES (p_id, p_name, p_contacts, p_address);
END; $$
LANGUAGE plpgsql;
