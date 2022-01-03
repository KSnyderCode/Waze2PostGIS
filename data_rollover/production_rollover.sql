INSERT INTO production.alerts
SELECT time_stamp, 
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
        no_thumbsup
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
        turn_type
FROM staging.detected_jams AS staging
WHERE NOT EXISTS (
    SELECT * FROM production.alerts AS production
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
        no_thumbsup
FROM staging.detected_jams AS staging
WHERE NOT EXISTS (
    SELECT * FROM production.alerts AS production
    WHERE staging.uuid = production.uuid);