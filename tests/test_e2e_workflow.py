"""
RecruitTrack ATS - Complete End-to-End Workflow Test
CIS 407 — Database Management Systems

Executes the complete 15-stage recruitment lifecycle:
 1. Recruiter login & credential validation
 2. Create / use employer company
 3. Create job posting
 4. Assign required skills to the job
 5. Register new applicant
 6. Assign skills to the applicant
 7. Upload / associate resume document
 8. Submit job application
 9. Calculate transparent candidate skill match
10. Update application status via stored procedure
11. Schedule an interview via stored procedure
12. Record interview feedback and evaluation
13. Record final hiring decision
14. Verify executive dashboard metrics update
15. Generate downloadable CSV recruitment report
"""

import datetime
import os
import sys
import pandas as pd
import pytest
from dotenv import load_dotenv

# Ensure apps directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps")))

from db_connection import (
    execute_procedure,
    execute_query,
    get_connection,
    test_connection as check_db_health,
    verify_password,
)

load_dotenv()


def test_complete_15_step_recruitment_workflow():
    """Executes all 15 stages of the recruitment workflow and validates database state."""
    ok, _ = check_db_health()
    if not ok:
        pytest.skip("PostgreSQL 14 on port 4919 is not accessible.")

    conn = get_connection()
    cur = conn.cursor()

    test_company_id = None
    test_job_id = None
    test_applicant_id = None
    test_resume_id = None
    test_application_id = None
    test_interview_id = None
    test_decision_id = None

    try:
        # ---------------------------------------------------------
        # STAGE 1: Log in as a recruiter
        # ---------------------------------------------------------
        cur.execute("SELECT recruiter_id, password_hash, company_id FROM recruiters WHERE email = 'sarah.johnson@example.com';")
        recruiter = cur.fetchone()
        assert recruiter is not None
        rec_id, rec_hash, rec_comp_id = recruiter[0], recruiter[1], recruiter[2]
        assert verify_password("DemoRecruiter2026!", rec_hash) is True

        # ---------------------------------------------------------
        # STAGE 2: Create a fictional company
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO companies (company_name, industry, location, website)
            VALUES ('E2E Fictional Corp', 'Cloud Computing', 'Louisville, KY', 'https://e2ecorp.test')
            RETURNING company_id;
        """)
        test_company_id = cur.fetchone()[0]
        assert test_company_id > 0

        # ---------------------------------------------------------
        # STAGE 3: Create a job posting
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO jobs (company_id, recruiter_id, job_title, description, location, salary, posted_date, status)
            VALUES (%s, %s, 'E2E Full Stack Engineer', 'Comprehensive automated test job posting', 'Remote', 130000.00, CURRENT_DATE, 'Open')
            RETURNING job_id;
        """, (test_company_id, rec_id))
        test_job_id = cur.fetchone()[0]
        assert test_job_id > 0

        # ---------------------------------------------------------
        # STAGE 4: Assign required skills to the job
        # ---------------------------------------------------------
        cur.execute("SELECT skill_id FROM skills WHERE skill_name IN ('Python', 'SQL', 'FastAPI') ORDER BY skill_id;")
        req_skills = [r[0] for r in cur.fetchall()]
        assert len(req_skills) >= 2

        for sk_id in req_skills:
            cur.execute("""
                INSERT INTO job_skills (job_id, skill_id, required_level)
                VALUES (%s, %s, 'Advanced')
                ON CONFLICT (job_id, skill_id) DO NOTHING;
            """, (test_job_id, sk_id))

        # ---------------------------------------------------------
        # STAGE 5: Register a new applicant
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO applicants (full_name, email, phone, location)
            VALUES ('E2E Candidate Jane', 'e2e.candidate.jane@test.edu', '555-0199', 'Lexington, KY')
            RETURNING applicant_id;
        """)
        test_applicant_id = cur.fetchone()[0]
        assert test_applicant_id > 0

        # ---------------------------------------------------------
        # STAGE 6: Assign skills to the applicant
        # ---------------------------------------------------------
        for sk_id in req_skills:
            cur.execute("""
                INSERT INTO applicant_skills (applicant_id, skill_id, proficiency_level)
                VALUES (%s, %s, 'Advanced')
                ON CONFLICT (applicant_id, skill_id) DO NOTHING;
            """, (test_applicant_id, sk_id))

        # ---------------------------------------------------------
        # STAGE 7: Upload / associate a resume
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO resumes (applicant_id, file_name, file_path, uploaded_date)
            VALUES (%s, 'e2e_jane_resume.pdf', 'uploads/resumes/e2e_jane_resume.pdf', CURRENT_DATE)
            RETURNING resume_id;
        """, (test_applicant_id,))
        test_resume_id = cur.fetchone()[0]
        assert test_resume_id > 0

        # ---------------------------------------------------------
        # STAGE 8: Submit an application
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO applications (applicant_id, job_id, resume_id, applied_date, status)
            VALUES (%s, %s, %s, CURRENT_DATE, 'Applied')
            RETURNING application_id;
        """, (test_applicant_id, test_job_id, test_resume_id))
        test_application_id = cur.fetchone()[0]
        assert test_application_id > 0

        # ---------------------------------------------------------
        # STAGE 9: Calculate candidate skill match
        # ---------------------------------------------------------
        cur.execute("""
            SELECT
                COUNT(js.skill_id) AS matched_count,
                ROUND(100.0 * COUNT(js.skill_id) / NULLIF((SELECT COUNT(*) FROM job_skills WHERE job_id = %s), 0), 1) AS match_pct
            FROM job_skills js
            JOIN applicant_skills aps ON js.skill_id = aps.skill_id
            WHERE js.job_id = %s AND aps.applicant_id = %s;
        """, (test_job_id, test_job_id, test_applicant_id))
        match_result = cur.fetchone()
        assert match_result[0] == len(req_skills)
        assert float(match_result[1]) == 100.0

        # ---------------------------------------------------------
        # STAGE 10: Update application status via stored procedure
        # ---------------------------------------------------------
        cur.execute("CALL update_application_status(%s, %s);", (test_application_id, 'Screening'))
        cur.execute("SELECT status FROM applications WHERE application_id = %s;", (test_application_id,))
        assert cur.fetchone()[0] == 'Screening'

        # ---------------------------------------------------------
        # STAGE 11: Schedule an interview via stored procedure
        # ---------------------------------------------------------
        interview_time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=2)
        cur.execute("CALL schedule_interview(%s, %s, %s, %s);", (test_application_id, interview_time, 'Video', 'Initial round agenda'))
        cur.execute("SELECT interview_id, status FROM interviews WHERE application_id = %s;", (test_application_id,))
        int_row = cur.fetchone()
        assert int_row is not None
        test_interview_id = int_row[0]

        # Stored procedure automatically syncs application status to 'Interview'
        cur.execute("SELECT status FROM applications WHERE application_id = %s;", (test_application_id,))
        assert cur.fetchone()[0] == 'Interview'

        # ---------------------------------------------------------
        # STAGE 12: Record interview feedback
        # ---------------------------------------------------------
        cur.execute("""
            UPDATE interviews
            SET status = 'Completed', feedback = 'Outstanding system architecture and database performance.'
            WHERE interview_id = %s;
        """, (test_interview_id,))
        cur.execute("SELECT feedback FROM interviews WHERE interview_id = %s;", (test_interview_id,))
        assert "Outstanding" in cur.fetchone()[0]

        # ---------------------------------------------------------
        # STAGE 13: Record a hiring decision
        # ---------------------------------------------------------
        cur.execute("""
            INSERT INTO hiring_decisions (application_id, decision, decision_date, remarks)
            VALUES (%s, 'Hired', CURRENT_DATE, 'Candidate accepted offer with start date in 2 weeks.')
            RETURNING decision_id;
        """, (test_application_id,))
        test_decision_id = cur.fetchone()[0]
        assert test_decision_id > 0

        # Synchronize application status
        cur.execute("CALL update_application_status(%s, 'Hired');", (test_application_id,))
        cur.execute("SELECT status FROM applications WHERE application_id = %s;", (test_application_id,))
        assert cur.fetchone()[0] == 'Hired'

        # ---------------------------------------------------------
        # STAGE 14: Verify dashboard changes
        # ---------------------------------------------------------
        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM companies) AS total_companies,
                (SELECT COUNT(*) FROM jobs) AS total_jobs,
                (SELECT COUNT(*) FROM applications) AS total_applications,
                (SELECT COUNT(*) FROM hiring_decisions WHERE decision = 'Hired') AS total_hired;
        """)
        dash = cur.fetchone()
        assert dash[0] >= 6  # 5 sample + 1 new test company
        assert dash[1] >= 6  # 5 sample + 1 new test job
        assert dash[2] >= 11 # 10 sample + 1 new application
        assert dash[3] >= 2  # 1 sample + 1 new hired candidate

        # ---------------------------------------------------------
        # STAGE 15: Generate and download a recruitment report
        # ---------------------------------------------------------
        cur.execute("SELECT * FROM applicant_application_view WHERE application_id = %s;", (test_application_id,))
        view_row = cur.fetchone()
        assert view_row is not None
        assert view_row[1] == 'E2E Candidate Jane'
        assert view_row[3] == 'E2E Full Stack Engineer'

        # Verify CSV export generation
        cols = [d[0] for d in cur.description]
        df = pd.DataFrame([view_row], columns=cols)
        csv_str = df.to_csv(index=False)
        assert "E2E Candidate Jane" in csv_str

    finally:
        # Safe cleanup of only the temporary test records created during this run
        conn.rollback()  # Rollback any uncommitted transaction first
        with conn.cursor() as clean_cur:
            if test_decision_id:
                clean_cur.execute("DELETE FROM hiring_decisions WHERE decision_id = %s;", (test_decision_id,))
            if test_interview_id:
                clean_cur.execute("DELETE FROM interviews WHERE interview_id = %s;", (test_interview_id,))
            if test_application_id:
                clean_cur.execute("DELETE FROM applications WHERE application_id = %s;", (test_application_id,))
            if test_resume_id:
                clean_cur.execute("DELETE FROM resumes WHERE resume_id = %s;", (test_resume_id,))
            if test_applicant_id:
                clean_cur.execute("DELETE FROM applicant_skills WHERE applicant_id = %s;", (test_applicant_id,))
                clean_cur.execute("DELETE FROM applicants WHERE applicant_id = %s;", (test_applicant_id,))
            if test_job_id:
                clean_cur.execute("DELETE FROM job_skills WHERE job_id = %s;", (test_job_id,))
                clean_cur.execute("DELETE FROM jobs WHERE job_id = %s;", (test_job_id,))
            if test_company_id:
                clean_cur.execute("DELETE FROM companies WHERE company_id = %s;", (test_company_id,))
            conn.commit()

        conn.close()
