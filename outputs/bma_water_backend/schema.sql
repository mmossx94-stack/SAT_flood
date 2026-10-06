-- Proposed PostgreSQL schema. Not executed.
CREATE TABLE water_snapshots (
 snapshot_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 source_url text NOT NULL, fetched_at timestamptz NOT NULL,
 raw_payload jsonb NOT NULL, metadata jsonb NOT NULL
);
CREATE TABLE water_observations (
 snapshot_id bigint NOT NULL REFERENCES water_snapshots(snapshot_id),
 source_station_id bigint NOT NULL, station_code text,
 district_code char(4), observed_at timestamptz,
 source_status text, quality_reason text NOT NULL,
 normalized jsonb NOT NULL, raw_station jsonb NOT NULL,
 PRIMARY KEY (snapshot_id, source_station_id)
);
CREATE INDEX water_observation_station_time ON water_observations(source_station_id, observed_at DESC);
CREATE TABLE water_district_status (
 snapshot_id bigint NOT NULL REFERENCES water_snapshots(snapshot_id),
 district_code char(4) NOT NULL, status text NOT NULL
 CHECK (status IN ('normal','warning','critical','unknown')),
 color char(7) NOT NULL, partial_data boolean NOT NULL,
 station_count integer NOT NULL, usable_station_count integer NOT NULL,
 details jsonb NOT NULL, PRIMARY KEY(snapshot_id, district_code)
);