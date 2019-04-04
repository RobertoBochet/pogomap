USE `pogomap`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `gyms`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid`,`entities`.`isEligible` AS `isEligible` from (`entities` join `portals` on((`entities`.`id` = `portals`.`id`))) where (`entities`.`type` = 'gym') ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `gyms_eligible`  AS  select `gyms`.`id` AS `id`,`gyms`.`latitude` AS `latitude`,`gyms`.`longitude` AS `longitude`,`gyms`.`name` AS `name`,`gyms`.`image` AS `image`,`gyms`.`guid` AS `guid` from `gyms` where (`gyms`.`isEligible` = 1) ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `inpogo`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid`,`entities`.`type` AS `type`,`entities`.`isEligible` AS `isEligible` from (`entities` join `portals` on((`entities`.`id` = `portals`.`id`))) where (`entities`.`type` <> 'none') ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `notinpogo`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid`,`entities`.`isEligible` AS `isEligible` from (`entities` join `portals` on((`entities`.`id` = `portals`.`id`))) where (`entities`.`type` = 'none') ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `pokestops`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid`,`entities`.`isEligible` AS `isEligible` from (`entities` join `portals` on((`entities`.`id` = `portals`.`id`))) where (`entities`.`type` = 'pokestop') ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `pokestops_eligible`  AS  select `pokestops`.`id` AS `id`,`pokestops`.`latitude` AS `latitude`,`pokestops`.`longitude` AS `longitude`,`pokestops`.`name` AS `name`,`pokestops`.`image` AS `image`,`pokestops`.`guid` AS `guid` from `pokestops` where (`pokestops`.`isEligible` = 1) ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `unverified`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid` from (`portals` left join `entities` on((`entities`.`id` = `portals`.`id`))) where isnull(`entities`.`id`) ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `verified`  AS  select `portals`.`id` AS `id`,`portals`.`latitude` AS `latitude`,`portals`.`longitude` AS `longitude`,`portals`.`name` AS `name`,`portals`.`image` AS `image`,`portals`.`guid` AS `guid`,`entities`.`type` AS `type`,`entities`.`isEligible` AS `isEligible` from (`entities` join `portals` on((`entities`.`id` = `portals`.`id`))) ;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `positions`  AS  select `portals`.`id` AS `id`,st_pointfromtext(concat('POINT(',`portals`.`latitude`,' ',`portals`.`longitude`,')'),4326) AS `position` from `portals` ;

COMMIT;