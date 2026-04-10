CREATE OR REPLACE FUNCTION get_user(p_id INT)
RETURNS TABLE(
    name VARCHAR(50),
    phone VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT pb.name, pb.phone 
    FROM phone_book pb
    WHERE pb.id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION show_users(s VARCHAR)
RETURNS TABLE(
    id INT,
    name VARCHAR(50),
    phone VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT pb.id, pb.name, pb.phone
    FROM phone_book pb 
    WHERE pb.name LIKE s||'%' OR pb.phone LIKe s||'%';
END;
$$ LANGUAGE plpgsql;

CREATE or REPLACE FUNCTION list_user(a INT, b INT)
RETURNS TABLE(
    id INT,
    name VARCHAR(50),
    phone VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY SELECT pb.id, pb.name, pb.phone
    FROM phone_book pb 
    LIMIT a OFFSET b;
END;
$$ LANGUAGE plpgsql;



























