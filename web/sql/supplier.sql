CREATE FUNCTION add_supplier(_name VARCHAR(50),
 _contacts INT, 
 _street VARCHAR(50), 
 _city VARCHAR(50), 
 _country VARCHAR(50), 
 _postal_code VARCHAR(50), 
 _house INT, _entrance INT, 
 _appartment INT)
RETURNS VOID AS $$
DECLARE 
    _address_id INT;
BEGIN
    INSERT INTO addresses (street, city, country, postal_code, house, entrance, appartment) 
    VALUES (_street, _city, _country, _postal_code, _house, _entrance, _appartment) 
    RETURNING id INTO _address_id;

    INSERT INTO suppliers (name, contacts, address) VALUES (_name, _contacts, _address_id);
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION get_supplier(_id INT)
RETURNS TABLE(id INT, name VARCHAR(50), contacts INT, address INT) AS $$
BEGIN
    RETURN QUERY SELECT * FROM suppliers WHERE id = _id;
END;
$$ LANGUAGE plpgsql;