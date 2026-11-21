-- ============================================
-- RecruitTrack ATS - Sample Data
-- CIS 407 Database Project
-- PostgreSQL 14
--
-- Designed to be executed with:
-- psql -h localhost -p 4919 -U postgres -d recruittrack_db -v ON_ERROR_STOP=1 -1 -f database/sample_data.sql
--
-- Note: Transaction handling (BEGIN/COMMIT) is managed by psql's -1 flag
-- to avoid nested transaction warnings.
-- All INSERT statements use idempotent WHERE NOT EXISTS filters, ensuring
-- safe reruns without creating duplicates or relying on missing UNIQUE constraints.
-- ============================================

-- 1. COMPANIES
INSERT INTO companies (company_name, industry, location, website)
SELECT v.company_name, v.industry, v.location, v.website
FROM (VALUES
    ('Google', 'Technology', 'Mountain View, CA', 'https://google.com'),
    ('Microsoft', 'Technology', 'Redmond, WA', 'https://microsoft.com'),
    ('Amazon', 'E-Commerce', 'Seattle, WA', 'https://amazon.com'),
    ('OpenAI', 'Artificial Intelligence', 'San Francisco, CA', 'https://openai.com'),
    ('NVIDIA', 'Semiconductors', 'Santa Clara, CA', 'https://nvidia.com')
) AS v(company_name, industry, location, website)
WHERE NOT EXISTS (
    SELECT 1 FROM companies c WHERE c.company_name = v.company_name
);


-- 2. RECRUITERS
-- Seeded with valid bcrypt hash ($2b$12$...) for demo password: DemoRecruiter2026!
INSERT INTO recruiters (company_id, full_name, email, password_hash)
SELECT c.company_id, v.full_name, v.email, v.password_hash
FROM (VALUES
    ('Google', 'Sarah Johnson', 'sarah.johnson@example.com', '$2b$12$nMg9pXg7.wG/4io6C8bjje4mmWdJUsSTB7UE593oGkmuEOT3lqide'),
    ('Microsoft', 'Michael Brown', 'michael.brown@example.com', '$2b$12$nMg9pXg7.wG/4io6C8bjje4mmWdJUsSTB7UE593oGkmuEOT3lqide'),
    ('Amazon', 'Emily Davis', 'emily.davis@example.com', '$2b$12$nMg9pXg7.wG/4io6C8bjje4mmWdJUsSTB7UE593oGkmuEOT3lqide'),
    ('OpenAI', 'David Wilson', 'david.wilson@example.com', '$2b$12$nMg9pXg7.wG/4io6C8bjje4mmWdJUsSTB7UE593oGkmuEOT3lqide'),
    ('NVIDIA', 'Jessica Miller', 'jessica.miller@example.com', '$2b$12$nMg9pXg7.wG/4io6C8bjje4mmWdJUsSTB7UE593oGkmuEOT3lqide')
) AS v(company_name, full_name, email, password_hash)
JOIN companies c ON c.company_name = v.company_name
WHERE NOT EXISTS (
    SELECT 1 FROM recruiters r WHERE r.email = v.email
);


-- 3. APPLICANTS
INSERT INTO applicants (full_name, email, phone, location)
SELECT v.full_name, v.email, v.phone, v.location
FROM (VALUES
    ('Alex Carter', 'alex.carter@example.com', '2705550101', 'Kentucky'),
    ('Priya Sharma', 'priya.sharma@example.com', '2705550102', 'Texas'),
    ('John Smith', 'john.smith@example.com', '2705550103', 'California'),
    ('Emily Chen', 'emily.chen@example.com', '2705550104', 'New York'),
    ('Rahul Patel', 'rahul.patel@example.com', '2705550105', 'Florida'),
    ('Sophia Wilson', 'sophia.wilson@example.com', '2705550106', 'Washington'),
    ('Daniel Kim', 'daniel.kim@example.com', '2705550107', 'Illinois'),
    ('Olivia Brown', 'olivia.brown@example.com', '2705550108', 'Georgia'),
    ('James Anderson', 'james.anderson@example.com', '2705550109', 'Ohio'),
    ('Aisha Khan', 'aisha.khan@example.com', '2705550110', 'Arizona')
) AS v(full_name, email, phone, location)
WHERE NOT EXISTS (
    SELECT 1 FROM applicants a WHERE a.email = v.email
);


