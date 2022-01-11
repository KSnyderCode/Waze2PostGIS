CREATE VIEW municipal_overview AS
SELECT municipality, county, subtype, COUNT(subtype)
FROM production.alerts
GROUP BY municipality, county, subtype
ORDER BY county, municipality, subtype ASC;

CREATE VIEW county_overview AS
SELECT county, subtype, COUNT(subtype)
FROM production.alerts
GROUP BY county, subtype
ORDER BY county, subtype ASC;

CREATE VIEW county_totals AS
SELECT county, COUNT(county)
FROM production.alerts
GROUP BY county
ORDER BY county ASC;