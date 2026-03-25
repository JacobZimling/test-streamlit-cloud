DROP VIEW IF EXISTS all_race_time_laps;
CREATE VIEW all_race_time_laps as 
SELECT race_identifier, race_time, driver_id, max(lap) as lap
FROM (  
	SELECT concat(ri.race_date, ri.race_venue, ri.race_name) as race_identifier, td.race_id, td.race_time, td.driver_id, l.lap, l.race_time as lap_race_time, td.race_time-l.race_time as time_diff
        FROM (
            SELECT t.race_id, t.race_time, d.driver_id
                FROM (
                    SELECT distinct race_id, race_time
                        FROM race_laps
                ) as t
                JOIN (
                    SELECT distinct race_id, driver_id
                        FROM race_laps
                ) as d
            	ON t.race_id=d.race_id
        ) as td
        LEFT JOIN (
            SELECT race_id, driver_id, lap, race_time
                FROM race_laps
        ) as l
            ON td.race_id=l.race_id 
            	and td.driver_id=l.driver_id
                and td.race_time-l.race_time>=0
		LEFT JOIN race_info as ri
        	ON td.race_id=ri.race_id
  )
GROUP by race_identifier, driver_id, race_time
order by race_identifier, driver_id, race_time, lap
;


DROP VIEW IF EXISTS
    all_race_time_laps;
CREATE VIEW all_race_time_laps AS SELECT
    race_identifier,
    race_time,
    driver_id,
    MAX(lap) AS lap
FROM
    (
    SELECT
        CONCAT(
            ri.race_date,
            ri.race_venue,
            ri.race_name
        ) AS race_identifier,
        td.race_id,
        td.race_time,
        td.driver_id,
        l.lap,
        l.race_time AS lap_race_time,
        td.race_time - l.race_time AS time_diff
    FROM
        (
        SELECT
            t.race_id,
            t.race_time,
            d.driver_id
        FROM
            (
            SELECT DISTINCT
                race_id,
                race_time
            FROM
                race_laps
        ) AS t
    JOIN(
        SELECT DISTINCT
            race_id,
            driver_id
        FROM
            race_laps
    ) AS d
ON
    t.race_id = d.race_id
    ) AS td
LEFT JOIN(
    SELECT race_id,
        driver_id,
        lap,
        race_time
    FROM
        race_laps
) AS l
ON
    td.race_id = l.race_id AND td.driver_id = l.driver_id AND td.race_time - l.race_time >= 0
LEFT JOIN race_info AS ri
ON
    td.race_id = ri.race_id
)
GROUP BY
    race_identifier,
    driver_id,
    race_time
ORDER BY
    race_identifier,
    driver_id,
    race_time,
    lap;
