DELETE FROM race_graph WHERE race_identifier='2025-05-18Birkerød4';

INSERT INTO race_graph (
		race_identifier, 
		driver_name,
		race_time_dt,
		lap
	)
		WITH 
			laps as (
				SELECT 
					wri.race_identifier, 
					rl.driver_id, 
					rl.race_time_dt, 
					rl.lap
				FROM race_laps as rl 
					JOIN w_race_identifier as wri 
						ON rl.race_id=wri.race_id 
			),
			racetime_laps as (
				SELECT 
					dt.race_identifier, 
					dt.driver_id, 
					dt.race_time_dt, 
					l.lap, 
					ROW_NUMBER() OVER ( 
						PARTITION BY dt.race_identifier, dt.driver_id, dt.race_time_dt 
						ORDER BY dt.race_time_dt - l.race_time_dt 
					) AS rn 
				FROM w_driver_times as dt 
				LEFT JOIN laps as l 
					ON dt.race_identifier=l.race_identifier 
					and dt.driver_id = l.driver_id 
					AND dt.race_time_dt >= l.race_time_dt 
				WHERE dt.race_identifier='2026-04-12Birkerød1' 
			)
			SELECT 
				rtl.race_identifier, 
				driver.driver_name,
				rtl.race_time_dt,
				CASE DSQ.DSQ
					WHEN 1 THEN 0
					ELSE coalesce(rtl.lap, 0) 
				END as lap
				FROM racetime_laps as rtl
					LEFT JOIN driver_name as driver
						ON rtl.driver_id=driver.driver_id
					LEFT JOIN (
						SELECT distinct w_race_identifier.race_identifier, w_result_identifier.year_type_date_race 
							FROM w_race_identifier  
							JOIN w_result_identifier  
								ON w_race_identifier.race_id=w_result_identifier.race_id 
					) as wri
						ON rtl.race_identifier=wri.race_identifier
					LEFT JOIN race_disqualified as DSQ
						ON wri.year_type_date_race=DSQ.year_type_date_race
							and driver.driver_name=DSQ.driver_name
				WHERE rtl.rn = 1 
;
