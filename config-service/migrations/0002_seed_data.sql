-- Seed dummy data for initial development/testing
-- Applications
INSERT INTO applications (id, name, comments) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FAV', 'alpha-app', 'Primary demo application'),
  ('01ARZ3NDEKTSV4RRFFQ69G5FAW', 'beta-app', 'Secondary demo application'),
  ('01ARZ3NDEKTSV4RRFFQ69G5FAX', 'gamma-app', 'Tertiary demo application')
ON CONFLICT (id) DO NOTHING;

-- Configurations for alpha-app
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB1', '01ARZ3NDEKTSV4RRFFQ69G5FAV', 'default', 'Default settings',
   '{"feature_flags": {"new_nav": true}, "retries": 3}'),
  ('01ARZ3NDEKTSV4RRFFQ69G5FB2', '01ARZ3NDEKTSV4RRFFQ69G5FAV', 'prod', 'Production settings',
   '{"feature_flags": {"new_nav": false}, "retries": 5, "cache_ttl": 300}')
ON CONFLICT (id) DO NOTHING;

-- Configurations for beta-app
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB3', '01ARZ3NDEKTSV4RRFFQ69G5FAW', 'default', 'Beta defaults',
   '{"theme": "dark", "limits": {"qps": 50}}')
ON CONFLICT (id) DO NOTHING;

-- Configurations for gamma-app
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB4', '01ARZ3NDEKTSV4RRFFQ69G5FAX', 'default', 'Gamma defaults',
   '{"maintenance": false, "regions": ["us-east-1", "eu-west-1"]}')
ON CONFLICT (id) DO NOTHING;

-- Additional configs to reach ~12 total records across both tables
-- Alpha: add 'dev'
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB5', '01ARZ3NDEKTSV4RRFFQ69G5FAV', 'dev', 'Development settings',
   '{"feature_flags": {"new_nav": true, "beta_banner": true}, "retries": 1, "log_level": "DEBUG"}')
ON CONFLICT (id) DO NOTHING;

-- Beta: add 'dev' and 'prod'
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB6', '01ARZ3NDEKTSV4RRFFQ69G5FAW', 'dev', 'Beta dev settings',
   '{"theme": "light", "limits": {"qps": 20}, "features": {"ab_test": true}}'),
  ('01ARZ3NDEKTSV4RRFFQ69G5FB7', '01ARZ3NDEKTSV4RRFFQ69G5FAW', 'prod', 'Beta prod settings',
   '{"theme": "dark", "limits": {"qps": 100}, "cache": {"enabled": true, "ttl": 600}}')
ON CONFLICT (id) DO NOTHING;

-- Gamma: add 'dev' and 'staging'
INSERT INTO configurations (id, application_id, name, comments, config) VALUES
  ('01ARZ3NDEKTSV4RRFFQ69G5FB8', '01ARZ3NDEKTSV4RRFFQ69G5FAX', 'dev', 'Gamma dev settings',
   '{"maintenance": false, "regions": ["us-east-1"], "rollout": {"percent": 10}}'),
  ('01ARZ3NDEKTSV4RRFFQ69G5FB9', '01ARZ3NDEKTSV4RRFFQ69G5FAX', 'staging', 'Gamma staging settings',
   '{"maintenance": true, "regions": ["eu-west-1"], "rollout": {"percent": 50}}')
ON CONFLICT (id) DO NOTHING;
