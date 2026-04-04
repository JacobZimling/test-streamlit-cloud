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

