CREATE OR REPLACE FUNCTION get_address(address_id INT)
RETURNS TABLE (
    id INT,
    street VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50),
    postal_code VARCHAR(50),
    house INT,
    entrance INT,
    appartment INT
) AS $$
BEGIN
    RETURN QUERY SELECT addresses.* FROM addresses WHERE addresses.id = address_id;
END; $$
LANGUAGE plpgsql;
