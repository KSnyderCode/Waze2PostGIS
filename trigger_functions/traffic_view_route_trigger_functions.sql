--updates each alert to add what county it took place in
CREATE FUNCTION route_county_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.traffic_view_routes
   SET route_county = production.municipalities.county_name
   FROM production.municipalities
   WHERE traffic_view_routes.route_county IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(traffic_view_routes.geom));
     
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER route_county
   AFTER INSERT
   ON production.traffic_view_routes
   FOR EACH STATEMENT
       EXECUTE PROCEDURE route_county_function();

       -- --updates each alert to add what municipality it took place in
CREATE FUNCTION route_municipality_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.traffic_view_routes
   SET route_muni = production.municipalities.full_name
   FROM production.municipalities
   WHERE traffic_view_routes.route_muni IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(traffic_view_routes.geom));
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER route_municipality
   AFTER INSERT
   ON production.traffic_view_routes
   FOR EACH STATEMENT
       EXECUTE PROCEDURE route_municipality_function();

--calculates the travel_azimuth value by using ST_Azimuth(ST_StartPoint, ST_EndPoint) of the line geometry
-- calculations are for Irregularities table
CREATE FUNCTION route_azimuth_calculation() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.traffic_view_routes
   SET travel_azimuth = CAST(TRUNC(degrees(ST_Azimuth(ST_StartPoint(traffic_view_routes.geom), ST_EndPoint(traffic_view_routes.geom)))) AS INTEGER)
   WHERE travel_azimuth IS NULL;
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER route_azimuth
   AFTER INSERT
   ON production.traffic_view_routes
   FOR EACH STATEMENT
       EXECUTE PROCEDURE route_azimuth_calculation();

--updates each alert to assign the direction of travel based off of the travel_azimuth value
-- assignments are made for the Irregularities
CREATE FUNCTION route_heading_assignment() 
   RETURNS TRIGGER
AS $$
BEGIN

   UPDATE production.traffic_view_routes
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

CREATE TRIGGER route_heading
   AFTER INSERT
   ON production.traffic_view_routes
   FOR EACH STATEMENT
       EXECUTE PROCEDURE route_heading_assignment();



