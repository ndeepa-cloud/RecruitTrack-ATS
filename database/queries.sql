-- =========================================================
-- RECRUITTRACK ATS — Job Recruitment & Applicant Tracking System
-- CIS 407 — Database Management Systems
-- File: database/queries.sql
-- Database: recruittrack_db (PostgreSQL 14)
-- =========================================================


-- =========================================================
-- SECTION 1: BASIC SELECT, WHERE, AND ORDER BY
-- =========================================================

-- QUERY 1: Display all registered applicants ordered by ID
SELECT
    applicant_id,
    full_name,
    email,
    phone,
    location
FROM applicants
ORDER BY applicant_id ASC;


-- QUERY 2: Display open jobs with salary filtering and date sorting
SELECT
    job_id,
    job_title,
    location,
    salary,
    posted_date,
    status
FROM jobs
WHERE status = 'Open' AND salary >= 115000.00
ORDER BY salary DESC, posted_date ASC;


-- =========================================================
-- SECTION 2: SQL JOINS (INNER, LEFT, MULTI-TABLE)
-- =========================================================

-- QUERY 3: Jobs with company and recruiter details (Two-table INNER JOIN)
SELECT
    j.job_id,
    j.job_title,
    c.company_name,
    r.full_name AS recruiter_name,
    j.location,
    j.salary,
    j.status
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
INNER JOIN recruiters r ON j.recruiter_id = r.recruiter_id
ORDER BY c.company_name, j.job_title;


-- QUERY 4: Comprehensive application records (Four-table INNER JOIN)
SELECT
    ap.application_id,
    a.full_name AS applicant_name,
    a.email AS applicant_email,
    j.job_title,
    c.company_name,
    res.file_name AS resume_submitted,
    ap.applied_date,
    ap.status AS application_status
FROM applications ap
INNER JOIN applicants a ON ap.applicant_id = a.applicant_id
INNER JOIN jobs j ON ap.job_id = j.job_id
INNER JOIN companies c ON j.company_id = c.company_id
INNER JOIN resumes res ON ap.resume_id = res.resume_id
ORDER BY ap.applied_date DESC;


-- QUERY 5: All jobs and their application counts (LEFT JOIN to include jobs with 0 applications)
SELECT
    j.job_id,
    j.job_title,
    c.company_name,
    COUNT(ap.application_id) AS total_applications
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
LEFT JOIN applications ap ON j.job_id = ap.job_id
GROUP BY j.job_id, j.job_title, c.company_name
ORDER BY total_applications DESC, j.job_title;


-- QUERY 6: Applicant skills and proficiency matrix (Many-to-Many JOIN)
SELECT
    a.applicant_id,
    a.full_name AS applicant_name,
    s.skill_name,
    aps.proficiency_level
FROM applicants a
INNER JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
INNER JOIN skills s ON aps.skill_id = s.skill_id
ORDER BY a.full_name, aps.proficiency_level, s.skill_name;


-- =========================================================
-- SECTION 3: AGGREGATE FUNCTIONS & GROUP BY / HAVING
-- =========================================================

-- QUERY 7: Application counts grouped by status (COUNT and GROUP BY)
SELECT
    status,
    COUNT(*) AS total_applications,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM applications), 2) AS percentage
FROM applications
GROUP BY status
ORDER BY total_applications DESC;


-- QUERY 8: Salary distribution statistics across all job postings (AVG, MIN, MAX, COUNT)
SELECT
    COUNT(*) AS total_posted_jobs,
    MIN(salary) AS minimum_salary,
    MAX(salary) AS maximum_salary,
    ROUND(AVG(salary), 2) AS average_salary
FROM jobs
WHERE salary IS NOT NULL;


-- QUERY 9: High-volume jobs with more than 1 application (GROUP BY and HAVING)
SELECT
    j.job_id,
    j.job_title,
    c.company_name,
    COUNT(ap.application_id) AS total_applications
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
INNER JOIN applications ap ON j.job_id = ap.job_id
GROUP BY j.job_id, j.job_title, c.company_name
HAVING COUNT(ap.application_id) > 1
ORDER BY total_applications DESC;


-- =========================================================
-- SECTION 4: SUBQUERIES (IN, NOT EXISTS, SCALAR)
-- =========================================================

-- QUERY 10: Find applicants with Python proficiency (IN Subquery)
SELECT
    applicant_id,
    full_name,
    email,
    location
FROM applicants
WHERE applicant_id IN (
    SELECT aps.applicant_id
    FROM applicant_skills aps
    INNER JOIN skills s ON aps.skill_id = s.skill_id
    WHERE s.skill_name = 'Python'
)
ORDER BY full_name;


-- QUERY 11: Find jobs offering above-average salary (Scalar Subquery)
SELECT
    job_id,
    job_title,
    location,
    salary
