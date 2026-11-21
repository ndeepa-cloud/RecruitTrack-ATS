"""
RecruitTrack ATS - Master Comprehensive Test Suite
CIS 407 — Database Management Systems

Covers all 20 required testing scenarios:
 1. Database connection
 2. Table existence
 3. Foreign-key integrity
 4. Recruiter authentication
 5. Invalid login rejection
 6. Company CRUD
 7. Applicant CRUD
 8. Job CRUD
 9. Application creation
10. Duplicate application prevention
11. Application status updates
12. Interview scheduling
13. Hiring decisions
14. Candidate skill matching
15. SQL views
16. Stored procedures
17. Dashboard query accuracy
18. CSV report generation
19. Input validation & constraints
20. Transaction rollback behavior
"""

import datetime
import io
import os
import sys
import pandas as pd
import pytest
import psycopg2
from dotenv import load_dotenv

# Ensure apps directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps")))

from db_connection import (
    execute_procedure,
    execute_query,
    get_connection,
    get_db_config,
    hash_password,
    test_connection as check_db_connectivity,
    verify_password,
)

load_dotenv()


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture(scope="module")
def db():
    """Provides a dedicated live database connection, skipped if DB is unreachable."""
    ok, _ = check_db_connectivity()
    if not ok:
        pytest.skip("PostgreSQL 14 database on port 4919 is not currently accessible.")
    conn = get_connection()
    yield conn
    conn.close()


# =========================================================
# TEST SCENARIO 1: DATABASE CONNECTION
# =========================================================
def test_01_database_connection(db):
    """Verify PostgreSQL 14 connectivity on port 4919."""
    ok, msg = check_db_connectivity()
    assert ok is True
    assert "Successfully connected" in msg


# =========================================================
# TEST SCENARIO 2: TABLE EXISTENCE (ALL 11 TABLES)
# =========================================================
def test_02_all_tables_exist(db):
    """Verify all 10 core tables plus job_skills exist in the public schema."""
    expected_tables = {
        "companies", "recruiters", "applicants", "jobs", "skills",
        "applicant_skills", "resumes", "applications", "interviews",
        "hiring_decisions", "job_skills"
    }
    with db.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        live_tables = {r[0] for r in cur.fetchall()}
    assert expected_tables.issubset(live_tables), f"Missing tables: {expected_tables - live_tables}"


# =========================================================
# TEST SCENARIO 3: FOREIGN-KEY INTEGRITY
# =========================================================
def test_03_foreign_key_integrity(db):
    """Verify that foreign keys prevent inserting orphaned child records."""
    with db.cursor() as cur:
        db.rollback()
        # Inserting a job with a nonexistent company_id should raise IntegrityError
        with pytest.raises(psycopg2.IntegrityError):
            cur.execute("""
                INSERT INTO jobs (company_id, recruiter_id, job_title, salary, status)
                VALUES (999999, 1, 'Orphaned Job', 100000.00, 'Open');
            """)
        db.rollback()


# =========================================================
# TEST SCENARIO 4: RECRUITER AUTHENTICATION (VALID)
# =========================================================
def test_04_recruiter_authentication_valid(db):
    """Verify valid recruiter credentials against bcrypt hash in database."""
    with db.cursor() as cur:
        cur.execute("SELECT password_hash FROM recruiters WHERE email = 'sarah.johnson@example.com';")
        row = cur.fetchone()
        assert row is not None, "Demo recruiter not found"
        stored_hash = row[0]
        assert verify_password("DemoRecruiter2026!", stored_hash) is True


# =========================================================
# TEST SCENARIO 5: RECRUITER AUTHENTICATION (INVALID)
# =========================================================
def test_05_recruiter_authentication_invalid(db):
    """Verify incorrect passwords and empty passwords fail authentication."""
    with db.cursor() as cur:
        cur.execute("SELECT password_hash FROM recruiters WHERE email = 'sarah.johnson@example.com';")
        stored_hash = cur.fetchone()[0]
        assert verify_password("WrongPassword123!", stored_hash) is False
        assert verify_password("", stored_hash) is False
        # Verify placeholder hashes are strictly rejected
        assert verify_password("DEMO_HASH_001", "DEMO_HASH_001") is False


