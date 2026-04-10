CREATE OR REPLACE PROCEDURE add_user(
    p_name VARCHAR(50),
    p_phone VARCHAR(20)
) AS $$
BEGIN
    INSERT INTO phone_book (name, phone)
    VALUES (p_name, p_phone);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE update_phone(
    p_id INT,
    p_phone VARCHAR
) AS $$
BEGIN
    UPDATE phone_book
    SET phone=p_phone
    WHERE id=p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user(
    p_id INT
) AS $$
BEGIN
    DELETE FROM phone_book
    WHERE id=p_id;
END;
$$ LANGUAGE plpgsql;