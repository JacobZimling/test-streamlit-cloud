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
				ORDER BY race_identifier, lap DESC, race_time
			) AS rank,
			driver_id,
			race_time,
			lap
		FROM (
			SELECT
            	wri.race_identifier,
				rl.driver_id,
				rl.race_time,
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
