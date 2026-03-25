CREATE TEMPORARY TABLE _laps as 
    SELECT td.race_time, td.driver_id, l.lap, l.race_time as lap_race_time, td.race_time-l.race_time as time_diff
        FROM (
            SELECT t.race_time, d.driver_id
                FROM (
                    SELECT distinct race_time
                        FROM race_laps
                        WHERE race_id in (SELECT race_id FROM race_info WHERE race_date="2025-06-15" and race_name="1")
                ) as t
                JOIN (
                    SELECT distinct driver_id
                        FROM race_laps
                        WHERE race_id in (SELECT race_id FROM race_info WHERE race_date="2025-06-15" and race_name="1")
                ) as d
        ) as td
        LEFT JOIN (
            SELECT driver_id, lap, race_time
                FROM race_laps
                WHERE race_id=2
        ) as l
            ON td.driver_id=l.driver_id
                and td.race_time-l.race_time>=0
;
SELECT m.driver_id, m.race_time, l.lap
from (
SELECT driver_id, race_time, min(time_diff) as time_diff
from _laps
GROUP BY driver_id, race_time
) as m
LEFT JOIN _laps as l
	ON m.driver_id=l.driver_id and m.race_time=l.race_time and m.time_diff=l.time_diff
ORDER BY driver_id, race_time;