# =========================================================
# TEST SCENARIO 6: COMPANY CRUD WITH ROLLBACK
# =========================================================
def test_06_company_crud(db):
    """Test Create, Read, Update, and Delete operations on companies."""
    with db.cursor() as cur:
        db.rollback()
        # Create
        cur.execute("""
            INSERT INTO companies (company_name, industry, location, website)
            VALUES ('Pytest Temporary Co', 'Testing', 'Austin, TX', 'https://testco.edu')
            RETURNING company_id;
        """)
        new_cid = cur.fetchone()[0]
        assert new_cid > 0

        # Read
        cur.execute("SELECT company_name, industry FROM companies WHERE company_id = %s;", (new_cid,))
        comp = cur.fetchone()
        assert comp[0] == 'Pytest Temporary Co'

        # Update
        cur.execute("UPDATE companies SET location = 'Dallas, TX' WHERE company_id = %s;", (new_cid,))
        cur.execute("SELECT location FROM companies WHERE company_id = %s;", (new_cid,))
        assert cur.fetchone()[0] == 'Dallas, TX'

        # Delete
        cur.execute("DELETE FROM companies WHERE company_id = %s;", (new_cid,))
        cur.execute("SELECT COUNT(*) FROM companies WHERE company_id = %s;", (new_cid,))
        assert cur.fetchone()[0] == 0
        db.rollback()


# =========================================================
# TEST SCENARIO 7: APPLICANT CRUD WITH ROLLBACK
# =========================================================
def test_07_applicant_crud(db):
    """Test Create, Read, Update, and Delete operations on applicants."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("""
            INSERT INTO applicants (full_name, email, phone, location)
            VALUES ('Pytest Candidate', 'pytest.candidate999@test.edu', '555-0100', 'California')
            RETURNING applicant_id;
        """)
        new_aid = cur.fetchone()[0]
        assert new_aid > 0

        cur.execute("SELECT full_name FROM applicants WHERE applicant_id = %s;", (new_aid,))
        assert cur.fetchone()[0] == 'Pytest Candidate'

        cur.execute("UPDATE applicants SET location = 'New York' WHERE applicant_id = %s;", (new_aid,))
        cur.execute("SELECT location FROM applicants WHERE applicant_id = %s;", (new_aid,))
        assert cur.fetchone()[0] == 'New York'

        cur.execute("DELETE FROM applicants WHERE applicant_id = %s;", (new_aid,))
        cur.execute("SELECT COUNT(*) FROM applicants WHERE applicant_id = %s;", (new_aid,))
        assert cur.fetchone()[0] == 0
        db.rollback()


# =========================================================
# TEST SCENARIO 8: JOB CRUD WITH ROLLBACK
# =========================================================
def test_08_job_crud(db):
    """Test posting, reading, updating status, and deleting a job posting."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("SELECT company_id, recruiter_id FROM jobs LIMIT 1;")
        cid, rid = cur.fetchone()

        cur.execute("""
            INSERT INTO jobs (company_id, recruiter_id, job_title, description, location, salary, status)
            VALUES (%s, %s, 'Pytest Systems Architect', 'Test role', 'Remote', 150000.00, 'Open')
            RETURNING job_id;
        """, (cid, rid))
        new_jid = cur.fetchone()[0]
        assert new_jid > 0

        cur.execute("UPDATE jobs SET status = 'Closed' WHERE job_id = %s;", (new_jid,))
        cur.execute("SELECT status FROM jobs WHERE job_id = %s;", (new_jid,))
        assert cur.fetchone()[0] == 'Closed'

        cur.execute("DELETE FROM jobs WHERE job_id = %s;", (new_jid,))
        db.rollback()


