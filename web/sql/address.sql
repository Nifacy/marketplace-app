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

CREATE OR REPLACE FUNCTION create_address(
    p_street VARCHAR(50),
    p_city VARCHAR(50),
    p_country VARCHAR(50),
    p_postal_code VARCHAR(50),
    p_house INT,
    p_entrance INT,
    p_appartment INT
) RETURNS INT AS $$
DECLARE
    v_new_id INT;
BEGIN
    INSERT INTO addresses(
        street, 
        city, 
        country, 
        postal_code, 
        house, entrance, 
        appartment
    )
    VALUES (
        p_street, 
        p_city, 
        p_country, 
        p_postal_code, 
        p_house, 
        p_entrance, 
        p_appartment)
    RETURNING id INTO v_new_id;

    RETURN v_new_id;
END; $$
LANGUAGE plpgsql;
