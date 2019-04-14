CREATE VIEW "gyms" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid",
    "entities"."is_eligible" AS "is_eligible"
FROM
    "entities"
    JOIN "portals" ON "entities"."id" = "portals"."id"
WHERE
    "entities"."type" = 'gym';

CREATE VIEW "gyms_eligible" AS
SELECT
    "gyms"."id" AS "id",
    "gyms"."latitude" AS "latitude",
    "gyms"."longitude" AS "longitude",
    "gyms"."name" AS "name",
    "gyms"."image" AS "image",
    "gyms"."guid" AS "guid"
FROM
    "gyms"
WHERE
    "gyms"."is_eligible" = TRUE;

CREATE VIEW "in_pogo" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid",
    "entities"."type" AS "type",
    "entities"."is_eligible" AS "is_eligible"
FROM
    "entities"
    JOIN "portals" ON "entities"."id" = "portals"."id"
WHERE
    "entities"."type" <> 'none';

CREATE VIEW "not_in_pogo" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid",
    "entities"."is_eligible" AS "is_eligible"
FROM
    "entities"
    JOIN "portals" ON "entities"."id" = "portals"."id"
WHERE
    "entities"."type" = 'none';

CREATE VIEW "pokestops" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid",
    "entities"."is_eligible" AS "is_eligible"
FROM
    "entities"
    JOIN "portals" ON "entities"."id" = "portals"."id"
WHERE
    "entities"."type" = 'pokestop';

CREATE VIEW "pokestops_eligible" AS
SELECT
    "pokestops"."id" AS "id",
    "pokestops"."latitude" AS "latitude",
    "pokestops"."longitude" AS "longitude",
    "pokestops"."name" AS "name",
    "pokestops"."image" AS "image",
    "pokestops"."guid" AS "guid"
FROM
    "pokestops"
WHERE
    "pokestops"."is_eligible" = TRUE;

CREATE VIEW "unverified" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid"
FROM
    "portals"
    LEFT JOIN "entities" ON "entities"."id" = "portals"."id"
WHERE
    "entities"."id" IS NULL;

CREATE VIEW "verified" AS
SELECT
    "portals"."id" AS "id",
    "portals"."latitude" AS "latitude",
    "portals"."longitude" AS "longitude",
    "portals"."name" AS "name",
    "portals"."image" AS "image",
    "portals"."guid" AS "guid",
    "entities"."type" AS "type",
    "entities"."is_eligible" AS "is_eligible"
FROM
    "entities"
    JOIN "portals" ON "entities"."id" = "portals"."id";

CREATE VIEW "positions" AS
SELECT
    "portals"."id" AS "id",
    ST_SetSRID(ST_MakePoint("portals"."longitude", "portals"."latitude"),4326) AS "position"
FROM
    "portals";