# =========================================================
# TEST SCENARIO 9: APPLICATION CREATION
# =========================================================
def test_09_application_creation(db):
    """Test submitting an application linking candidate, job, and resume."""
    with db.cursor() as cur:
        db.rollback()
        # Create temp applicant
        cur.execute("INSERT INTO applicants (full_name, email) VALUES ('App Tester', 'app.tester@test.edu') RETURNING applicant_id;")
        aid = cur.fetchone()[0]
        # Create temp resume
        cur.execute("INSERT INTO resumes (applicant_id, file_name, file_path) VALUES (%s, 'test_cv.pdf', 'uploads/test_cv.pdf') RETURNING resume_id;", (aid,))
        resid = cur.fetchone()[0]
        cur.execute("SELECT job_id FROM jobs LIMIT 1;")
        jid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO applications (applicant_id, job_id, resume_id, status)
            VALUES (%s, %s, %s, 'Applied')
            RETURNING application_id;
        """, (aid, jid, resid))
        app_id = cur.fetchone()[0]
        assert app_id > 0
        db.rollback()


# =========================================================
# TEST SCENARIO 10: DUPLICATE APPLICATION PREVENTION
# =========================================================
def test_10_duplicate_application_prevention(db):
    """Verify UNIQUE (applicant_id, job_id) constraint blocks duplicate submissions."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("SELECT applicant_id, job_id, resume_id FROM applications LIMIT 1;")
        row = cur.fetchone()
        aid, jid, resid = row[0], row[1], row[2]

        with pytest.raises(psycopg2.IntegrityError):
            cur.execute("""
                INSERT INTO applications (applicant_id, job_id, resume_id, status)
                VALUES (%s, %s, %s, 'Applied');
            """, (aid, jid, resid))
        db.rollback()


# =========================================================
# TEST SCENARIO 11: APPLICATION STATUS UPDATE PROCEDURE
# =========================================================
def test_11_application_status_update_procedure(db):
    """Verify PL/pgSQL update_application_status stored procedure modifies status."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("SELECT application_id, status FROM applications LIMIT 1;")
        aid, orig_status = cur.fetchone()

        target_status = 'Screening' if orig_status != 'Screening' else 'Interview'
        cur.execute("CALL update_application_status(%s, %s);", (aid, target_status))

        cur.execute("SELECT status FROM applications WHERE application_id = %s;", (aid,))
        assert cur.fetchone()[0] == target_status
        db.rollback()


# =========================================================
# TEST SCENARIO 12: INTERVIEW SCHEDULING PROCEDURE
# =========================================================
def test_12_interview_scheduling_procedure(db):
    """Verify PL/pgSQL schedule_interview stored procedure inserts interview and syncs status."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("SELECT application_id FROM applications WHERE status IN ('Applied', 'Screening') LIMIT 1;")
        row = cur.fetchone()
        if not row:
            # Fallback to any application and set it to Screening first
            cur.execute("SELECT application_id FROM applications LIMIT 1;")
            aid = cur.fetchone()[0]
            cur.execute("UPDATE applications SET status = 'Screening' WHERE application_id = %s;", (aid,))
        else:
            aid = row[0]

        int_date = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=3)

        cur.execute("CALL schedule_interview(%s, %s, %s, %s);", (aid, int_date, 'Video', 'Automated test schedule'))

        cur.execute("SELECT status FROM applications WHERE application_id = %s;", (aid,))
        assert cur.fetchone()[0] == 'Interview'
        db.rollback()


# =========================================================
# TEST SCENARIO 13: HIRING DECISIONS
# =========================================================
def test_13_hiring_decisions(db):
    """Verify recording a hiring decision and preventing duplicate decisions per application."""
    with db.cursor() as cur:
        db.rollback()
        # Find application without a decision
        cur.execute("SELECT application_id FROM applications WHERE application_id NOT IN (SELECT application_id FROM hiring_decisions) LIMIT 1;")
        row = cur.fetchone()
        if row:
            aid = row[0]
            cur.execute("INSERT INTO hiring_decisions (application_id, decision, remarks) VALUES (%s, 'Pending', 'Awaiting review');", (aid,))
            # Duplicate decision for same application should violate UNIQUE constraint
            with pytest.raises(psycopg2.IntegrityError):
                cur.execute("INSERT INTO hiring_decisions (application_id, decision) VALUES (%s, 'Hired');", (aid,))
        db.rollback()


