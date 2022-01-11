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
       EXECUTE PROCEDURE alert_county_function();

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



