-- SQL Queries for Joins, Aggregations, Window Functions, and Optimization

-- JOINS
-- Inner join: Get all visits with visitor and employee details
SELECT v.id as visit_id, vis.visitorName, e.name as employee_name, v.check_in_time, v.check_out_time, v.purpose
FROM visits v
INNER JOIN visitors vis ON v.visitor_id = vis.id
INNER JOIN employees e ON v.employee_id = e.id;

-- Left join: Get all employees and their visit counts (including those with no visits)
SELECT e.name, e.department, COUNT(v.id) as visit_count
FROM employees e
LEFT JOIN visits v ON e.id = v.employee_id
GROUP BY e.id, e.name, e.department;

-- AGGREGATIONS
-- Count total visits per employee
SELECT e.name, COUNT(v.id) as total_visits
FROM employees e
LEFT JOIN visits v ON e.id = v.employee_id
GROUP BY e.id, e.name
ORDER BY total_visits DESC;

-- Average visit duration per department
SELECT e.department, AVG(
    CASE
        WHEN v.check_out_time IS NOT NULL THEN
            (julianday(v.check_out_time) - julianday(v.check_in_time)) * 24 * 60
        ELSE NULL
    END
) as avg_duration_minutes
FROM employees e
LEFT JOIN visits v ON e.id = v.employee_id
WHERE v.check_out_time IS NOT NULL
GROUP BY e.department;

-- WINDOW FUNCTIONS
-- Rank employees by number of visits
SELECT name, department, visit_count,
       RANK() OVER (ORDER BY visit_count DESC) as rank_by_visits
FROM (
    SELECT e.name, e.department, COUNT(v.id) as visit_count
    FROM employees e
    LEFT JOIN visits v ON e.id = v.employee_id
    GROUP BY e.id, e.name, e.department
) sub;

-- Running total of visits over time
SELECT check_in_time, visitorName, purpose,
       COUNT(*) OVER (ORDER BY check_in_time) as running_total_visits
FROM visits v
JOIN visitors vis ON v.visitor_id = vis.id
ORDER BY check_in_time;

-- QUERY OPTIMIZATION
-- Create indexes for better performance (run these separately)
-- CREATE INDEX idx_visits_employee_id ON visits(employee_id);
-- CREATE INDEX idx_visits_check_in ON visits(check_in_time);
-- CREATE INDEX idx_visitors_host ON visitors(hostEmployeeId);

-- Optimized query using indexes
SELECT e.name, COUNT(v.id) as visit_count
FROM employees e
LEFT JOIN visits v ON e.id = v.employee_id
WHERE v.check_in_time >= '2024-01-01'
GROUP BY e.id, e.name
HAVING COUNT(v.id) > 0
ORDER BY visit_count DESC;

-- Complex query with subquery optimization
SELECT *
FROM visitors
WHERE hostEmployeeId IN (
    SELECT id FROM employees WHERE department = 'Engineering'
)
AND checkInTime >= '2024-01-01';

-- CTE for better readability and potential optimization
WITH engineering_hosts AS (
    SELECT id FROM employees WHERE department = 'Engineering'
),
recent_visits AS (
    SELECT * FROM visits WHERE check_in_time >= '2024-01-01'
)
SELECT v.visitorName, e.name as host_name, rv.check_in_time
FROM visitors v
JOIN engineering_hosts eh ON v.hostEmployeeId = eh.id
LEFT JOIN recent_visits rv ON v.id = rv.visitor_id
ORDER BY rv.check_in_time DESC;