# =========================================================
# TEST SCENARIO 14: CANDIDATE SKILL MATCHING
# =========================================================
def test_14_candidate_skill_matching(db):
    """Verify transparent percentage calculation comparing applicant skills with job requirements."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT
                j.job_id,
                j.job_title,
                a.full_name,
                COUNT(js.skill_id) AS matched_count,
                ROUND(100.0 * COUNT(js.skill_id) / NULLIF((SELECT COUNT(*) FROM job_skills WHERE job_id = j.job_id), 0), 1) AS match_pct
            FROM jobs j
            JOIN job_skills js ON j.job_id = js.job_id
            JOIN applicant_skills aps ON js.skill_id = aps.skill_id
            JOIN applicants a ON aps.applicant_id = a.applicant_id
            WHERE j.job_title = 'Software Engineer' AND a.full_name = 'Alex Carter'
            GROUP BY j.job_id, j.job_title, a.full_name;
        """)
        row = cur.fetchone()
        assert row is not None
        assert row[3] == 3  # Alex Carter matches 3 of 3 skills
        assert float(row[4]) == 100.0


# =========================================================
# TEST SCENARIO 15: SQL VIEWS
# =========================================================
def test_15_sql_views(db):
    """Verify applicant_application_view and recruitment_summary_view return data."""
    with db.cursor() as cur:
        cur.execute("SELECT * FROM applicant_application_view LIMIT 5;")
        v1_rows = cur.fetchall()
        assert len(v1_rows) > 0

        cur.execute("SELECT * FROM recruitment_summary_view;")
        v2_rows = cur.fetchall()
        assert len(v2_rows) > 0


# =========================================================
# TEST SCENARIO 16: STORED PROCEDURES DOMAIN VALIDATION
# =========================================================
def test_16_stored_procedures_validation(db):
    """Verify procedures reject invalid domain values and nonexistent IDs."""
    with db.cursor() as cur:
        db.rollback()
        # Invalid status string
        with pytest.raises(psycopg2.DatabaseError):
            cur.execute("CALL update_application_status(1, 'INVALID_STATUS_XYZ');")
        db.rollback()

        # Nonexistent application ID
        with pytest.raises(psycopg2.DatabaseError):
            cur.execute("CALL update_application_status(999999, 'Hired');")
        db.rollback()

        # Invalid interview type
        with pytest.raises(psycopg2.DatabaseError):
            cur.execute("CALL schedule_interview(1, CURRENT_TIMESTAMP, 'CarrierPigeon', 'Test');")
        db.rollback()


