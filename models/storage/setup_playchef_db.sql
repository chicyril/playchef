-- prepares a MySQL server for the project

DROP DATABASE IF EXISTS playchef_db;
CREATE DATABASE IF NOT EXISTS playchef_db;
CREATE USER IF NOT EXISTS 'playchef_dev'@'localhost' IDENTIFIED BY 'Devchef1_';
GRANT ALL PRIVILEGES ON `playchef_db`.* TO 'playchef_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'playchef_dev'@'localhost';
FLUSH PRIVILEGES;
