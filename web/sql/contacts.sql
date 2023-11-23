CREATE OR REPLACE FUNCTION get_contacts(contacts_id INT)
RETURNS TABLE (
    id INT,
    phone public.phone,
    email public.email,
    telegram VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY SELECT contacts.* FROM contacts WHERE contacts.id = contacts_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_contacts(
    p_phone public.phone,
    p_email public.email,
    p_telegram VARCHAR(50)
) RETURNS INT AS $$
DECLARE
    v_new_id INT;
BEGIN
    INSERT INTO contacts(
        phone, 
        email, 
        telegram
    )
    VALUES (
        p_phone, 
        p_email, 
        p_telegram
    )
    RETURNING id INTO v_new_id;

    RETURN v_new_id;
END; $$
LANGUAGE plpgsql;
