-- =========================================================
-- RecruitTrack ATS — Job Recruitment & Applicant Tracking System
-- CIS 407 — Database Management Systems
-- File: database/schema.sql
-- Database: recruittrack_db (PostgreSQL 14)
-- =========================================================

-- =========================================================
-- SECTION 1: CORE 10-TABLE RELATIONAL SCHEMA
-- =========================================================

-- TABLE 1: COMPANIES
-- Represents employer organizations posting job openings.
CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) UNIQUE NOT NULL,
    industry VARCHAR(100) NOT NULL,
    location VARCHAR(150),
    website VARCHAR(255)
);

-- TABLE 2: RECRUITERS
-- Represents company recruiting staff managing job postings.
-- Includes unique composite (recruiter_id, company_id) to enforce company consistency on jobs.
CREATE TABLE IF NOT EXISTS recruiters (
    recruiter_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,

    CONSTRAINT fk_recruiter_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_recruiter_company
        UNIQUE (recruiter_id, company_id)
);

-- TABLE 3: APPLICANTS
-- Represents job seekers registered in the system.
CREATE TABLE IF NOT EXISTS applicants (
    applicant_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    location VARCHAR(150)
);

-- TABLE 4: JOBS
-- Represents job requisitions posted by recruiters for their companies.
-- Uses composite foreign key to guarantee recruiter belongs to the job's company.
CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    company_id INT NOT NULL,
    recruiter_id INT NOT NULL,
    job_title VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(150),
    salary DECIMAL(12,2) CHECK (salary >= 0),
    posted_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Open'
        CHECK (status IN ('Open', 'Closed')),

    CONSTRAINT fk_job_company
        FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_job_recruiter
        FOREIGN KEY (recruiter_id)
        REFERENCES recruiters(recruiter_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_job_recruiter_company
        FOREIGN KEY (recruiter_id, company_id)
        REFERENCES recruiters(recruiter_id, company_id)
        ON DELETE RESTRICT
);

-- TABLE 5: SKILLS
-- Master catalog of candidate and job technical proficiencies.
CREATE TABLE IF NOT EXISTS skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL
);

