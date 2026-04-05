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
