CREATE FUNCTION portals_check () RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    counter integer := 0;
	rand integer;
BEGIN
    -- Rand id
    IF NEW."id" = 0 THEN
        LOOP
            rand := floor(random() * (999999 - 100000) + 100000);
        	EXIT WHEN (SELECT
                COUNT(*)
            FROM
                "portals"
            WHERE
                "id" = rand) = 0;
        END LOOP;
		NEW."id" := rand;
    END IF;

    -- Image protocol
    NEW."image" := replace(NEW."image", 'http://', '//');
    NEW."image" := replace(NEW."image", 'https://', '//');

	RETURN NEW;
END;
$$;

CREATE TRIGGER "portals_BEFORE_INSERT"
    BEFORE INSERT ON "portals"
    FOR EACH ROW
    EXECUTE PROCEDURE portals_check ();