-- TABLE 6: APPLICANT_SKILLS (Many-to-Many junction table)
-- Associates applicants with multiple skills and proficiency levels.
CREATE TABLE IF NOT EXISTS applicant_skills (
    applicant_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level VARCHAR(30)
        CHECK (proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),

    CONSTRAINT pk_applicant_skills
        PRIMARY KEY (applicant_id, skill_id),

    CONSTRAINT fk_applicant_skills_applicant
        FOREIGN KEY (applicant_id)
        REFERENCES applicants(applicant_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_applicant_skills_skill
        FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
        ON DELETE RESTRICT
);

-- TABLE 7: RESUMES
-- Resumes uploaded by applicants.
-- Unique composite (resume_id, applicant_id) guarantees resume ownership on applications.
CREATE TABLE IF NOT EXISTS resumes (
    resume_id SERIAL PRIMARY KEY,
    applicant_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_date DATE DEFAULT CURRENT_DATE,

    CONSTRAINT fk_resume_applicant
        FOREIGN KEY (applicant_id)
        REFERENCES applicants(applicant_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_resume_applicant
        UNIQUE (resume_id, applicant_id)
);

-- TABLE 8: APPLICATIONS
-- Connects applicants, jobs, and resumes.
-- Composite foreign key guarantees selected resume belongs to the applicant.
CREATE TABLE IF NOT EXISTS applications (
    application_id SERIAL PRIMARY KEY,
    applicant_id INT NOT NULL,
    job_id INT NOT NULL,
    resume_id INT NOT NULL,
    applied_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(30) DEFAULT 'Applied'
        CHECK (status IN (
            'Applied',
            'Screening',
            'Interview',
            'Offered',
            'Rejected',
            'Hired'
        )),

    CONSTRAINT fk_application_applicant
        FOREIGN KEY (applicant_id)
        REFERENCES applicants(applicant_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_application_job
        FOREIGN KEY (job_id)
        REFERENCES jobs(job_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_application_resume
        FOREIGN KEY (resume_id)
        REFERENCES resumes(resume_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_application_resume_applicant
        FOREIGN KEY (resume_id, applicant_id)
        REFERENCES resumes(resume_id, applicant_id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_applicant_job
        UNIQUE (applicant_id, job_id)
);

-- TABLE 9: INTERVIEWS
-- Tracks interview rounds for applications.
CREATE TABLE IF NOT EXISTS interviews (
    interview_id SERIAL PRIMARY KEY,
    application_id INT NOT NULL,
    interview_date TIMESTAMP NOT NULL,
    interview_type VARCHAR(30)
        CHECK (interview_type IN ('Phone', 'Video', 'In-Person')),
    feedback TEXT,
    status VARCHAR(30) DEFAULT 'Scheduled'
        CHECK (status IN ('Scheduled', 'Completed', 'Cancelled')),

    CONSTRAINT fk_interview_application
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);

-- TABLE 10: HIRING DECISIONS
-- Final recruitment outcome for an application. One decision per application.
CREATE TABLE IF NOT EXISTS hiring_decisions (
    decision_id SERIAL PRIMARY KEY,
    application_id INT NOT NULL UNIQUE,
    decision VARCHAR(30) NOT NULL
        CHECK (decision IN ('Hired', 'Rejected', 'Pending')),
    decision_date DATE DEFAULT CURRENT_DATE,
    remarks TEXT,

    CONSTRAINT fk_decision_application
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);


-- =========================================================
-- SECTION 2: OPTIONAL SCHEMA EXTENSION (JOB_SKILLS)
-- Proposes a normalized M:N junction table between jobs and skills
-- for transparent, SQL-based applicant ranking and matching.
-- =========================================================
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


-- =========================================================
-- SECTION 3: PERFORMANCE INDEXES
-- Accelerate common ATS search, filtering, and foreign key queries.
-- Note: 'CREATE INDEX IF NOT EXISTS' is standard PostgreSQL 9.5+ syntax.
-- =========================================================
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


-- =========================================================
-- SECTION 4: VIEWS
-- Pre-aggregated and denormalized views for reporting & dashboards.
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


-- =========================================================
-- SECTION 5: STORED PROCEDURES
-- Transaction-safe PL/pgSQL business logic routines.
-- =========================================================

-- PROCEDURE 1: Update application status with input validation
CREATE OR REPLACE PROCEDURE update_application_status(
    p_application_id INT,
    p_new_status VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validate status value
    IF p_new_status IS NULL OR p_new_status NOT IN (
        'Applied', 'Screening', 'Interview', 'Offered', 'Rejected', 'Hired'
    ) THEN
        RAISE EXCEPTION 'Invalid application status: "%". Allowed: Applied, Screening, Interview, Offered, Rejected, Hired',
            p_new_status;
    END IF;

    -- Update status
    UPDATE applications
    SET status = p_new_status
    WHERE application_id = p_application_id;

    -- Verify row existence
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application ID % not found in database.', p_application_id;
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
    -- Check application existence and get status
    SELECT status INTO v_current_status
    FROM applications
    WHERE application_id = p_application_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Application ID % not found.', p_application_id;
    END IF;

    -- Validate interview type
    IF p_interview_type NOT IN ('Phone', 'Video', 'In-Person') THEN
        RAISE EXCEPTION 'Invalid interview type "%". Allowed: Phone, Video, In-Person', p_interview_type;
    END IF;

    -- Insert interview record
    INSERT INTO interviews (application_id, interview_date, interview_type, feedback, status)
    VALUES (p_application_id, p_interview_date, p_interview_type, p_feedback, 'Scheduled');

    -- Automatically transition status to 'Interview' if currently 'Applied' or 'Screening'
    IF v_current_status IN ('Applied', 'Screening') THEN
        UPDATE applications
        SET status = 'Interview'
        WHERE application_id = p_application_id;
    END IF;
END;
$$;
