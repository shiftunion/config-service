-- applications
CREATE TABLE applications (
  id TEXT PRIMARY KEY,
  name VARCHAR(256) NOT NULL UNIQUE,
  comments VARCHAR(1024)
);

-- configurations
CREATE TABLE configurations (
  id TEXT PRIMARY KEY,
  application_id TEXT NOT NULL REFERENCES applications(id),
  name VARCHAR(256) NOT NULL,
  comments VARCHAR(1024),
  config JSONB NOT NULL,
  CONSTRAINT configurations_unique_name_per_app UNIQUE (application_id, name)
);

-- helpful indexes
CREATE INDEX idx_configurations_app_id ON configurations(application_id);
