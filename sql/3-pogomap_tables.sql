USE `pogomap`;

CREATE TABLE `editorkeys` (
  `key` varchar(32) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL,
  `comment` text CHARACTER SET utf8 COLLATE utf8_swedish_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

CREATE TABLE `entities` (
  `id` int(11) NOT NULL,
  `type` enum('none','pokestop','gym','') COLLATE utf8_swedish_ci NOT NULL DEFAULT 'none',
  `isEligible` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

CREATE TABLE `portals` (
  `id` int(11) NOT NULL DEFAULT '0',
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `name` text COLLATE utf8_swedish_ci NOT NULL,
  `image` text COLLATE utf8_swedish_ci NOT NULL,
  `guid` text COLLATE utf8_swedish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

CREATE TABLE `s2cells` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `level` tinyint(3) UNSIGNED NOT NULL,
  `cell` polygon NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;


ALTER TABLE `editorkeys` ADD PRIMARY KEY (`key`);

ALTER TABLE `entities` ADD PRIMARY KEY (`id`);

ALTER TABLE `portals` ADD PRIMARY KEY (`id`);

ALTER TABLE `s2cells` ADD PRIMARY KEY (`id`);

COMMIT;