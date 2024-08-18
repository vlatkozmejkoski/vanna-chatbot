DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO customers (first_name, last_name, email, phone) VALUES
        (
            'FirstName' || i,
            'LastName' || i,
            'email' || i || '@example.com',
            '555-' || LPAD(i::text, 4, '0')
        );
    END LOOP;
END $$;