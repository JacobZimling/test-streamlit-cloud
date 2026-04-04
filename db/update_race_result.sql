TRUNCATE TABLE race_result;

INSERT INTO race_result (
		result_identifier,
		rank,
		driver_name,
		race_time_dt,
		lap,
		point,
		DNF_DSQ
	)
WITH 
	last_lap AS (
		SELECT
			year_type_date_race,
	    	year_type_date, 
	    	year_type,
		    race_identifier,
			elimination_race,
			ROW_NUMBER() OVER(
		        PARTITION BY year_type_date_race, race_identifier
				ORDER BY year_type_date_race, race_identifier, lap DESC, race_time_dt
			) AS rank,
			driver_name,
			race_time_dt,
			lap,
			DSQ
		FROM (
			SELECT
		    	result_id.year_type_date_race,
		    	result_id.year_type_date, 
		    	result_id.year_type,
		    	race_id.race_identifier,
		    	race_id.elimination_race,
		    	driver.driver_name,
				CASE dsq.DSQ
					WHEN 1 then '1900-01-01 00:00:00'
					else rl.race_time_dt
				END as race_time_dt,
				CASE dsq.DSQ
					WHEN 1 then 0
					else rl.lap
				END as lap,
				dsq.DSQ,
				ROW_NUMBER() OVER(
					PARTITION BY result_id.year_type_date_race, result_id.year_type_date, result_id.year_type, race_id.race_identifier, driver.driver_name
					ORDER BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
		    	JOIN w_race_identifier as race_id
		    		ON rl.race_id=race_id.race_id
		    	JOIN w_result_identifier as result_id
		    		ON rl.race_id=result_id.race_id
		    	LEFT JOIN driver_name as driver
		    		ON rl.driver_id=driver.driver_id
		    	LEFT JOIN race_disqualified as dsq
		    		ON result_id.year_type_date_race=dsq.year_type_date_race
		    			and rl.driver_id=dsq.driver_id
/*
		    WHERE not(result_id.year_type_date_race='2025¤4wd¤2025-05-18¤4' and driver.driver_name='Jacob Gottlieb')
*/
		) sub
		WHERE rn = 1
	),
	point_info AS (
		SELECT 
		    ll.year_type_date_race,
	    	ll.year_type_date, 
	    	ll.year_type,
		    ll.rank,
		    ll.driver_name,
		    ll.race_time_dt,
		    ll.lap,
		    ll.DSQ,
		    max(ll.lap) OVER (
		    	partition by ll.year_type_date_race
		    )/2 as lap_point_limit,
		    ll.elimination_race,
		    p.point
		FROM last_lap as ll
			LEFT JOIN race_points as p
				ON ll.rank = p.rank
	    ORDER BY ll.year_type_date_race, p.point DESC
	),
	point_dnf as (
		SELECT 
		    year_type_date_race,
	    	year_type_date, 
	    	year_type,
		    rank,
		    driver_name,
		    race_time_dt,
		    lap,
		    lap_point_limit,
		    elimination_race,
		    point,
			CASE 
				WHEN DSQ=1 then 0
				WHEN elimination_race=1 and lap<3 THEN 0
				WHEN elimination_race=0 and lap<lap_point_limit THEN 0
				ELSE point
			END as result_point,
			CASE 
				WHEN DSQ=1 then 0
				WHEN elimination_race=1 and lap<3 THEN 0
				WHEN elimination_race=0 and race_time_dt<'1900-01-01 00:07:00' THEN 0
				WHEN elimination_race=0 and lap<lap_point_limit THEN 0
				ELSE point
			END as result_point_2,
			CASE 
				WHEN DSQ=1 then 'DSQ'
				WHEN elimination_race=1 and lap<3 THEN 'DNF'
				WHEN elimination_race=0 and lap<lap_point_limit THEN 'DNF'
				ELSE NULL
			END as DNF_DSQ
		FROM point_info
	),
	final_result AS (
		SELECT 
			year_type as race_identifier,
			ROW_NUMBER() OVER (
				PARTITION BY race_identifier
				ORDER BY race_identifier, point DESC
			) as rank,
			driver_name,
			NULL as race_time_dt,
			NULL as lap,
			sum(result_point) as point,
			sum(result_point_2) as point_2,
			NULL as DNF_DSQ
			FROM point_dnf 
			GROUP BY year_type, driver_name
		UNION ALL
		SELECT 
			year_type_date as race_identifier,
			ROW_NUMBER() OVER (
				PARTITION BY race_identifier
				ORDER BY race_identifier, point DESC
			) as rank,
			driver_name,
			NULL as race_time_dt,
			NULL as lap,
			sum(result_point) as point,
			sum(result_point_2) as point_2,
			NULL as DNF_DSQ
			FROM point_dnf 
			GROUP BY year_type_date, driver_name
		UNION ALL
		SELECT 
			year_type_date_race as race_identifier,
			ROW_NUMBER() OVER (
				PARTITION BY race_identifier
				ORDER BY race_identifier, lap DESC, point DESC
			) as rank,
			driver_name,
			race_time_dt,
			lap,
/*			sum(result_point) as point,
			sum(result_point_2) as point_2*/
			result_point as point,
			result_point_2 as point_2,
			DNF_DSQ
			FROM point_dnf 
/*			GROUP BY year_type_date_race, driver_name*/
		/*
		*/	
			order by race_identifier, rank 
	)
	SELECT
		race_identifier,
		rank,
		driver_name,
		race_time_dt,
		lap,
		point,
		DNF_DSQ
		FROM final_result
;
