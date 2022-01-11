--updates each alert to add what county it took place in
CREATE FUNCTION irregularity_county_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.irregularities
   SET irreg_county = production.municipalities.county_name
   FROM production.municipalities
   WHERE irregularities.irreg_county IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(irregularities.geom));
     
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER irregularity_county
   AFTER INSERT
   ON production.irregularities
   FOR EACH STATEMENT
       EXECUTE PROCEDURE irregularity_county_function();

       -- --updates each alert to add what municipality it took place in
CREATE FUNCTION irregularity_municipality_function() 
   RETURNS TRIGGER
AS $$
BEGIN
   UPDATE production.irregularities
   SET irreg_muni = production.municipalities.full_name
   FROM production.municipalities
   WHERE irregularities.irreg_muni IS NULL AND ST_Intersects(municipalities.wkb_geometry, ST_StartPoint(irregularities.geom));
   
   RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER irregularity_municipality
   AFTER INSERT
   ON production.irregularities
   FOR EACH STATEMENT
       EXECUTE PROCEDURE irregularity_municipality_function();



