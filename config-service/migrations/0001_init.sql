-- applications
CREATE TABLE IF NOT EXISTS applications (
  id TEXT PRIMARY KEY,
  name VARCHAR(256) NOT NULL UNIQUE,
  comments VARCHAR(1024)
);

-- configurations
CREATE TABLE IF NOT EXISTS configurations (
  id TEXT PRIMARY KEY,
  application_id TEXT NOT NULL REFERENCES applications(id),
  name VARCHAR(256) NOT NULL,
  comments VARCHAR(1024),
  config JSONB NOT NULL,
  CONSTRAINT configurations_unique_name_per_app UNIQUE (application_id, name)
);

-- helpful indexes
CREATE INDEX IF NOT EXISTS idx_configurations_app_id ON configurations(application_id);
