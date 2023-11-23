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
