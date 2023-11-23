CREATE OR REPLACE FUNCTION get_contact(contact_id INT)
RETURNS TABLE (
    id INT,
    phone public.phone,
    email public.email,
    telegram VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY SELECT contacts.* FROM contacts WHERE contacts.id = contact_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_contact(
    p_id INT,
    p_phone public.phone,
    p_email public.email,
    p_telegram VARCHAR(50)
) RETURNS VOID AS $$
BEGIN
    INSERT INTO contacts(id, phone, email, telegram)
    VALUES (p_id, p_phone, p_email, p_telegram);
END; $$
LANGUAGE plpgsql;
