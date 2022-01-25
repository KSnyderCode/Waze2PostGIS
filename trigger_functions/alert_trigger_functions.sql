--updates each alert to add what county it took place in
CREATE FUNCTION alert_county_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.alerts
   SET county = production.municipalities.county_name
   FROM production.municipalities
   WHERE alerts.county IS NULL AND ST_Intersects(municipalities.wkb_geometry, alerts.geom);
     
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER alert_county
   AFTER INSERT
   ON production.alerts
   FOR EACH STATEMENT
       EXECUTE PROCEDURE alert_county_function();

       -- --updates each alert to add what municipality it took place in
CREATE FUNCTION alert_municipality_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.alerts
   SET municipality = production.municipalities.full_name
   FROM production.municipalities
   WHERE alerts.municipality IS NULL AND ST_Intersects(municipalities.wkb_geometry, alerts.geom);
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER alert_municipality
   AFTER INSERT
   ON production.alerts
   FOR EACH STATEMENT
       EXECUTE PROCEDURE alert_municipality_function();

--updates each alert to assign the direction of travel based off of the MAGVAR value
CREATE FUNCTION alert_heading_assignment() 
   RETURNS TRIGGER
AS $$
BEGIN

   UPDATE production.alerts
   SET travel_dir = CASE 
      WHEN magvar BETWEEN 0 and 45 OR magvar BETWEEN 315 and 359 THEN 'N'
      WHEN magvar BETWEEN 45 AND 135 THEN 'E'
      WHEN magvar BETWEEN 135 AND 225 THEN 'S'
      WHEN magvar BETWEEN 225 AND 315 THEN 'W'
      END
   WHERE travel_dir IS NULL;

   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER alert_heading
   AFTER INSERT
   ON production.alerts
   FOR EACH STATEMENT
       EXECUTE PROCEDURE alert_heading_assignment();

