-- =========================================================
-- RecruitTrack ATS — Non-Destructive Migration
-- Migration 01: Job Skills, Performance Indexes & Stored Procedures
-- Database: recruittrack_db (PostgreSQL 14)
-- =========================================================

-- 1. CREATE JOB_SKILLS JUNCTION TABLE
CREATE TABLE IF NOT EXISTS job_skills (
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    required_level VARCHAR(30) DEFAULT 'Intermediate'
        CHECK (required_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),

    CONSTRAINT pk_job_skills
        PRIMARY KEY (job_id, skill_id),

    CONSTRAINT fk_job_skills_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_job_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE RESTRICT
);

-- 2. CREATE PERFORMANCE INDEXES
CREATE INDEX IF NOT EXISTS idx_applications_applicant
    ON applications(applicant_id);

CREATE INDEX IF NOT EXISTS idx_applications_job
    ON applications(job_id);

CREATE INDEX IF NOT EXISTS idx_applications_status
    ON applications(status);

CREATE INDEX IF NOT EXISTS idx_interviews_date
    ON interviews(interview_date);

CREATE INDEX IF NOT EXISTS idx_jobs_company
    ON jobs(company_id);

CREATE INDEX IF NOT EXISTS idx_applicant_skills_skill
    ON applicant_skills(skill_id);

CREATE INDEX IF NOT EXISTS idx_job_skills_skill
    ON job_skills(skill_id);

-- 3. STORED PROCEDURE 1: update_application_status
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
        RAISE EXCEPTION 'Invalid application status: "%". Allowed values: Applied, Screening, Interview, Offered, Rejected, Hired',
            p_new_status;
    END IF;

    UPDATE applications
    SET status = p_new_status
    WHERE application_id = p_application_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application ID % not found.', p_application_id;
    END IF;
END;
$$;

-- 4. STORED PROCEDURE 2: schedule_interview
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
        RAISE EXCEPTION 'Invalid interview type "%". Allowed values: Phone, Video, In-Person', p_interview_type;
    END IF;

    INSERT INTO interviews (application_id, interview_date, interview_type, feedback, status)
    VALUES (p_application_id, p_interview_date, p_interview_type, p_feedback, 'Scheduled');

    -- Advance application status to Interview if currently Applied or Screening
    IF v_current_status IN ('Applied', 'Screening') THEN
        UPDATE applications
        SET status = 'Interview'
        WHERE application_id = p_application_id;
    END IF;
END;
$$;

-- 5. REFRESH / UPDATE REPORTING VIEWS MATCHING EXISTING SIGNATURES
CREATE OR REPLACE VIEW applicant_application_view AS
SELECT
    ap.application_id,
    a.full_name AS applicant_name,
    a.email,
    j.job_title,
    c.company_name,
    ap.applied_date,
    ap.status AS application_status
FROM applications ap
JOIN applicants a ON ap.applicant_id = a.applicant_id
JOIN jobs j ON ap.job_id = j.job_id
JOIN companies c ON j.company_id = c.company_id;

CREATE OR REPLACE VIEW recruitment_summary_view AS
SELECT
    c.company_name,
    COUNT(DISTINCT j.job_id) AS total_jobs,
    COUNT(ap.application_id) AS total_applications
FROM companies c
LEFT JOIN jobs j ON c.company_id = j.company_id
LEFT JOIN applications ap ON j.job_id = ap.job_id
GROUP BY c.company_id, c.company_name;

-- 6. SEED INITIAL JOB_SKILLS (SAFE IDEMPOTENT INSERT)
INSERT INTO job_skills (job_id, skill_id, required_level)
SELECT j.job_id, s.skill_id, v.required_level
FROM (VALUES
    ('Software Engineer', 'Python', 'Advanced'),
    ('Software Engineer', 'SQL', 'Intermediate'),
    ('Software Engineer', 'FastAPI', 'Intermediate'),

    ('Cloud Engineer', 'AWS', 'Advanced'),
    ('Cloud Engineer', 'Docker', 'Advanced'),

    ('Data Engineer', 'SQL', 'Advanced'),
    ('Data Engineer', 'Python', 'Intermediate'),
    ('Data Engineer', 'PostgreSQL', 'Advanced'),

    ('AI Engineer', 'Python', 'Advanced'),
    ('AI Engineer', 'Machine Learning', 'Advanced'),
    ('AI Engineer', 'LangChain', 'Intermediate'),

    ('Machine Learning Engineer', 'Machine Learning', 'Advanced'),
    ('Machine Learning Engineer', 'Python', 'Advanced'),
    ('Machine Learning Engineer', 'Docker', 'Intermediate')
) AS v(job_title, skill_name, required_level)
JOIN jobs j ON j.job_title = v.job_title
JOIN skills s ON s.skill_name = v.skill_name
WHERE NOT EXISTS (
    SELECT 1 FROM job_skills js
    WHERE js.job_id = j.job_id AND js.skill_id = s.skill_id
);
