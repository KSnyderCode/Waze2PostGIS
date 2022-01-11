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



