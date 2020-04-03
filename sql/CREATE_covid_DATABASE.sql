
-- DROP DATABASE IF Exists COVID;

CREATE DATABASE COVID
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'de_CH.UTF-8'
    LC_CTYPE = 'de_CH.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
