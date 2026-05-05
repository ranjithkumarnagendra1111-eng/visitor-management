-- Data Ingestion and Transformation Queries
-- These queries demonstrate loading data from CSV/JSON sources into the database
-- Note: SQLite doesn't have direct CSV import like PostgreSQL, but we can use INSERT statements

-- Insert sample employees
INSERT OR IGNORE INTO employees (id, name, department, role) VALUES
(1, 'John Doe', 'Engineering', 'Software Engineer'),
(2, 'Jane Smith', 'HR', 'HR Manager'),
(3, 'Bob Johnson', 'Engineering', 'Senior Developer');

-- Insert sample visitors
INSERT OR IGNORE INTO visitors (id, visitorName, company, purpose, checkInTime, checkOutTime, hostEmployeeId) VALUES
(1, 'Alice Brown', 'Tech Corp', 'Meeting', '2024-01-15 09:00:00', '2024-01-15 11:00:00', 1),
(2, 'Charlie Wilson', 'Consulting Inc', 'Interview', '2024-01-16 10:00:00', '2024-01-16 12:00:00', 2),
(3, 'Diana Prince', 'Wonder Co', 'Presentation', '2024-01-17 14:00:00', NULL, 3);

-- Insert sample visits
INSERT OR IGNORE INTO visits (id, visitor_id, employee_id, check_in_time, check_out_time, purpose) VALUES
(1, 1, 1, '2024-01-15 09:00:00', '2024-01-15 11:00:00', 'Meeting'),
(2, 2, 2, '2024-01-16 10:00:00', '2024-01-16 12:00:00', 'Interview'),
(3, 3, 3, '2024-01-17 14:00:00', NULL, 'Presentation');

-- Data transformation: Update check-out times for ongoing visits
UPDATE visits
SET check_out_time = datetime('now')
WHERE check_out_time IS NULL;

-- Bulk insert from a simulated CSV (in practice, this would be done via application code)
-- For demonstration, we'll use a CTE to simulate CSV data
WITH csv_data AS (
    SELECT 4 as id, 'Eve Adams' as visitorName, 'Startup LLC' as company, 'Demo' as purpose,
           '2024-01-18 13:00:00' as checkInTime, '2024-01-18 15:00:00' as checkOutTime, 1 as hostEmployeeId
    UNION ALL
    SELECT 5, 'Frank Miller', 'Agency XYZ', 'Review', '2024-01-19 11:00:00', NULL, 2
)
INSERT OR IGNORE INTO visitors (id, visitorName, company, purpose, checkInTime, checkOutTime, hostEmployeeId)
SELECT id, visitorName, company, purpose, checkInTime, checkOutTime, hostEmployeeId FROM csv_data;