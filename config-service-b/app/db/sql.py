"""
SQL queries.
"""

# Applications
APPLICATIONS_SELECT = """
SELECT id, name, comments FROM applications
"""

APPLICATIONS_SELECT_BY_ID = APPLICATIONS_SELECT + " WHERE id = %s"

APPLICATIONS_SELECT_BY_NAME = APPLICATIONS_SELECT + " WHERE name = %s"

APPLICATIONS_INSERT = """
INSERT INTO applications (id, name, comments) VALUES (%s, %s, %s)
"""

APPLICATIONS_UPDATE = """
UPDATE applications SET name = %s, comments = %s WHERE id = %s
"""

APPLICATIONS_DELETE = """
DELETE FROM applications WHERE id = %s
"""

APPLICATIONS_EXISTS = """
SELECT 1 FROM applications WHERE id = %s
"""

# Configurations
CONFIGURATIONS_SELECT = """
SELECT id, application_id, name, comments, config FROM configurations
"""

CONFIGURATIONS_SELECT_BY_ID = CONFIGURATIONS_SELECT + " WHERE id = %s"

CONFIGURATIONS_SELECT_BY_APP = CONFIGURATIONS_SELECT + " WHERE application_id = %s"

CONFIGURATIONS_SELECT_BY_APP_AND_NAME = (
    CONFIGURATIONS_SELECT + " WHERE application_id = %s AND name = %s"
)

CONFIGURATIONS_INSERT = """
INSERT INTO configurations (id, application_id, name, comments, config)
VALUES (%s, %s, %s, %s, %s)
"""

CONFIGURATIONS_UPDATE = """
UPDATE configurations SET name = %s, comments = %s, config = %s WHERE id = %s
"""

CONFIGURATIONS_DELETE = """
DELETE FROM configurations WHERE id = %s
"""

CONFIGURATIONS_EXISTS = """
SELECT 1 FROM configurations WHERE id = %s
"""

# Application with related configurations count
APPLICATIONS_WITH_CONFIG_COUNT = """
SELECT a.id, a.name, a.comments,
       COUNT(c.id) as configurations_count
FROM applications a
LEFT JOIN configurations c ON a.id = c.application_id
GROUP BY a.id, a.name, a.comments
"""

APPLICATIONS_WITH_CONFIG_COUNT_BY_ID = (
    APPLICATIONS_WITH_CONFIG_COUNT + " HAVING a.id = %s"
)