-- 4. JOBS
INSERT INTO jobs (company_id, recruiter_id, job_title, description, location, salary, posted_date, status)
SELECT
    c.company_id,
    r.recruiter_id,
    v.job_title,
    v.description,
    v.location,
    v.salary::NUMERIC,
    v.posted_date::DATE,
    v.status
FROM (VALUES
    ('Google', 'sarah.johnson@example.com', 'Software Engineer', 'Develop backend services using Python and Java.', 'Mountain View, CA', 120000, '2026-11-01', 'Open'),
    ('Microsoft', 'michael.brown@example.com', 'Cloud Engineer', 'Build and maintain cloud infrastructure.', 'Redmond, WA', 115000, '2026-11-02', 'Open'),
    ('Amazon', 'emily.davis@example.com', 'Data Engineer', 'Develop data pipelines using SQL and Python.', 'Seattle, WA', 110000, '2026-11-03', 'Open'),
    ('OpenAI', 'david.wilson@example.com', 'AI Engineer', 'Develop LLM applications and AI services.', 'San Francisco, CA', 140000, '2026-11-04', 'Open'),
    ('NVIDIA', 'jessica.miller@example.com', 'Machine Learning Engineer', 'Build and deploy machine learning models.', 'Santa Clara, CA', 135000, '2026-11-05', 'Open')
) AS v(company_name, recruiter_email, job_title, description, location, salary, posted_date, status)
JOIN companies c ON c.company_name = v.company_name
JOIN recruiters r ON r.email = v.recruiter_email
WHERE NOT EXISTS (
    SELECT 1 FROM jobs j WHERE j.company_id = c.company_id AND j.job_title = v.job_title
);


-- 5. SKILLS
INSERT INTO skills (skill_name)
SELECT v.skill_name
FROM (VALUES
    ('Python'),
    ('Java'),
    ('SQL'),
    ('React'),
    ('Machine Learning'),
    ('AWS'),
    ('Docker'),
    ('FastAPI'),
    ('PostgreSQL'),
    ('LangChain')
) AS v(skill_name)
WHERE NOT EXISTS (
    SELECT 1 FROM skills s WHERE s.skill_name = v.skill_name
);


-- 6. APPLICANT SKILLS
INSERT INTO applicant_skills (applicant_id, skill_id, proficiency_level)
SELECT a.applicant_id, s.skill_id, v.proficiency_level
FROM (VALUES
    ('alex.carter@example.com', 'Python', 'Advanced'),
    ('alex.carter@example.com', 'SQL', 'Advanced'),
    ('alex.carter@example.com', 'FastAPI', 'Intermediate'),

    ('priya.sharma@example.com', 'Python', 'Advanced'),
    ('priya.sharma@example.com', 'Machine Learning', 'Advanced'),
    ('priya.sharma@example.com', 'LangChain', 'Intermediate'),

    ('john.smith@example.com', 'Java', 'Advanced'),
    ('john.smith@example.com', 'AWS', 'Intermediate'),

    ('emily.chen@example.com', 'React', 'Advanced'),
    ('emily.chen@example.com', 'Python', 'Intermediate'),

    ('rahul.patel@example.com', 'SQL', 'Advanced'),
    ('rahul.patel@example.com', 'PostgreSQL', 'Advanced'),

    ('sophia.wilson@example.com', 'AWS', 'Advanced'),
    ('sophia.wilson@example.com', 'Docker', 'Advanced'),

    ('daniel.kim@example.com', 'Machine Learning', 'Advanced'),
    ('daniel.kim@example.com', 'Python', 'Advanced'),

    ('olivia.brown@example.com', 'React', 'Advanced'),
    ('olivia.brown@example.com', 'Java', 'Intermediate'),

    ('james.anderson@example.com', 'Docker', 'Intermediate'),
    ('james.anderson@example.com', 'FastAPI', 'Advanced'),

    ('aisha.khan@example.com', 'LangChain', 'Advanced'),
    ('aisha.khan@example.com', 'Python', 'Advanced')
) AS v(email, skill_name, proficiency_level)
JOIN applicants a ON a.email = v.email
JOIN skills s ON s.skill_name = v.skill_name
WHERE NOT EXISTS (
    SELECT 1 FROM applicant_skills aps
    WHERE aps.applicant_id = a.applicant_id AND aps.skill_id = s.skill_id
);


-- 7. RESUMES
-- File paths are fictional representations in uploads/resumes/
INSERT INTO resumes (applicant_id, file_name, file_path, uploaded_date)
SELECT
    a.applicant_id,
    split_part(a.email, '@', 1) || '_resume.pdf',
    'uploads/resumes/' || split_part(a.email, '@', 1) || '_resume.pdf',
    '2026-11-06'::DATE