# =========================================================
# TEST SCENARIO 17: DASHBOARD QUERY ACCURACY
# =========================================================
def test_17_dashboard_metrics_accuracy(db):
    """Verify single-row executive KPI query matches actual table counts."""
    with db.cursor() as cur:
        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM companies) AS total_companies,
                (SELECT COUNT(*) FROM recruiters) AS total_recruiters,
                (SELECT COUNT(*) FROM applicants) AS total_applicants,
                (SELECT COUNT(*) FROM jobs) AS total_jobs,
                (SELECT COUNT(*) FROM applications) AS total_applications;
        """)
        row = cur.fetchone()
        assert row[0] >= 5
        assert row[1] >= 5
        assert row[2] >= 10
        assert row[3] >= 5
        assert row[4] >= 10


# =========================================================
# TEST SCENARIO 18: CSV REPORT GENERATION
# =========================================================
def test_18_csv_report_generation(db):
    """Verify DataFrame CSV serialization of database view data."""
    with db.cursor() as cur:
        cur.execute("SELECT * FROM recruitment_summary_view;")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=cols)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_text = csv_buffer.getvalue()
        assert "company_name" in csv_text
        assert len(csv_text.splitlines()) >= 2


# =========================================================
# TEST SCENARIO 19: INPUT VALIDATION & CONSTRAINTS
# =========================================================
def test_19_input_validation_and_check_constraints(db):
    """Verify negative salaries and duplicate emails are rejected by PostgreSQL."""
    with db.cursor() as cur:
        db.rollback()
        # Negative salary CHECK constraint
        with pytest.raises(psycopg2.IntegrityError):
            cur.execute("""
                INSERT INTO jobs (company_id, recruiter_id, job_title, salary, status)
                VALUES (1, 1, 'Negative Salary Role', -1000.00, 'Open');
            """)
        db.rollback()

        # Duplicate email UNIQUE constraint
        with pytest.raises(psycopg2.IntegrityError):
            cur.execute("""
                INSERT INTO applicants (full_name, email)
                VALUES ('Clone Candidate', 'alex.carter@example.com');
            """)
        db.rollback()


# =========================================================
# TEST SCENARIO 20: TRANSACTION ROLLBACK BEHAVIOR
# =========================================================
def test_20_transaction_rollback_behavior(db):
    """Verify explicit rollback completely reverts database state."""
    with db.cursor() as cur:
        db.rollback()
        cur.execute("SELECT COUNT(*) FROM companies;")
        before_count = cur.fetchone()[0]

        cur.execute("INSERT INTO companies (company_name, industry) VALUES ('Rollback Co', 'Test');")
        cur.execute("SELECT COUNT(*) FROM companies;")
        assert cur.fetchone()[0] == before_count + 1

        db.rollback()

        cur.execute("SELECT COUNT(*) FROM companies;")
        assert cur.fetchone()[0] == before_count


# =========================================================
# TEST SCENARIO 21: CANDIDATE SKILL MATCHING - NVIDIA MACHINE LEARNING ENGINEER (REGRESSION)
# =========================================================
def test_21_candidate_skill_matching_nvidia_regression(db):
    """
    Regression test for IndexError: tuple index out of range.
    Specifically tests Job 5 (Machine Learning Engineer @ NVIDIA) with 3 required skills:
    Docker, Machine Learning, Python.
    Verifies:
      1. Safe parameter binding with (total_req, target_jid).
      2. No tuple index error occurs.
      3. Expected ranking columns exist ('Candidate', 'Email Address', 'Location',
         'Matched Competencies', 'Match %', 'Matched Skills', 'applicant_id').
      4. Mathematical accuracy: 2/3 = 66.7% for top candidates.
      5. Candidates with 0 matches are safely handled (0 competencies, 0.0% match).
    """
    with db.cursor() as cur:
        # Locate NVIDIA Machine Learning Engineer position
        cur.execute("""
            SELECT j.job_id, j.job_title, c.company_name
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE j.job_title = 'Machine Learning Engineer' AND c.company_name = 'NVIDIA';
        """)
        job_row = cur.fetchone()
        assert job_row is not None, "NVIDIA Machine Learning Engineer job requisition not found"
        target_jid = job_row[0]

        # Verify 3 required skills: Docker, Machine Learning, Python
        cur.execute("""
            SELECT s.skill_id, s.skill_name, js.required_level
            FROM job_skills js
            JOIN skills s ON js.skill_id = s.skill_id
            WHERE js.job_id = %s
            ORDER BY s.skill_name;
        """, (target_jid,))
        reqs = cur.fetchall()
        assert len(reqs) == 3, f"Expected 3 required skills, found {len(reqs)}"
        req_names = {r[1] for r in reqs}
        assert req_names == {"Docker", "Machine Learning", "Python"}
        total_req = len(reqs)

        # Test direct execution via execute_query with escaped literal %%
        app_ranking_sql = """
            SELECT
                a.full_name AS "Candidate",
                a.email AS "Email Address",
                a.location AS "Location",
                COUNT(js.skill_id) AS "Matched Competencies",
                COALESCE(ROUND(100.0 * COUNT(js.skill_id) / NULLIF(%s, 0), 1), 0.0) AS "Match %%",
                COALESCE(STRING_AGG(CASE WHEN js.skill_id IS NOT NULL THEN s.skill_name || ' (' || aps.proficiency_level || ')' END, ', ' ORDER BY s.skill_name), 'None') AS "Matched Skills",
                a.applicant_id
            FROM applicants a
            LEFT JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
            LEFT JOIN skills s ON aps.skill_id = s.skill_id
            LEFT JOIN job_skills js ON js.skill_id = s.skill_id AND js.job_id = %s
            GROUP BY a.applicant_id, a.full_name, a.email, a.location
            ORDER BY "Matched Competencies" DESC, "Match %%" DESC, a.full_name ASC;
        """
        ranked = execute_query(app_ranking_sql, (total_req, target_jid))
        assert len(ranked) >= 10, f"Expected at least 10 applicants ranked, got {len(ranked)}"

        # Validate expected columns
        expected_cols = {"Candidate", "Email Address", "Location", "Matched Competencies", "Match %", "Matched Skills", "applicant_id"}
        assert set(ranked[0].keys()) == expected_cols

        # Validate top match accuracy (2 of 3 = 66.7%)
        top = ranked[0]
        assert top["Matched Competencies"] == 2
        assert float(top["Match %"]) == 66.7
        assert "Machine Learning" in top["Matched Skills"]
        assert "Python" in top["Matched Skills"]

        # Validate zero-match handling: candidates with no matching skills have 0 competencies and 0.0%
        zero_match_candidates = [r for r in ranked if r["Matched Competencies"] == 0]
        assert len(zero_match_candidates) > 0, "Expected at least one candidate with zero matching skills"
        for z in zero_match_candidates:
            assert float(z["Match %"]) == 0.0
            assert z["Matched Skills"] == "None"


# =========================================================
# TEST SCENARIO 22: CANDIDATE SKILL MATCHING - ALL FIVE SAMPLE JOBS
# =========================================================
def test_22_candidate_skill_matching_all_five_sample_jobs(db):
    """Verify Candidate Skill Matching runs without exception across all five sample jobs."""
    app_ranking_sql = """
        SELECT
            a.full_name AS "Candidate",
            a.email AS "Email Address",
            a.location AS "Location",
            COUNT(js.skill_id) AS "Matched Competencies",
            COALESCE(ROUND(100.0 * COUNT(js.skill_id) / NULLIF(%s, 0), 1), 0.0) AS "Match %%",
            COALESCE(STRING_AGG(CASE WHEN js.skill_id IS NOT NULL THEN s.skill_name || ' (' || aps.proficiency_level || ')' END, ', ' ORDER BY s.skill_name), 'None') AS "Matched Skills",
            a.applicant_id
        FROM applicants a
        LEFT JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
        LEFT JOIN skills s ON aps.skill_id = s.skill_id
        LEFT JOIN job_skills js ON js.skill_id = s.skill_id AND js.job_id = %s
        GROUP BY a.applicant_id, a.full_name, a.email, a.location
        ORDER BY "Matched Competencies" DESC, "Match %%" DESC, a.full_name ASC;
    """

    jobs = execute_query("SELECT job_id, job_title, company_name FROM jobs j JOIN companies c ON j.company_id = c.company_id WHERE j.job_id <= 5 ORDER BY job_id;")
    assert len(jobs) == 5, f"Expected 5 sample jobs, found {len(jobs)}"

    for j in jobs:
        jid = j["job_id"]
        reqs = execute_query("SELECT s.skill_id, s.skill_name, js.required_level FROM job_skills js JOIN skills s ON js.skill_id = s.skill_id WHERE js.job_id = %s;", (jid,))
        total_req = len(reqs)
        assert total_req > 0, f"Sample Job {j['job_title']} has no required skills"

        ranked = execute_query(app_ranking_sql, (total_req, jid))
        assert len(ranked) >= 10, f"Failed ranking for job {j['job_title']}"

        # Verify ranking order: highest match first
        for i in range(len(ranked) - 1):
            assert ranked[i]["Matched Competencies"] >= ranked[i + 1]["Matched Competencies"]
            assert float(ranked[i]["Match %"]) >= float(ranked[i + 1]["Match %"])


# =========================================================
# TEST SCENARIO 23: ZERO REQUIRED SKILLS AND ZERO DIVISION SAFETY
# =========================================================
def test_23_candidate_skill_matching_zero_required_skills_safety(db):
    """Verify that total_req = 0 does not raise ZeroDivisionError or PostgreSQL division by zero."""
    app_ranking_sql = """
        SELECT
            a.full_name AS "Candidate",
            COUNT(js.skill_id) AS "Matched Competencies",
            COALESCE(ROUND(100.0 * COUNT(js.skill_id) / NULLIF(%s, 0), 1), 0.0) AS "Match %%"
        FROM applicants a
        LEFT JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
        LEFT JOIN skills s ON aps.skill_id = s.skill_id
        LEFT JOIN job_skills js ON js.skill_id = s.skill_id AND js.job_id = %s
        GROUP BY a.applicant_id, a.full_name, a.email, a.location
        ORDER BY "Matched Competencies" DESC, "Match %%" DESC, a.full_name ASC;
    """

    # Calling with total_req = 0 must succeed and return 0.0% without error
    ranked = execute_query(app_ranking_sql, (0, 1))
    assert len(ranked) > 0
    for r in ranked:
        assert float(r["Match %"]) == 0.0
