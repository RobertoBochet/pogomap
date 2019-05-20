CREATE TABLE "editorkeys" (
  "key" varchar(32) NOT NULL PRIMARY KEY,
  "comment" text
);

CREATE TABLE "entities" (
  "id" integer NOT NULL PRIMARY KEY,
  "type" entities_type NOT NULL DEFAULT 'portal',
  "is_eligible" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE "portals" (
  "id" integer NOT NULL DEFAULT '0' PRIMARY KEY,
  "latitude" double precision NOT NULL,
  "longitude" double precision NOT NULL,
  "name" text NOT NULL,
  "image" text NOT NULL,
  "guid" text NOT NULL
);

CREATE TABLE "s2cells" (
  "id" integer NOT NULL PRIMARY KEY,
  "level" integer NOT NULL,
  "cell" polygon NOT NULL
);