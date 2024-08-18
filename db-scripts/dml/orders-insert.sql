DO $$
DECLARE
    i INT;
    t_customer_id INT;
    status_options TEXT[] := ARRAY['completed', 'pending', 'shipped', 'canceled'];
BEGIN
    FOR i IN 1..5000 LOOP
        t_customer_id := (SELECT customer_id FROM customers ORDER BY RANDOM() LIMIT 1);
        INSERT INTO orders (customer_id, order_date, amount, status) VALUES
        (
            t_customer_id,
            NOW() - INTERVAL '1 day' * (RANDOM() * 365)::INT,
            ROUND(RANDOM()::numeric * 500 + 1, 2),
            status_options[FLOOR(RANDOM() * 4 + 1)::INT]
        );
    END LOOP;
END $$;