INSERT INTO production.alerts
SELECT  time_stamp, 
        geom,
        magvar,
        alert_type,
        subtype,
        report_description, 
        street,
        city,
        country,
        road_type,
        report_rating,
        uuid,
        confidence,
        reliability,
        no_thumbsup,
        municipality,
        alert_county
FROM staging.alerts AS staging
WHERE NOT EXISTS (
    SELECT * FROM production.alerts AS production
    WHERE staging.uuid = production.uuid);

INSERT INTO production.detected_jams
SELECT  id,
        time_stamp,
        geom, 
        street,
        city, 
        country,
        jam_speed,
        jam_speed_mph,
        jam_length,
        jam_length_ft,
        delay_seconds,
        delay_minutes,
        road_type,
        start_node,
        end_node, 
        jam_level,
        uuid,
        blocking_alert_uuid, 
        turn_line, 
        turn_type,
        jam_county,
        jam_muni
FROM staging.detected_jams AS staging
WHERE NOT EXISTS (
    SELECT * FROM production.detected_jams AS production
    WHERE staging.uuid = production.uuid);

INSERT INTO production.irregularities
SELECT  id, 
        geom, 
        detection_date,
        update_date,
        irregularity_type,
        start_node,
        end_node,
        speed,
        speed_mph,
        delay_seconds, 
        delay_minutes, 
        jam_length, 
        jam_length_ft,
        jam_trend, 
        street,
        city,
        country, 
        jam_severity, 
        jam_level,
        highway,
        drivers_count, 
        alerts_count,
        no_thumbsup,
        irreg_muni,
        irreg_county
FROM staging.irregularities AS staging
WHERE NOT EXISTS (
    SELECT * FROM production.irregularities AS production
    WHERE staging.id = production.id and staging.update_date = production.update_date); 

INSERT INTO production.traffic_view_routes
SELECT  route_name,
        to_name,
        from_name,
        historic_time,
        current_travel_time,
        jam_level,
        jam_length,
        jam_length_ft,
        route_id,
        route_type,
        travel_time_index,
        geom
FROM staging.traffic_view_routes AS staging
WHERE NOT EXISTS(
    SELECT * FROM production.traffic_view_routes AS production
    WHERE staging.route_id = production.route_id and staging.current_travel_time = production.current_travel_time);