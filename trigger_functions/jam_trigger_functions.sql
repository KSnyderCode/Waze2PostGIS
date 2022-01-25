--updates each alert to add what county it took place in
CREATE FUNCTION jam_county_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.detected_jams
   SET jam_county = production.municipalities.county_name
   FROM production.municipalities
   WHERE detected_jams.jam_county IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(detected_jams.geom));
     
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER jam_county
   AFTER INSERT
   ON production.detected_jams
   FOR EACH STATEMENT
       EXECUTE PROCEDURE jam_county_function();

       -- --updates each alert to add what municipality it took place in
CREATE FUNCTION jam_municipality_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.detected_jams
   SET jam_muni = production.municipalities.full_name
   FROM production.municipalities
   WHERE detected_jams.jam_muni IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(detected_jams.geom));
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER jam_municipality
   AFTER INSERT
   ON production.detected_jams
   FOR EACH STATEMENT
       EXECUTE PROCEDURE jam_municipality_function();

--calculates the travel_azimuth value by using ST_Azimuth(ST_StartPoint, ST_EndPoint) of the line geometry
--calculations for Detected Jams table
CREATE FUNCTION detected_jam_azimuth_calculation() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.detected_jams
   SET travel_azimuth = CAST(TRUNC(degrees(ST_Azimuth(ST_StartPoint(detected_jams.geom), ST_EndPoint(detected_jams.geom)))) AS INTEGER)
   WHERE travel_azimuth IS NULL;
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER detected_jam_azimuth
   AFTER INSERT
   ON production.detected_jams
   FOR EACH STATEMENT
       EXECUTE PROCEDURE detected_jam_azimuth_calculation();

--updates each alert to assign the direction of travel based off of the travel_azimuth value
-- assignments are for Detected Jams table
CREATE FUNCTION detected_jam_heading_assignment() 
   RETURNS TRIGGER
AS $$
BEGIN

   UPDATE production.detected_jams
   SET travel_dir = CASE 
   	WHEN travel_azimuth BETWEEN 0 and 45 OR travel_azimuth BETWEEN 315 and 359 THEN 'N'
   	WHEN travel_azimuth BETWEEN 45 AND 135 THEN 'E'
   	WHEN travel_azimuth BETWEEN 135 AND 225 THEN 'S'
   	WHEN travel_azimuth BETWEEN 225 AND 315 THEN 'W'
   	END
   WHERE travel_dir IS NULL;
  
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER detected_jam_heading
   AFTER INSERT
   ON production.detected_jams
   FOR EACH STATEMENT
       EXECUTE PROCEDURE detected_jam_heading_assignment();



