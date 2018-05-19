DROP DATABASE IF EXISTS phl_neargreen;
DROP DATABASE IF EXISTS phl_neargreen_test;
DROP ROLE IF EXISTS phl_neargreen_user;
CREATE USER phl_neargreen_user;
ALTER USER phl_neargreen_user SUPERUSER; -- don't love this but superuser is needed in order to add postgres extensions...
CREATE DATABASE phl_neargreen OWNER phl_neargreen_user;
