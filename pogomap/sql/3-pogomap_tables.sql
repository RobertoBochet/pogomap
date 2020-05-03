CREATE TABLE "editorkeys"
(
    "key"     varchar(32) NOT NULL PRIMARY KEY,
    "comment" text
);

CREATE TABLE "portals"
(
    "id"        integer          NOT NULL DEFAULT '0' PRIMARY KEY,
    "latitude"  double precision NOT NULL,
    "longitude" double precision NOT NULL,
    "name"      text             NOT NULL,
    "image"     text             NOT NULL
);

CREATE TABLE "entities"
(
    "id"          integer       NOT NULL PRIMARY KEY,
    "type"        entities_type NOT NULL DEFAULT 'portal',
    "is_eligible" boolean       NOT NULL DEFAULT FALSE,
    FOREIGN KEY ("id") REFERENCES "portals" ("id") ON DELETE CASCADE
);

CREATE TABLE "s2cells"
(
    "id"    integer NOT NULL PRIMARY KEY,
    "level" integer NOT NULL,
    "cell"  polygon NOT NULL
);