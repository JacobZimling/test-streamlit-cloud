DROP VIEW IF EXISTS w_race_identifier;
create view w_race_identifier as
SELECT  race_id,
		CONCAT(
            race_date,
            race_venue,
            race_name
        ) AS race_identifier,
        case race_heat
        	when 'e' then True
        	else False
        end as elimination_race
	from race_info;


DROP VIEW IF EXISTS w_race_graph;
create view w_race_graph as		
SELECT *
FROM (
    SELECT 
    	dt.race_identifier,
        dt.driver_id, 
        dt.race_time, 
        l.lap, 
        l.race_time AS lap_race_time, 
/*        dt.race_time - l.race_time AS time_diff,*/
        ROW_NUMBER() OVER (
            PARTITION BY dt.race_identifier, dt.driver_id, dt.race_time
            ORDER BY dt.race_time - l.race_time
        ) AS rn
    FROM w_driver_times as dt
    LEFT JOIN (
	    SELECT wri.race_identifier, rl.driver_id, rl.race_time, rl.lap
        FROM race_laps as rl
        	JOIN w_race_identifier as wri
        		ON rl.race_id=wri.race_id
       ) as l
        ON dt.race_identifier=l.race_identifier
    	and dt.driver_id = l.driver_id
        AND dt.race_time >= l.race_time
) sub
WHERE 

rn = 1
/*and 
race_identifier='2025-06-15Slangerup1' and driver_id='Zimling'
*/
ORDER BY driver_id, race_time, lap;


