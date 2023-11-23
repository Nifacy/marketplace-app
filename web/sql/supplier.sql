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