FROM applicants a
WHERE NOT EXISTS (
    SELECT 1 FROM resumes r WHERE r.applicant_id = a.applicant_id
);


-- 8. APPLICATIONS
INSERT INTO applications (applicant_id, job_id, resume_id, applied_date, status)
SELECT
    a.applicant_id,
    j.job_id,
    r.resume_id,
    v.applied_date::DATE,
    v.status
FROM (VALUES
    ('alex.carter@example.com', 'Software Engineer', '2026-11-07', 'Interview'),
    ('priya.sharma@example.com', 'AI Engineer', '2026-11-07', 'Screening'),
    ('john.smith@example.com', 'Cloud Engineer', '2026-11-08', 'Applied'),
    ('emily.chen@example.com', 'Software Engineer', '2026-11-08', 'Rejected'),
    ('rahul.patel@example.com', 'Data Engineer', '2026-11-09', 'Interview'),
    ('sophia.wilson@example.com', 'Cloud Engineer', '2026-11-09', 'Offered'),
    ('daniel.kim@example.com', 'Machine Learning Engineer', '2026-11-10', 'Hired'),
    ('olivia.brown@example.com', 'Software Engineer', '2026-11-10', 'Applied'),
    ('james.anderson@example.com', 'Data Engineer', '2026-11-11', 'Screening'),
    ('aisha.khan@example.com', 'AI Engineer', '2026-11-11', 'Interview')
) AS v(email, job_title, applied_date, status)
JOIN applicants a ON a.email = v.email
JOIN resumes r ON r.applicant_id = a.applicant_id
JOIN jobs j ON j.job_title = v.job_title
WHERE NOT EXISTS (
    SELECT 1 FROM applications ap WHERE ap.applicant_id = a.applicant_id AND ap.job_id = j.job_id
);


-- 9. INTERVIEWS
INSERT INTO interviews (application_id, interview_date, interview_type, feedback, status)
SELECT
    ap.application_id,
    v.interview_date::TIMESTAMP,
    v.interview_type,
    v.feedback,
    v.status
FROM (VALUES
    ('alex.carter@example.com', 'Software Engineer', '2026-11-22 10:00:00', 'Video', 'Technical interview scheduled.', 'Scheduled'),
    ('rahul.patel@example.com', 'Data Engineer', '2026-11-23 11:00:00', 'Phone', 'Initial screening completed.', 'Completed'),
    ('sophia.wilson@example.com', 'Cloud Engineer', '2026-11-15 14:00:00', 'Video', 'Strong cloud infrastructure knowledge.', 'Completed'),
    ('daniel.kim@example.com', 'Machine Learning Engineer', '2026-11-16 09:00:00', 'In-Person', 'Excellent machine learning knowledge.', 'Completed'),
    ('aisha.khan@example.com', 'AI Engineer', '2026-11-24 13:00:00', 'Video', 'Technical discussion scheduled.', 'Scheduled')
) AS v(email, job_title, interview_date, interview_type, feedback, status)
JOIN applicants a ON a.email = v.email
JOIN jobs j ON j.job_title = v.job_title
JOIN applications ap ON ap.applicant_id = a.applicant_id AND ap.job_id = j.job_id
WHERE NOT EXISTS (
    SELECT 1 FROM interviews i
    WHERE i.application_id = ap.application_id AND i.interview_date = v.interview_date::TIMESTAMP
);


-- 10. HIRING DECISIONS
INSERT INTO hiring_decisions (application_id, decision, decision_date, remarks)
SELECT
    ap.application_id,
    v.decision,
    v.decision_date::DATE,
    v.remarks
FROM (VALUES
    ('emily.chen@example.com', 'Software Engineer', 'Rejected', '2026-11-18', 'Candidate not selected.'),
    ('sophia.wilson@example.com', 'Cloud Engineer', 'Pending', '2026-11-19', 'Offer awaiting candidate acceptance.'),
    ('daniel.kim@example.com', 'Machine Learning Engineer', 'Hired', '2026-11-19', 'Candidate successfully hired.')
) AS v(email, job_title, decision, decision_date, remarks)
JOIN applicants a ON a.email = v.email
JOIN jobs j ON j.job_title = v.job_title
JOIN applications ap ON ap.applicant_id = a.applicant_id AND ap.job_id = j.job_id
WHERE NOT EXISTS (
    SELECT 1 FROM hiring_decisions hd WHERE hd.application_id = ap.application_id
);
