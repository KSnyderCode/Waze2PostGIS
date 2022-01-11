CREATE INDEX alerts_geom_idx
    ON production.alerts
    USING GIST (geom);

CREATE INDEX jams_geom_idx
    ON production.detected_jams
    USING GIST (geom);

CREATE INDEX irreg_geom_idx
    ON production.irregularities
    USING GIST (geom);