-- Create Metabase database
CREATE DATABASE metabase_db;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE metabase_db TO plant_user;

-- Switch to metabase database
\c metabase_db;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";