FROM jobs
WHERE salary > (
    SELECT AVG(salary)
    FROM jobs
)
ORDER BY salary DESC;


-- QUERY 12: Identify applicants who have not yet submitted any application (NOT EXISTS Subquery)
SELECT
    a.applicant_id,
    a.full_name,
    a.email,
    a.location
FROM applicants a
WHERE NOT EXISTS (
    SELECT 1
    FROM applications ap
    WHERE ap.applicant_id = a.applicant_id
);


-- =========================================================
-- SECTION 5: COMPLEX RECRUITMENT REPORTS
-- =========================================================

-- QUERY 13: Detailed Interview Pipeline Schedule
SELECT
    i.interview_id,
    a.full_name AS applicant_name,
    a.email AS applicant_email,
    j.job_title,
    c.company_name,
    i.interview_date,
    i.interview_type,
    i.status AS interview_status,
    i.feedback
FROM interviews i
INNER JOIN applications ap ON i.application_id = ap.application_id
INNER JOIN applicants a ON ap.applicant_id = a.applicant_id
INNER JOIN jobs j ON ap.job_id = j.job_id
INNER JOIN companies c ON j.company_id = c.company_id
ORDER BY i.interview_date ASC;


-- QUERY 14: Final Hiring Decisions & Time-to-Hire Insights
SELECT
    hd.decision_id,
    a.full_name AS candidate_name,
    j.job_title,
    c.company_name,
    ap.applied_date,
    hd.decision_date,
    (hd.decision_date - ap.applied_date) AS days_in_pipeline,
    hd.decision,
    hd.remarks
FROM hiring_decisions hd
INNER JOIN applications ap ON hd.application_id = ap.application_id
INNER JOIN applicants a ON ap.applicant_id = a.applicant_id
INNER JOIN jobs j ON ap.job_id = j.job_id
INNER JOIN companies c ON j.company_id = c.company_id
ORDER BY hd.decision_date DESC;


-- QUERY 15: Single-Row Executive ATS Metrics Dashboard
SELECT
    (SELECT COUNT(*) FROM companies) AS total_companies,
    (SELECT COUNT(*) FROM recruiters) AS total_recruiters,
    (SELECT COUNT(*) FROM applicants) AS total_applicants,
    (SELECT COUNT(*) FROM jobs) AS total_jobs,
    (SELECT COUNT(*) FROM applications) AS total_applications,
    (SELECT COUNT(*) FROM interviews) AS total_interviews,
    (SELECT COUNT(*) FROM hiring_decisions WHERE decision = 'Hired') AS total_hired;


-- QUERY 16: Applicant-to-Job Skill Matching & Candidate Ranking
-- Ranks candidates for each job based on matching skills
SELECT
    j.job_id,
    j.job_title,
    c.company_name,
    a.applicant_id,
    a.full_name AS candidate_name,
    COUNT(js.skill_id) AS matching_skills_count,
    ROUND(100.0 * COUNT(js.skill_id) / NULLIF((SELECT COUNT(*) FROM job_skills WHERE job_id = j.job_id), 0), 1) AS match_percentage
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
INNER JOIN job_skills js ON j.job_id = js.job_id
INNER JOIN applicant_skills aps ON js.skill_id = aps.skill_id
INNER JOIN applicants a ON aps.applicant_id = a.applicant_id
GROUP BY j.job_id, j.job_title, c.company_name, a.applicant_id, a.full_name
ORDER BY j.job_id, matching_skills_count DESC, candidate_name;


-- =========================================================
-- SECTION 6: SAFE DML DEMONSTRATION (INSERT, UPDATE, DELETE)
-- Uses explicit transaction blocks with ROLLBACK to protect data.
-- =========================================================

-- DEMO 1: Transaction-safe INSERT demonstration
BEGIN;
    INSERT INTO applicants (full_name, email, phone, location)
    VALUES ('Demo Candidate', 'demo.candidate@test.edu', '555-0199', 'Demo City');

    -- Verify insertion within the transaction
    SELECT * FROM applicants WHERE email = 'demo.candidate@test.edu';
ROLLBACK;


-- DEMO 2: Transaction-safe UPDATE demonstration
BEGIN;
    UPDATE jobs
    SET salary = salary * 1.05
    WHERE status = 'Open';

    -- Verify updated salaries within the transaction
    SELECT job_id, job_title, salary FROM jobs WHERE status = 'Open';
ROLLBACK;


-- DEMO 3: Transaction-safe DELETE demonstration
BEGIN;
    -- Safely test deleting an interview note
    DELETE FROM interviews
    WHERE interview_type = 'Phone';

    -- Verify row count decreased within transaction
    SELECT COUNT(*) AS remaining_interviews FROM interviews;