/* Race result */
DROP VIEW IF EXISTS w_race_result;
CREATE VIEW w_race_result as
SELECT
    r.*,
    p.point
	FROM (
		SELECT
        	race_identifier,
			ROW_NUMBER() OVER(
                PARTITION BY race_identifier
				ORDER BY race_identifier, lap DESC, race_time_dt
			) AS rank,
			driver_id,
			race_time_dt,
			lap
		FROM (
			SELECT
            	wri.race_identifier,
				rl.driver_id,
				rl.race_time_dt,
				rl.lap,
				ROW_NUMBER() OVER(
					PARTITION BY wri.race_identifier, rl.driver_id
					ORDER BY wri.race_identifier, rl.driver_id, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
            	JOIN w_race_identifier as wri
            		ON rl.race_id=wri.race_id
		) sub
		WHERE rn = 1
	) AS r
	LEFT JOIN race_points AS p
		ON r.rank = p.rank
	ORDER BY r.race_identifier, r.rank;

/* driver_name */
 INSERT INTO `driver_name` (`driver_id`, `driver_name`) VALUES ('Peter', 'Peter Seyfarth'), ('Jesper K', 'Jesper Klausen'), ('Jesper', 'Jesper Seyfarth'), ('Palle', 'Palle Larsen'), ('Mike', 'Mike Pedersen'), ('John', 'John Dalsgaard'), ('Alex', 'Alex Pedersen'), ('Zimling', 'Jacob Zimling'), ('Niels', 'Niels Bay'), ('Leif', 'Leif Nebbelunde'), ('Jacob G', 'Jacob Gottlieb'), ('Brian', 'Brian Nielsen'), ('Jacob Z', 'Jacob Zimling'), ('Jesper S', 'Jesper Seyfarth'),('Zimling', 'Jacob Zimling'), ('Jacob', 'Jacob Gottlieb');

/* year_race */
/*
*/
insert into race_result (result_identifier, driver_name, point)
SELECT
    r.result_identifier,
    r.driver_name,
    sum(p.point) as point
	FROM (
		SELECT
        	result_identifier,
            race_identifier,
			ROW_NUMBER() OVER(
                PARTITION BY result_identifier, race_identifier
				ORDER BY result_identifier, race_identifier, lap DESC, race_time_dt
			) AS rank,
        	driver_name,
			race_time_dt,
			lap
		FROM (
			SELECT
            	result_id.year_type as result_identifier,
            	race_id.race_identifier,
            	driver.driver_name,
				rl.race_time_dt,
				rl.lap,
				ROW_NUMBER() OVER(
					PARTITION BY result_id.year_type, race_id.race_identifier, driver.driver_name
					ORDER BY result_id.year_type, race_id.race_identifier, driver.driver_name, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
            	JOIN w_race_identifier as race_id
            		ON rl.race_id=race_id.race_id
            	JOIN w_result_identifier as result_id
            		ON rl.race_id=result_id.race_id
            	LEFT JOIN driver_name as driver
            		ON rl.driver_id=driver.driver_id
		) sub
		WHERE rn = 1
	) AS r
	LEFT JOIN race_points AS p
		ON r.rank = p.rank
    GROUP BY r.result_identifier, r.driver_name
    ORDER BY r.result_identifier, point DESC
/*        
	ORDER BY r.race_identifier, r.rank;
 */

/* year_type_date */
/*
*/
insert into race_result (result_identifier, driver_name, point)
SELECT
    r.result_identifier,
    r.driver_name,
    sum(p.point) as point
	FROM (
		SELECT
        	result_identifier,
            race_identifier,
			ROW_NUMBER() OVER(
                PARTITION BY result_identifier, race_identifier
				ORDER BY result_identifier, race_identifier, lap DESC, race_time_dt
			) AS rank,
        	driver_name,
			race_time_dt,
			lap
		FROM (
			SELECT
            	result_id.year_type_date as result_identifier,
            	race_id.race_identifier,
            	driver.driver_name,
				rl.race_time_dt,
				rl.lap,
				ROW_NUMBER() OVER(
					PARTITION BY result_id.year_type_date, race_id.race_identifier, driver.driver_name
					ORDER BY result_id.year_type_date, race_id.race_identifier, driver.driver_name, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
            	JOIN w_race_identifier as race_id
            		ON rl.race_id=race_id.race_id
            	JOIN w_result_identifier as result_id
            		ON rl.race_id=result_id.race_id
            	LEFT JOIN driver_name as driver
            		ON rl.driver_id=driver.driver_id
		) sub
		WHERE rn = 1
	) AS r
	LEFT JOIN race_points AS p
		ON r.rank = p.rank
    GROUP BY r.result_identifier, r.driver_name
    ORDER BY r.driver_name, r.result_identifier, point DESC
/*        
    ORDER BY r.result_identifier, point DESC
	ORDER BY r.race_identifier, r.rank;
 */

/* year_type_date_race */
insert into race_result (result_identifier, rank, driver_name, race_time_dt, lap, point)
SELECT
    r.result_identifier,
    r.rank,
    r.driver_name,
    r.race_time_dt,
    r.lap,
    sum(p.point) as point
	FROM (
		SELECT
        	result_identifier,
            race_identifier,
			ROW_NUMBER() OVER(
                PARTITION BY result_identifier, race_identifier
				ORDER BY result_identifier, race_identifier, lap DESC, race_time_dt
			) AS rank,
        	driver_name,
			race_time_dt,
			lap
		FROM (
			SELECT
            	result_id.year_type_date_race as result_identifier,
            	race_id.race_identifier,
            	driver.driver_name,
				rl.race_time_dt,
				rl.lap,
				ROW_NUMBER() OVER(
					PARTITION BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name
					ORDER BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
            	JOIN w_race_identifier as race_id
            		ON rl.race_id=race_id.race_id
            	JOIN w_result_identifier as result_id
            		ON rl.race_id=result_id.race_id
            	LEFT JOIN driver_name as driver
            		ON rl.driver_id=driver.driver_id
		) sub
		WHERE rn = 1
	) AS r
	LEFT JOIN race_points AS p
		ON r.rank = p.rank
    GROUP BY r.result_identifier, r.driver_name
    ORDER BY r.result_identifier, point DESC

SELECT
    r.result_identifier,
    r.rank,
    r.driver_name,
    r.race_time_dt,
    r.lap,
    r.elimination_race,
    /*
    max(r.lap) as max_lap,
    */
    max(r.lap) OVER (
    	partition by r.result_identifier
    ) as max_lap,
    /*
    calculated max_lap as max_lap2,
    sum(
    	case 
    		when r.elimination_race=1 and r.lap<3 then 0
    		when r.elimination_race=0 and r.lap<max(r.lap) OVER (partition by r.result_identifier)/2 then 0 
    		else p.point
    	end
    ) as point_50pl,
    */
    sum(
    	case 
    		when r.elimination_race=1 and r.lap<3 then 0
    		when r.elimination_race=0 and r.race_time_dt<'1900-01-01 00:03:30' then 0 
    		else p.point
    	end
    ) as point_3_30,
    sum(
    	case 
    		when r.elimination_race=1 and r.lap<3 then 0
    		else p.point
    	end
    ) as point_E3
	,p.point as point
	FROM (
		SELECT
        	result_identifier,
            race_identifier,
        	elimination_race,
			ROW_NUMBER() OVER(
                PARTITION BY result_identifier, race_identifier
				ORDER BY result_identifier, race_identifier, lap DESC, race_time_dt
			) AS rank,
        	driver_name,
			race_time_dt,
			lap
		FROM (
			SELECT
            	result_id.year_type_date_race as result_identifier,
            	race_id.race_identifier,
            	race_id.elimination_race,
            	driver.driver_name,
				rl.race_time_dt,
				rl.lap,
				ROW_NUMBER() OVER(
					PARTITION BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name
					ORDER BY result_id.year_type_date_race, race_id.race_identifier, driver.driver_name, rl.lap DESC
				) AS rn
			FROM `race_laps` as rl
            	JOIN w_race_identifier as race_id
            		ON rl.race_id=race_id.race_id
            	JOIN w_result_identifier as result_id
            		ON rl.race_id=result_id.race_id
            	LEFT JOIN driver_name as driver
            		ON rl.driver_id=driver.driver_id
            WHERE not(result_id.year_type_date_race='2025¤4wd¤2025-05-18¤4' and driver.driver_name='Jacob Gottlieb')
		) sub
		WHERE rn = 1
	) AS r
	LEFT JOIN race_points AS p
		ON r.rank = p.rank
    GROUP BY r.result_identifier, r.driver_name
    ORDER BY r.result_identifier, point DESC

/* race_result using WITH */
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
			lap
		FROM (
			SELECT
		    	result_id.year_type_date_race,
		    	result_id.year_type_date, 
		    	result_id.year_type,
		    	race_id.race_identifier,
		    	race_id.elimination_race,
		    	driver.driver_name,
				rl.race_time_dt,
				rl.lap,
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
				WHEN elimination_race=1 and lap<3 THEN 0
				WHEN elimination_race=0 and lap<lap_point_limit THEN 0
				ELSE point
			END as result_point,
			CASE 
				WHEN elimination_race=1 and lap<3 THEN 0
				WHEN elimination_race=0 and race_time_dt<'1900-01-01 00:07:00' THEN 0
				WHEN elimination_race=0 and lap<lap_point_limit THEN 0
				ELSE point
			END as result_point_2,
			CASE 
				WHEN elimination_race=1 and lap<3 THEN 'DNF'
				WHEN elimination_race=0 and lap<lap_point_limit THEN 'DNF'
				ELSE ''
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
