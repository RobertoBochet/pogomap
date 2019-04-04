USE `pogomap`;

DELIMITER ;;
CREATE TRIGGER `portals_BEFORE_INSERT` BEFORE INSERT ON `portals` FOR EACH ROW BEGIN
	#Rand id
	DECLARE counter INT;
    IF (NEW.`id` = 0) THEN
		loop1: LOOP
			SET NEW.`id` = (SELECT FLOOR(RAND()*(999999-100000)+100000));
			SET @counter = (SELECT COUNT(*) FROM `portals` WHERE `id` = NEW.`id`);
			IF (@counter = 0) THEN
				LEAVE loop1;
			END IF;
		END LOOP;
    END IF;
    
    #Image protocol
    SET NEW.`image` = REPLACE(NEW.`image`, "http://", "//");
    SET NEW.`image` = REPLACE(NEW.`image`, "https://", "//");
END;;
DELIMITER ;

COMMIT;