ROLLBACK;


-- =========================================================
-- SECTION 7: DATABASE VIEWS & VERIFICATION
-- =========================================================

-- VIEW 1: Applicant application details with job and company names
CREATE OR REPLACE VIEW applicant_application_view AS
SELECT
    ap.application_id,
    a.applicant_id,
    a.full_name AS applicant_name,
    a.email AS applicant_email,
    j.job_id,
    j.job_title,
    c.company_id,
    c.company_name,
    ap.applied_date,
    ap.status AS application_status,
    r.resume_id,
    r.file_name AS resume_file
FROM applications ap
JOIN applicants a ON ap.applicant_id = a.applicant_id
JOIN jobs j ON ap.job_id = j.job_id
JOIN companies c ON j.company_id = c.company_id
JOIN resumes r ON ap.resume_id = r.resume_id;

-- VIEW 2: Recruitment summary by company
CREATE OR REPLACE VIEW recruitment_summary_view AS
SELECT
    c.company_id,
    c.company_name,
    c.industry,
    COUNT(DISTINCT j.job_id) AS total_jobs,
    COUNT(DISTINCT ap.application_id) AS total_applications,
    COUNT(DISTINCT CASE WHEN ap.status = 'Hired' THEN ap.application_id END) AS total_hired
FROM companies c
LEFT JOIN jobs j ON c.company_id = j.company_id
LEFT JOIN applications ap ON j.job_id = ap.job_id
GROUP BY c.company_id, c.company_name, c.industry;

-- Verification queries for views:
SELECT * FROM applicant_application_view ORDER BY application_id LIMIT 5;
SELECT * FROM recruitment_summary_view ORDER BY company_name;


-- =========================================================
-- SECTION 8: PERFORMANCE INDEXES
-- Valid PostgreSQL 9.5+ syntax.
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_applications_applicant
    ON applications(applicant_id);

CREATE INDEX IF NOT EXISTS idx_applications_job
    ON applications(job_id);

CREATE INDEX IF NOT EXISTS idx_applications_status
    ON applications(status);

CREATE INDEX IF NOT EXISTS idx_interviews_date
    ON interviews(interview_date);


-- =========================================================
-- SECTION 9: STORED PROCEDURES & PL/PGSQL LOGIC
-- =========================================================

-- PROCEDURE 1: Update application status with domain validation
CREATE OR REPLACE PROCEDURE update_application_status(
    p_application_id INT,
    p_new_status VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_new_status IS NULL OR p_new_status NOT IN (
        'Applied', 'Screening', 'Interview', 'Offered', 'Rejected', 'Hired'
    ) THEN
        RAISE EXCEPTION 'Invalid application status: "%". Allowed: Applied, Screening, Interview, Offered, Rejected, Hired',
            p_new_status;
    END IF;

    UPDATE applications
    SET status = p_new_status
    WHERE application_id = p_application_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application ID % not found', p_application_id;
    END IF;
END;
$$;


-- PROCEDURE 2: Schedule interview with state synchronization
CREATE OR REPLACE PROCEDURE schedule_interview(
    p_application_id INT,
    p_interview_date TIMESTAMP,
    p_interview_type VARCHAR,
    p_feedback TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_current_status VARCHAR(30);
BEGIN
    SELECT status INTO v_current_status
    FROM applications
    WHERE application_id = p_application_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application ID % not found.', p_application_id;
    END IF;

    IF p_interview_type NOT IN ('Phone', 'Video', 'In-Person') THEN
        RAISE EXCEPTION 'Invalid interview type "%". Allowed: Phone, Video, In-Person', p_interview_type;
    END IF;

    INSERT INTO interviews (application_id, interview_date, interview_type, feedback, status)
    VALUES (p_application_id, p_interview_date, p_interview_type, p_feedback, 'Scheduled');

    IF v_current_status IN ('Applied', 'Screening') THEN
        UPDATE applications
        SET status = 'Interview'
        WHERE application_id = p_application_id;
    END IF;
END;
$$;


-- =========================================================
-- SECTION 10: STORED PROCEDURE VERIFICATION IN TRANSACTION
-- Demonstrates invocation of stored procedures safely with rollback.
-- =========================================================
BEGIN;
    -- Test status update
    CALL update_application_status(1, 'Screening');
    SELECT application_id, status FROM applications WHERE application_id = 1;

    -- Test interview scheduling procedure
    CALL schedule_interview(2, '2026-11-25 15:00:00'::TIMESTAMP, 'Video', 'Automated test interview');
    SELECT * FROM interviews WHERE application_id = 2 ORDER BY interview_id DESC LIMIT 1;
ROLLBACK;

-- =========================================================
-- END OF QUERIES.SQL
-- =========================================================
