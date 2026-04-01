DROP VIEW IF EXISTS w_race_identifier;
create view w_race_identifier as
SELECT  race_id,
		CONCAT(
            race_date,
            race_venue,
            race_name
        ) AS race_identifier
	from race_info;


DROP VIEW IF EXISTS w_driver_times;
create view w_driver_times as
SELECT t.race_identifier, d.driver_id, t.race_time
                FROM (
                    SELECT distinct race_identifier, race_time
                        FROM race_laps as rl
                    	join w_race_identifier as wri
							ON rl.race_id=wri.race_id
                ) as t
                JOIN (
                    SELECT distinct race_identifier, driver_id
                        FROM race_laps as rl
                    	join w_race_identifier as wri
							ON rl.race_id=wri.race_id
                ) as d
            	ON t.race_identifier=d.race_identifier;
		

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
