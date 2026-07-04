CREATE DATABASE system_monitor;

USE system_monitor;

CREATE TABLE system_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    disk_percent FLOAT,
    bytes_sent BIGINT,
    bytes_received BIGINT
);