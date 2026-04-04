DROP VIEW IF EXISTS w_race_info;

CREATE  VIEW `w_race_info`  AS 
	SELECT 
		`race_info`.`race_id` AS `race_id`, 
		CASE `race_info`.`race_name` 
			WHEN '2wd' THEN `race_info`.`race_name` 
			ELSE '4wd' 
		END AS `race_type`, 
		year(`race_info`.`race_date`) AS `race_year`, 
		date_format(`race_info`.`race_date`,'%Y-%m-%d') AS `race_date`, 
		`race_info`.`race_venue` AS `race_venue`, 
		concat(date_format(`race_info`.`race_date`,'%Y-%m-%d'),`race_info`.`race_venue`) AS `date_venue`, 
		concat(`race_info`.`race_venue`,' (',date_format(`race_info`.`race_date`,'%e. %M'),')') AS `venue_label`, 
		`race_info`.`race_name` AS `race_name`, 
		CASE `race_info`.`race_name`
			WHEN '2wd' THEN '0' 
			ELSE `race_info`.`race_name` 
		END as `race_order`
	FROM `race_info` 
	ORDER BY race_date, race_order
;
