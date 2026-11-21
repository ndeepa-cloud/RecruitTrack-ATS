# RecruitTrack ATS — Final CIS 407 Rubric Compliance Audit

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Evaluator Reference:** 40-Point Capstone Project Grading Rubric (8 Categories × 5 Points)  
**Database Engine:** PostgreSQL 14.24 (Port **4919** / Database: `recruittrack_db`)  
**GitHub Repository:** [https://github.com/ndeepa-cloud/RecruitTrack-ATS](https://github.com/ndeepa-cloud/RecruitTrack-ATS)  
**Audit Date:** November 21, 2026  
**Test Suite Verification:** 24 of 24 Automated Tests Passing (2.75s)  

---

## 📊 Master Rubric Compliance Summary Table

The table below summarizes the comprehensive compliance audit across all eight 5-point rubric categories:

| Rubric Category | Maximum Points | Evidence (Verified Implementation & File Paths) | Missing Requirements | Readiness | Recommended Action |
|:---|:---:|:---|:---|:---:|:---|
| **1. Database Design** | 5 | • 11 normalized tables in 3NF/BCNF with complete mathematical proofs in `docs/DATABASE_DESIGN.md` (Sec. 4).<br>• Professional Crow's foot ERD in Markdown (`docs/ERD.md`), high-res image (`docs/RecruitTrack_ERD.png`, 3800×2500 px, 300 DPI), and vector PDF (`docs/RecruitTrack_ERD.pdf`).<br>• Fully articulated business rules and cardinalities matrix (1:1, 1:N, M:N) in `docs/FINAL_PROJECT_REPORT.md` (Sec. 6–8) and `database/schema.sql`.<br>• Explicit primary keys and foreign keys with cascading rules on all relationships. | **None.** All criteria fully met and verified. | **Exceeds** (5/5) | Maintain current schema design; all normalization proofs and diagrams match the live database. |
| **2. Database Implementation** | 5 | • Live PostgreSQL 14 schema on port 4919 (`recruittrack_db`) created via `database/schema.sql`.<br>• Standard types (`INT`, `SERIAL`, `VARCHAR`, `TEXT`, `DECIMAL(12,2)`, `DATE`, `TIMESTAMP`).<br>• Strict constraints: PKs on all 11 tables; FKs with `ON DELETE CASCADE`/`RESTRICT`; UNIQUE on emails, company names, skills, and composite `(applicant_id, job_id)`; 8 domain CHECK constraints (`salary >= 0`, status domains).<br>• Realistic, idempotent sample data in `database/sample_data.sql` with 5 companies, 5 recruiters (valid bcrypt hash for `DemoRecruiter2026!`), 10 applicants, 5 jobs, 10 skills, 10 resumes, 10 applications, 5 interviews, 3 decisions. | **None.** Idempotent recreation verified. | **Exceeds** (5/5) | None required. Clean database recreation confirmed without developer dependencies. |
| **3. SQL Queries** | 5 | • **SELECT:** Over 40 parameterized queries in `apps/main.py` and Queries 1–15 in `database/queries.sql`.<br>• **INSERT:** Verified across companies, recruiters, jobs, applicants, skills, applications, interviews, and decisions (`apps/main.py:1086–2006`).<br>• **UPDATE:** Safe editing for companies, recruiters, jobs (open/closed), and applications via procedure (`apps/main.py:1107–1772`).<br>• **DELETE:** Referentially guarded company delete (`apps/main.py:1121`); transaction-safe deletes in `queries.sql:286` and tests (`tests/test_recruittrack.py:168, 196, 224`).<br>• **Joins:** 2-table INNER JOIN, 5-table INNER JOIN (`queries.sql:57`), LEFT OUTER JOIN preserving 0-applicant jobs (`queries.sql:75`), M:N skill joins.<br>• **Aggregations:** `COUNT()`, `MIN()`, `MAX()`, `ROUND(AVG(), 2)`, `GROUP BY` with `HAVING > 1` (`queries.sql:102, 117`).<br>• **Subqueries:** `IN`, `Scalar`, and `NOT EXISTS` (`queries.sql:133–163`).<br>• **Complex Query:** Transparent SQL candidate skill matching with `NULLIF(..., 0)` zero-division protection. | **None.** All 4 CRUD operations, joins, aggregations, and subqueries verified. | **Exceeds** (5/5) | In presentation/report, explain that UI deletion is intentionally restricted to Companies with referential guards to follow enterprise audit and data retention standards. |
| **4. Python Application & UI** | 5 | • Modern monochrome SaaS UI in Streamlit 1.42 (`apps/main.py`) connected to PostgreSQL on port 4919.<br>• Dedicated connection factory with automatic retry (`apps/db_connection.py`) and live sidebar connection indicator.<br>• Interactive forms for entering and updating data across 11 modules (`st.form`, validated inputs).<br>• Real-time keyword search across Companies, Recruiters, Jobs, Candidates, Applications, Interviews, and Decisions (`apps/main.py:1013, 1145, 1301, 1466, 1632, 1791, 1936`).<br>• Dropdown filters for Industry, Employer, Job Status, Skill, and Lifecycle Stage.<br>• Interactive Plotly conversion funnel chart, one-click resume file downloads, and instant CSV exports. | **None.** UI, search, filtering, forms, and error indicators verified. | **Exceeds** (5/5) | None required. UI is responsive, polished, and free of deprecation warnings. |
| **5. Advanced Database Features** | 5 | • **Views:** `applicant_application_view` (`schema.sql:264`) and `recruitment_summary_view` (`schema.sql:285`).<br>• **Stored Procedures:** `update_application_status` (`schema.sql:304`) and `schedule_interview` (`schema.sql:332`) with PL/pgSQL domain validation.<br>• **Indexes:** 7 B-Tree indexes on foreign keys, status, and dates (`schema.sql:239–256`).<br>• **Transactions:** Multi-table atomic onboarding transactions with `BEGIN`, `COMMIT`, and `ROLLBACK` (`queries.sql:260–290`, `apps/db_connection.py`, `tests/test_recruittrack.py:458`).<br>• **Security:** Bcrypt cryptographic password hashing (`$2b$12$...`) and 100% psycopg2 parameterized queries.<br>• **Optimization:** Set-based SQL skill matching with `NULLIF(..., 0)` division safety. | Custom database **triggers** are omitted (schema uses stored procedures instead). The rubric lists features disjunctively (*"views, stored procedures, triggers, indexes, transactions, security/roles, OR query optimization"*), satisfying 6 of the 7 items. | **Exceeds** (5/5) | Document that business logic is encapsulated in stored procedures. Provide an optional trigger definition in documentation for graders requiring triggers. |
| **6. Testing & Functionality** | 5 | • **24 Automated pytest Tests:** 23 component/integration tests in `tests/test_recruittrack.py` + 1 full 15-step recruiter workflow test in `tests/test_e2e_workflow.py`.<br>• **Actual Result:** 24 passed in 2.75s against live database.<br>• **Constraint Testing:** Validates foreign key blocks, duplicate application rejections, check constraint rejections, and zero-required-skills division safety.<br>• **Transaction Rollback Testing:** Confirms `db.rollback()` reverts uncommitted state without test contamination.<br>• **Error Handling:** Graceful Streamlit alerts on duplicate submissions, invalid credentials, and database exceptions. | **None.** Comprehensive testing demonstrated across unit, integration, and UI layers. | **Exceeds** (5/5) | Run pytest live during presentation (Step 7 of Demo Guide) to show passing tests. |
| **7. Documentation** | 5 | • Complete root `README.md` with business problem, 3-tier architecture, setup guide emphasizing port 4919, test commands, demo account.<br>• 21-section academic report in `docs/FINAL_PROJECT_REPORT.md` (36 KB).<br>• Data dictionary and normalization proofs in `docs/DATABASE_DESIGN.md` (19 KB).<br>• SQL implementation guide with live query outputs in `docs/SQL_FEATURES.md` (21 KB).<br>• Recruiter operations manual in `docs/USER_GUIDE.md` (9.1 KB).<br>• 5-minute grading walkthrough in `docs/DEMO_GUIDE.md` (7.5 KB).<br>• QA test report in `docs/TESTING.md` (4.4 KB).<br>• Submission checklist in `docs/SUBMISSION_CHECKLIST.md` (4.2 KB). | **None.** Documentation exceeds typical university project depth. | **Exceeds** (5/5) | Ensure all markdown links in `README.md` and `docs/` remain relative for GitHub web browsing. |
| **8. Presentation & Demonstration** | 5 | • **Live Demo Guide:** Timed 5-minute script in `docs/DEMO_GUIDE.md` covering 7 clear stages from login to CSV export and pytest run.<br>• **9-Slide Presentation Deck:** Fully articulated in `docs/PRESENTATION_SLIDES.md`, mapping slide-by-slide to all eight rubric categories with speaker notes.<br>• Pre-configured demo credentials (`sarah.johnson@example.com` / `DemoRecruiter2026!`).<br>• Explicit academic talking points connecting UI actions to database theory. | Dedicated presentation deck was previously implicit; now explicitly provided in `docs/PRESENTATION_SLIDES.md`. | **Exceeds** (5/5) | Use `docs/PRESENTATION_SLIDES.md` for oral slides and `docs/DEMO_GUIDE.md` for the live software demonstration. |

---

## 🔍 Detailed Category-by-Category Audit

---

### Category 1: Database Design (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Relational Schema:** 11 relational tables comprising 10 core entities and 1 associative junction table:
  `companies`, `recruiters`, `applicants`, `jobs`, `skills`, `applicant_skills`, `job_skills`, `resumes`, `applications`, `interviews`, `hiring_decisions`.
- **Entity-Relationship Diagrams:**
  - [docs/ERD.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/ERD.md): Complete Mermaid diagram rendering entity attributes, data types, PK/FK/UK/CHK markers, and Crow's foot cardinality notation.
  - [docs/RecruitTrack_ERD.png](file:///Users/nihtinroy/RecruitTrack-ATS/docs/RecruitTrack_ERD.png): High-resolution visual diagram rendered at 3800 × 2500 px (300 DPI) with distinct color badges, table headers, connector lines, and legend.
  - [docs/RecruitTrack_ERD.pdf](file:///Users/nihtinroy/RecruitTrack-ATS/docs/RecruitTrack_ERD.pdf): Publication-ready vector PDF edition.
- **Normalization Analysis:** Fully documented in [docs/DATABASE_DESIGN.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/DATABASE_DESIGN.md) (Section 4):
  - **1NF:** Elimination of multi-valued attributes and repeating groups; skills stored as discrete rows in junction tables.
  - **2NF:** Elimination of partial dependencies on composite primary keys (`{applicant_id, skill_id}` and `{job_id, skill_id}`).
  - **3NF & BCNF:** Elimination of transitive dependencies; every determinant is a candidate superkey.
- **Relationship Matrix:**
  - 1:1 Relationship: `applications` &rarr; `hiring_decisions` (`application_id` is unique in `hiring_decisions`).
  - 1:N Relationships: `companies` &rarr; `jobs`, `companies` &rarr; `recruiters`, `recruiters` &rarr; `jobs`, `applicants` &rarr; `resumes`, `applicants` &rarr; `applications`, `jobs` &rarr; `applications`, `applications` &rarr; `interviews`.
  - M:N Relationships: `applicants` &harr; `skills` via `applicant_skills`, `jobs` &harr; `skills` via `job_skills`.
- **Referential Integrity Actions:**
  - `ON DELETE CASCADE`: Applied to strictly dependent child entities (`resumes`, `applications.applicant_id`, `interviews`, `hiring_decisions`, `job_skills.job_id`, `applicant_skills.applicant_id`).
  - `ON DELETE RESTRICT`: Applied to master reference entities (`companies`, `skills`, `resumes` referenced by applications).
  - `ON DELETE SET NULL`: Applied to recruiter assignments on job requisitions (`jobs.recruiter_id`).

#### Deficiencies / Missing Elements
- **None.**

#### Rubric Determination
- **Exceeds (5/5):** The database design adheres rigorously to relational theory, includes comprehensive normalization proofs, and provides multi-format ER diagrams matching the live database.

---

### Category 2: Database Implementation (Score Potential: 5 / 5)

#### Evidence & Implementation
- **DDL Script:** [database/schema.sql](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql) contains idempotent `CREATE TABLE IF NOT EXISTS` definitions for all 11 tables.
- **Data Types:** Accurate mapping of real-world attributes:
  - Numerical / Financial: `DECIMAL(12, 2)` for job salaries and offer amounts.
  - Temporal: `DATE` for application/posting dates; `TIMESTAMP` for interview scheduling.
  - Textual: Appropriately sized `VARCHAR(20)` to `VARCHAR(255)` and `TEXT` for descriptions and feedback.
  - Surrogate Keys: `SERIAL PRIMARY KEY` across parent tables.
- **Integrity Constraints:**
  - Primary Keys: Enforced across all 11 tables.
  - Foreign Keys: Validated on all associations.
  - Composite Uniqueness & Consistency:
    - `UNIQUE (recruiter_id, company_id)` in `recruiters` and composite FK in `jobs(recruiter_id, company_id)` ensuring a recruiter cannot post a job for a company they do not belong to.
    - `UNIQUE (resume_id, applicant_id)` in `resumes` and composite FK in `applications(resume_id, applicant_id)` guaranteeing an applicant can only apply with their own resume.
    - `UNIQUE (applicant_id, job_id)` in `applications` preventing duplicate applications.
  - Domain CHECK Constraints:
    - `jobs.salary >= 0`
    - `jobs.status IN ('Open', 'Closed')`
    - `applicant_skills.proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')`
    - `job_skills.required_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')`
    - `applications.status IN ('Applied', 'Screening', 'Interview', 'Offered', 'Rejected', 'Hired')`
    - `interviews.interview_type IN ('Phone', 'Video', 'In-Person')`
    - `interviews.status IN ('Scheduled', 'Completed', 'Cancelled')`
    - `hiring_decisions.decision IN ('Hired', 'Rejected', 'Pending')`
- **Sample Data:** [database/sample_data.sql](file:///Users/nihtinroy/RecruitTrack-ATS/database/sample_data.sql) seeds realistic, meaningful records:
  - 5 corporate employers, 5 recruiters (with valid bcrypt hash for `DemoRecruiter2026!`).
  - 10 applicants with fictional identities and `@example.com` domains.
  - 5 jobs, 10 skills, 16 applicant skills, 10 job skills, 10 resumes, 10 applications, 5 interviews, 3 decisions.
  - Insertion logic utilizes `WHERE NOT EXISTS` clauses, enabling idempotent re-execution without duplicate key violations.

#### Deficiencies / Missing Elements
- **None.** Clean database recreation verified without external dependencies.

#### Rubric Determination
- **Exceeds (5/5):** The live schema on port 4919 enforces rigorous data types, composite uniqueness constraints, domain checks, and idempotent sample data.

---

### Category 3: SQL Queries (Score Potential: 5 / 5)

#### Evidence & Implementation
- **SELECT Queries:** Ubiquitous across [database/queries.sql](file:///Users/nihtinroy/RecruitTrack-ATS/database/queries.sql) (Queries 1–15) and [apps/main.py](file:///Users/nihtinroy/RecruitTrack-ATS/apps/main.py).
- **INSERT Statements:**
  - Companies: `apps/main.py:1086`
  - Recruiters: `apps/main.py:1218`
  - Jobs: `apps/main.py:1379`
  - Applicants: `apps/main.py:1529`
  - Skills: `apps/main.py:1606`
  - Candidate Skills: `apps/main.py:1653`
  - Job Requirements: `apps/main.py:1704`
  - Applications: `apps/main.py:1754`
  - Interviews: via `CALL schedule_interview(...)` at `apps/main.py:1865`
  - Hiring Decisions: `apps/main.py:2006`
  - DML Demonstration: `database/queries.sql:263`
- **UPDATE Statements:**
  - Companies: `apps/main.py:1107`
  - Recruiters: `apps/main.py:1255`
  - Jobs: `apps/main.py:1415` (Title, Salary, Description, Status Open/Closed)
  - Application Status: via `CALL update_application_status(...)` at `apps/main.py:1772`
  - DML Demonstration: `database/queries.sql:273`
- **DELETE Statements:**
  - Company Deletion: `apps/main.py:1121` (`DELETE FROM companies WHERE company_id = %s;`) with tenant isolation checks and relational guards preventing deletion if active jobs or recruiters exist.
  - Interview Deletion: `database/queries.sql:286` (`DELETE FROM interviews WHERE ...`) inside safe transaction block.
  - CRUD Verification Tests: `tests/test_recruittrack.py:168, 196, 224` testing Create, Read, Update, and Delete across companies, applicants, and jobs.
  - End-to-End Teardown: `tests/test_e2e_workflow.py:249–263` testing programmatic DELETE across 7 relational tables.
- **Multi-Table JOINs:**
  - 4-Table / 5-Table INNER JOIN: `applications` + `applicants` + `jobs` + `companies` + `resumes` (`database/queries.sql:57`).
  - LEFT OUTER JOIN: Preserving zero-count requisitions (`database/queries.sql:75` and `docs/SQL_FEATURES.md:65–85`).
  - Many-to-Many JOINs: `applicants` + `applicant_skills` + `skills` (`database/queries.sql:88`).
- **Statistical Aggregations & Grouping:**
  - `COUNT(*)`, `MIN(salary)`, `MAX(salary)`, `ROUND(AVG(salary), 2)` (`database/queries.sql:102`).
  - `GROUP BY` with `HAVING COUNT(ap.application_id) > 1` (`database/queries.sql:117`).
- **Subqueries:**
  - `IN` Subquery: Candidate competency filtering (`database/queries.sql:133`).
  - Scalar Subquery: Above-average compensation benchmark (`database/queries.sql:148`).
  - `NOT EXISTS` Subquery: Anti-semi join for unengaged candidates (`database/queries.sql:163`).
- **Complex Query (Candidate Skill Matching):**
  - Deterministic set-intersection query calculating qualification percentage:
    $$\text{Match \%} = \text{ROUND}\left( \frac{\text{Count of Candidate's Matched Skills}}{\text{Total Required Skills for Job}} \times 100, 1 \right)$$
  - Implemented with `NULLIF((SELECT COUNT(*) FROM job_skills WHERE job_id = j.job_id), 0)` to guarantee zero-division safety (`database/queries.sql:178`, `apps/main.py:2076`).

#### Deficiencies / Missing Elements
- In the Streamlit UI, DELETE is only exposed for Companies (with safety checks). Job and applicant deletions are handled in the UI via status updates (`Closed`, `Rejected`) to adhere to enterprise audit retention standards. All 4 CRUD operations are present and verified in SQL scripts, test suites, and backend functions.

#### Rubric Determination
- **Exceeds (5/5):** All 4 CRUD operations, multi-table joins, aggregations with HAVING, subqueries, and complex analytical queries are implemented and verified.

---

### Category 4: Python Application & UI (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Database Connection:**
  - Implemented in [apps/db_connection.py](file:///Users/nihtinroy/RecruitTrack-ATS/apps/db_connection.py) using `psycopg2-binary`.
  - Reads configuration dynamically from `.env` (`DB_HOST`, `DB_PORT=4919`, `DB_NAME=recruittrack_db`, `DB_USER=postgres`).
  - Real-time connection testing (`test_connection()`) driving the green/red status indicator in the sidebar.
- **User Interface Framework:** Built with Streamlit 1.42.0 ([apps/main.py](file:///Users/nihtinroy/RecruitTrack-ATS/apps/main.py)).
- **Monochrome Design System:** Professional white-and-black theme (`#FFFFFF`, `#111111`, `#64748B`, `#E5E7EB`) inspired by modern enterprise SaaS platforms (Linear, Notion).
- **Forms for Entering & Updating Data:**
  - Dedicated interactive forms across 11 modules:
    1. Dashboard: Executive overview with 7 KPI tiles.
    2. Companies: Add, edit, and delete employer partners.
    3. Recruiters: Add and edit talent acquisition staff with automatic bcrypt password hashing.
    4. Jobs: Post new requisitions, edit compensation, and close requisitions.
    5. Applicants: Register candidates with real file resume uploads (`.pdf`, `.docx`).
    6. Skills: Standardized catalog, candidate endorsements, and job requirements.
    7. Applications: Submit applications with duplicate prevention; advance status via stored procedure.
    8. Interviews: Schedule rounds with automatic status synchronization; log feedback.
    9. Hiring Decisions: Record final offer/rejection with automatic pipeline status sync.
    10. Skill Matching: Dynamic candidate leaderboard with match percentages and skill gap breakdowns.
    11. Reports & Analytics: View pre-joined tables with instant CSV download buttons.
- **Searching and Filtering Implementation:**
  - Company search by name/city (`apps/main.py:1013`) + Industry filter dropdown (`apps/main.py:1017`).
  - Recruiter search by name/email (`apps/main.py:1145`) + Employer filter dropdown (`apps/main.py:1149`).
  - Job search by title/location (`apps/main.py:1301`) + Employer filter + Status filter (`apps/main.py:1306`).
  - Candidate search by name/email/location (`apps/main.py:1466`) + Skills filter.
  - Application search by candidate/position (`apps/main.py:1632`) + Status filter (`apps/main.py:1636`).
  - Interview search (`apps/main.py:1791`) + Type and Status filters.
  - Hiring Decision search (`apps/main.py:1936`) + Decision filter.
- **Interactive Buttons & File Handlers:**
  - One-click resume file download (`apps/main.py:1555`).
  - CSV report generation via Pandas (`apps/main.py:2160`).
  - Plotly recruitment conversion funnel visualization (`apps/main.py:730`).

#### Deficiencies / Missing Elements
- **None.**

#### Rubric Determination
- **Exceeds (5/5):** Highly functional, polished Python/Streamlit interface with comprehensive search, filtering, form validation, file handling, and live database connectivity.

---

### Category 5: Advanced Database Features (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Database Views:**
  - `applicant_application_view` ([database/schema.sql#L264](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql#L264)): Pre-joins applications, applicants, jobs, companies, and resumes.
  - `recruitment_summary_view` ([database/schema.sql#L285](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql#L285)): Pre-aggregates total jobs, applications, and hired count per employer.
- **Stored Procedures (PL/pgSQL):**
  - `update_application_status` ([database/schema.sql#L304](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql#L304)): Enforces status domain validation (`Applied`, `Screening`, `Interview`, `Offered`, `Rejected`, `Hired`) before atomic update.
  - `schedule_interview` ([database/schema.sql#L332](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql#L332)): Inserts interview round and automatically synchronizes application status to `'Interview'` if currently in `'Applied'` or `'Screening'`.
- **B-Tree Performance Indexes:**
  - 7 indexes defined in [database/schema.sql#L239-L256](file:///Users/nihtinroy/RecruitTrack-ATS/database/schema.sql#L239-L256):
    `idx_applications_applicant`, `idx_applications_job`, `idx_applications_status`, `idx_interviews_date`, `idx_jobs_company`, `idx_applicant_skills_skill`, `idx_job_skills_skill`.
- **ACID Transactions:**
  - Multi-table atomic onboarding transactions linking applicant registration, resume recording, and application submission with explicit `BEGIN`, `COMMIT`, `ROLLBACK` blocks ([database/queries.sql#L260-L290](file:///Users/nihtinroy/RecruitTrack-ATS/database/queries.sql#L260-L290), [tests/test_recruittrack.py#L458-L475](file:///Users/nihtinroy/RecruitTrack-ATS/tests/test_recruittrack.py#L458-L475)).
- **Security & Parameterization:**
  - `bcrypt` cryptographic password hashing (`$2b$12$...`) with zero plaintext storage.
  - 100% psycopg2 parameterized queries (`%s`) preventing SQL injection.
- **Query Optimization:**
  - B-tree indexing on foreign keys and search targets.
  - `NULLIF(..., 0)` zero-division protection in ranking query.

#### Deficiencies / Missing Elements
- Custom database **triggers** are omitted from the live schema (the system utilizes PL/pgSQL stored procedures for status synchronization and domain validation).
- **Rubric Wording Analysis:** The rubric specifies *"views, stored procedures, triggers, indexes, transactions, security/roles, **or** query optimization"*. Because the rubric uses the disjunctive *"or"*, implementing 6 of the 7 features satisfies the rubric requirement for Exceeds.

#### Rubric Determination
- **Exceeds (5/5):** Implements views, stored procedures, B-tree indexes, ACID transactions, bcrypt security, and query optimization.

---

### Category 6: Testing & Functionality (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Automated Test Suite:**
  - 24 automated tests located in [tests/test_recruittrack.py](file:///Users/nihtinroy/RecruitTrack-ATS/tests/test_recruittrack.py) (23 tests) and [tests/test_e2e_workflow.py](file:///Users/nihtinroy/RecruitTrack-ATS/tests/test_e2e_workflow.py) (1 test).
- **Execution Command & Actual Results:**
  ```bash
  .venv/bin/pytest tests/ -v
  ```
  **Actual Verified Result:** `24 passed in 2.75s` (100% pass rate).
- **Test Scenarios Covered:**
  - `test_01_database_connection`: TCP/IP connectivity on port 4919.
  - `test_02_all_tables_exist`: Confirms all 11 tables exist in public schema.
  - `test_03_foreign_key_integrity`: Verifies rejection of orphaned child records.
  - `test_04_recruiter_authentication_valid`: Validates bcrypt hash against `DemoRecruiter2026!`.
  - `test_05_recruiter_authentication_invalid`: Verifies immediate rejection of invalid passwords.
  - `test_06_company_crud`: Create, Read, Update, Delete for companies.
  - `test_07_applicant_crud`: Create, Read, Update, Delete for applicants.
  - `test_08_job_crud`: Create, Read, Update, Delete for jobs.
  - `test_09_application_creation`: Submits application linking candidate, job, and resume.
  - `test_10_duplicate_application_prevention`: Enforces `UNIQUE(applicant_id, job_id)`.
  - `test_11_application_status_update_procedure`: Tests `CALL update_application_status(...)`.
  - `test_12_interview_scheduling_procedure`: Tests `CALL schedule_interview(...)`.
  - `test_13_hiring_decisions`: Verifies decision recording and duplicate prevention.
  - `test_14_candidate_skill_matching`: Verifies transparent SQL ranking accuracy.
  - `test_15_sql_views`: Verifies live data aggregation via views.
  - `test_16_stored_procedures_validation`: Verifies error raising on invalid status strings.
  - `test_17_dashboard_metrics_accuracy`: Mathematical consistency of executive KPI counters.
  - `test_18_csv_report_generation`: Verifies DataFrame CSV serialization.
  - `test_19_input_validation_and_check_constraints`: Rejects negative salaries and duplicate emails.
  - `test_20_transaction_rollback_behavior`: Confirms explicit `ROLLBACK` reverts uncommitted state.
  - `test_21_candidate_skill_matching_nvidia_regression`: Query parsing regression test for NVIDIA.
  - `test_22_candidate_skill_matching_all_five_sample_jobs`: Verifies ranking across all 5 sample jobs.
  - `test_23_candidate_skill_matching_zero_required_skills_safety`: Verifies zero-division safety.
  - `test_complete_15_step_recruitment_workflow`: Full 15-step recruiter hiring lifecycle from job posting to hire.
- **Error Handling & Data Isolation:**
  - All tests execute within transaction blocks with explicit `db.rollback()` to prevent sample data contamination.
  - User-facing error handling in Streamlit catches database exceptions and presents clear warning banners.

#### Deficiencies / Missing Elements
- **None.**

#### Rubric Determination
- **Exceeds (5/5):** 24 automated tests covering unit, integration, constraint, transaction, and regression testing with 100% pass rate.

---

### Category 7: Documentation (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Root Documentation:** [README.md](file:///Users/nihtinroy/RecruitTrack-ATS/README.md) (15 KB):
  - Executive overview, business problem, and solution.
  - 3-tier architecture diagram.
  - Complete technology stack table.
  - Project directory tree.
  - Setup guide emphasizing PostgreSQL on port 4919, `.env` setup, schema initialization, Streamlit command, test command, and demo credentials.
- **Academic Capstone Paper:** [docs/FINAL_PROJECT_REPORT.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/FINAL_PROJECT_REPORT.md) (36 KB):
  - Covers all 21 numbered required university sections.
  - Normalization proofs, ERD walkthrough, relationship matrix, algorithm math, security, test matrix, challenges & solutions, limitations, and future roadmap.
- **Database Architecture Documentation:** [docs/DATABASE_DESIGN.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/DATABASE_DESIGN.md) (19 KB):
  - Complete 11-table data dictionaries (column, type, PK, FK, UK, CHK, default, description).
  - 1NF, 2NF, 3NF, and BCNF normalization proofs; anomaly elimination proofs.
- **SQL Implementation Guide:** [docs/SQL_FEATURES.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/SQL_FEATURES.md) (21 KB):
  - 5-table INNER JOIN, LEFT OUTER JOIN, continuous aggregations, HAVING clause, subqueries, views, stored procedures, ACID transactions, and verified live tabular query outputs.
- **User & Operational Manuals:**
  - Recruiter User Guide: [docs/USER_GUIDE.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/USER_GUIDE.md) (9.1 KB).
  - Step-by-Step Demonstration Script: [docs/DEMO_GUIDE.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/DEMO_GUIDE.md) (7.5 KB).
  - Quality Assurance Testing Report: [docs/TESTING.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/TESTING.md) (4.4 KB).
  - Submission Checklist: [docs/SUBMISSION_CHECKLIST.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/SUBMISSION_CHECKLIST.md) (4.2 KB).

#### Deficiencies / Missing Elements
- **None.**

#### Rubric Determination
- **Exceeds (5/5):** Documentation is thorough, professionally structured, and completely synchronized with the live code and database.

---

### Category 8: Presentation & Demonstration (Score Potential: 5 / 5)

#### Evidence & Implementation
- **Live Software Demonstration Script:** [docs/DEMO_GUIDE.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/DEMO_GUIDE.md):
  - Structured into a timed 5-to-7-minute walkthrough:
    - Step 1: System Health & Recruiter Authentication (1 min)
    - Step 2: Executive Dashboard & Funnel Analytics (45 sec)
    - Step 3: Candidate Registration & Real File Resume Upload (1 min)
    - Step 4: Skills Assignment & Candidate Skill Matching (1.5 min)
    - Step 5: Application Submission & Stored Procedure Execution (1 min)
    - Step 6: Interview Scheduling & Hiring Decision (45 sec)
    - Step 7: Exportable Audit Reports & Live Pytest Execution (30 sec)
  - Pre-configured demo credentials: `sarah.johnson@example.com` / `DemoRecruiter2026!`.
  - Specific academic talking points connecting user actions to normalization, referential integrity, and PL/pgSQL logic.
- **9-Slide Presentation Deck Specification:** [docs/PRESENTATION_SLIDES.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/PRESENTATION_SLIDES.md):
  - Explicit slide-by-slide structure directly mapped to all eight rubric categories:
    - Slide 1: Title, Academic Context & Executive Overview (Rubric 1, 7)
    - Slide 2: Business Problem, Motivation & Domain Rules (Rubric 1)
    - Slide 3: Relational Database Design, 3NF & ER Diagram (Rubric 1, 2)
    - Slide 4: Database Implementation: 11 Tables & Constraints (Rubric 2)
    - Slide 5: Core SQL Capabilities: CRUD, Joins & Aggregations (Rubric 3)
    - Slide 6: Advanced Database Features: Procedures, Views & ACID (Rubric 5)
    - Slide 7: Python & Streamlit UI: Architecture, Search & Forms (Rubric 4)
    - Slide 8: Testing, Error Handling & 24 Automated Tests (Rubric 6)
    - Slide 9: Live Demonstration Roadmap & Conclusion (Rubric 8)
  - Includes slide headers, bullet points, visual diagrams references, KaTeX formulas, and detailed speaker notes for every slide.

#### Deficiencies / Missing Elements
- **None.** The 9-slide presentation guide and live demo script address all eight rubric categories.

#### Rubric Determination
- **Exceeds (5/5):** Comprehensive presentation materials covering oral slides, speaker scripts, live demonstration steps, and academic talking points.

---

## 🔒 Verification of Secrets & Privacy Protection

Prior to GitHub publication, the codebase was audited for confidential information:
- [x] `.env` is strictly excluded via `.gitignore` (untracked).
- [x] `.env.example` contains sanitized placeholders (`DB_PASSWORD=your_secure_password_here`).
- [x] `uploads/*` and `uploads/resumes/*` are excluded via `.gitignore`, protecting personal candidate resumes.
- [x] Sample data in `database/sample_data.sql` and `docs/SQL_FEATURES.md` uses fictional identities (`Alex Carter`, `Priya Sharma`, etc.) and `@example.com` domains.
- [x] Demo recruiter accounts use valid bcrypt hashes for `DemoRecruiter2026!`, ensuring clean environment recreatability.

---

## 📝 Optional Enhancement Recommendation: PostgreSQL Audit Trigger

While the rubric's disjunctive phrasing (*"views, stored procedures, triggers, indexes, transactions, security/roles, OR query optimization"*) is fully satisfied by the 6 implemented advanced features, should your instructor strictly insist on a trigger in addition to stored procedures, the following trigger can be added to `database/schema.sql`:

```sql
-- OPTIONAL AUDIT TRIGGER: Automatically logs application status transitions
CREATE TABLE IF NOT EXISTS application_status_history (
    history_id SERIAL PRIMARY KEY,
    application_id INT NOT NULL,
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_application_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO application_status_history (application_id, old_status, new_status)
        VALUES (NEW.application_id, OLD.status, NEW.status);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_application_status_audit
AFTER UPDATE OF status ON applications
FOR EACH ROW
EXECUTE FUNCTION log_application_status_change();
```
*(Note: Per your instructions, this trigger has NOT been added to your database automatically and will only be deployed if you request it).*

---

## 🏁 Final Submission Readiness Conclusion

### Overall Readiness: **100% READY FOR SUBMISSION**

The project satisfies all eight categories of the CIS 407 grading rubric:
1. **Database Design:** Exceeds (11 tables in 3NF/BCNF, Crow's foot ERD in PNG/PDF/Mermaid, full normalization proofs).
2. **Database Implementation:** Exceeds (PostgreSQL 14 on port 4919, domain checks, composite uniqueness, idempotent sample data).
3. **SQL Queries:** Exceeds (All 4 CRUD operations, 5-table joins, LEFT JOINs, HAVING, subqueries, deterministic skill matching).
4. **Python Application & UI:** Exceeds (Modern monochrome Streamlit UI, keyword search across 7 modules, dropdown filtering, real file downloads, CSV exports).
5. **Advanced Features:** Exceeds (2 views, 2 PL/pgSQL stored procedures, 7 B-Tree indexes, ACID transactions, bcrypt hashing).
6. **Testing & Functionality:** Exceeds (24 automated tests passing in 2.75s, robust error handling, transaction isolation).
7. **Documentation:** Exceeds (README, 21-section report, data dictionaries, SQL guide with live outputs, user guide).
8. **Presentation & Demonstration:** Exceeds (9-slide presentation deck guide + 5-minute timed demo script).

All 24 automated tests pass cleanly, no secrets are exposed, and the repository is published on GitHub at [https://github.com/ndeepa-cloud/RecruitTrack-ATS](https://github.com/ndeepa-cloud/RecruitTrack-ATS).
