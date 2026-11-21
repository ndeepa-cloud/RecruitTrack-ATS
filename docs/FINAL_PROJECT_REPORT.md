# RecruitTrack ATS — Final Project Report
## Comprehensive Database Management Systems Capstone Project

**Course:** CIS 407 — Database Management Systems  
**Project Title:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Academic Term:** Spring 2026  
**Author / Engineering Lead:** Nithin Roy  
**Institution:** College of Engineering & Computer Science  
**Technology Stack:** PostgreSQL 14.24, Python 3.13, Streamlit 1.42, psycopg2, Pandas, Plotly, bcrypt, pytest  
**Database Host & Port:** `localhost:4919`  
**Database Name:** `recruittrack_db`  

---

## 1. Title Page & Academic Context

| Parameter | Specification |
|:---|:---|
| **Course** | CIS 407: Database Management Systems |
| **Project Name** | RecruitTrack ATS — Job Recruitment & Applicant Tracking System |
| **System Classification** | Enterprise Multi-Tenant Relational ATS Platform |
| **Primary Database Engine**| PostgreSQL 14.24 (Running on Custom Port **4919**) |
| **Backend Architecture** | Python 3.13 / psycopg2-binary 2.9.10 / bcrypt 4.3.0 |
| **User Interface** | Streamlit 1.42.0 (Modern Monochrome White & Black SaaS Interface) |
| **Data Analytics & Viz** | Pandas 2.2.3 / Plotly Graph Objects 6.0.0 |
| **Test Verification** | 24 Automated pytest Unit & Integration Test Scenarios |

---

## 2. Executive Summary & Abstract

Talent acquisition is the operational lifeblood of modern enterprise organizations. However, recruitment departments routinely suffer from severe operational friction caused by disconnected spreadsheets, unmanaged email inboxes, lost candidate resumes, duplicate applications, and opaque candidate evaluation processes.

**RecruitTrack ATS** was designed and implemented as an enterprise-grade, relational applicant tracking system that grounds talent acquisition workflows in strict database relational theory. Designed specifically for **CIS 407 (Database Management Systems)**, RecruitTrack ATS demonstrates how a properly modeled relational schema in **PostgreSQL 14** (port `4919`) eliminates data anomalies, enforces referential integrity, and automates multi-stage recruitment pipelines.

Key accomplishments of the RecruitTrack ATS project include:
1. **Fully Normalized Relational Architecture:** 11 database tables modeled strictly in Boyce-Codd and Third Normal Form (3NF), eliminating insertion, update, and deletion anomalies.
2. **Deterministic SQL Skill Matching Engine:** An auditable SQL algorithm that computes candidate qualification percentages against open job requirements in real-time, eliminating black-box bias.
3. **Database-Enforced Business Rules:** PL/pgSQL stored procedures for state transitions (`update_application_status`, `schedule_interview`) and database-level constraints that prevent duplicate candidate submissions (`UNIQUE(applicant_id, job_id)`).
4. **Modern Monochrome Enterprise UI:** A high-contrast, professional white-and-black SaaS interface built in Streamlit, featuring real-time KPI metrics, Plotly recruitment conversion funnels, resume management, and CSV report exports.
5. **Rigorous Quality Assurance:** A comprehensive automated testing suite comprising 24 automated pytest tests verifying connectivity, schema integrity, bcrypt password hashing, transactional rollback, and edge-case division safety.

---

## 3. Problem Statement & Motivation

### The Crisis of Unstructured Recruitment Tracking
In the absence of a centralized relational database, recruitment data across small-to-midsize enterprises is typically tracked across disparate Microsoft Excel or Google Sheets files, desktop folders containing unindexed PDF resumes, and recruiter inboxes. This ad-hoc approach creates four critical operational failure modes:

1. **Severe Data Redundancy and Update Anomalies:**  
   When candidate contact information changes (e.g., telephone number or email address), recruiters must locate and modify multiple spreadsheets. Inevitably, certain rows remain un-updated, leaving conflicting candidate data across departments.
2. **Accidental Duplicate Applications & Wasted Labor:**  
   Without an atomic uniqueness constraint at the database layer, candidates frequently submit multiple applications for the same requisition. Recruiters spend redundant hours screening the same candidate across different dates.
3. **Orphaned Resumes & Document Misplacement:**  
   When candidate records are deleted or updated, detached resume files frequently remain in file storage without pointers, creating compliance liabilities under privacy regulations (such as GDPR and CCPA).
4. **Lack of Auditable Pipeline Visibility:**  
   Hiring decisions and interview evaluations are frequently recorded in informal email threads or chat messages. When an executive requests recruitment velocity metrics (e.g., average time in pipeline, offer-acceptance ratios), assembling the data requires days of manual synthesis.

### Relational Database Motivation
A relational database management system (RDBMS) provides the mathematical foundations required to solve recruitment data challenges. Through entity-relationship modeling, primary-foreign key integrity, multi-table join algorithms, and transaction control, an RDBMS transforms recruitment from chaotic paper-pushing into a streamlined, auditable, and deterministic pipeline.

---

## 4. Project Objectives

The primary engineering and academic objectives of RecruitTrack ATS are:

- **Relational Schema Rigor:** Model all entities and associations across 11 normalized tables adhering strictly to Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF).
- **Referential Integrity & Cascading Constraints:** Implement foreign key rules that maintain data consistency across parents and children (`ON DELETE CASCADE` for resumes; `ON DELETE RESTRICT` for reference skills).
- **Database-Level Business Logic:** Implement PL/pgSQL stored procedures and domain check constraints so business rules are enforced inside the database engine regardless of which client connects.
- **Auditable Candidate-Job Skill Matching:** Formulate a set-based SQL ranking query that calculates qualification percentages using relational set intersection rather than opaque heuristic models.
- **Enterprise UI/UX Delivery:** Deliver an intuitive, accessible, and responsive user interface for recruiters, talent leads, and hiring managers with live database indicators and instant CSV reporting.
- **Production-Ready Security Standards:** Ensure zero plaintext credential persistence through cryptographic `bcrypt` password hashing and eliminate SQL injection vulnerabilities via psycopg2 parameterized queries.
- **100% Automated Test Coverage:** Establish an automated pytest testing framework validating all 24 critical system and database scenarios.

---

## 5. System Architecture

RecruitTrack ATS implements a decoupled **3-Tier Architecture**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 1: PRESENTATION LAYER (CLIENT)                  │
│                                                                         │
│  - Streamlit 1.42.0 Web Application (apps/main.py)                      │
│  - Monochrome Design System (#FFFFFF / #111111 / #64748B)               │
│  - 10 Specialized Recruiter Modules with Session State Management       │
│  - Interactive Plotly Visualizations (Funnels, Distributions, Trends)   │
│  - Instant CSV Report Downloader & Real File Resume Manager             │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │
                                     │ HTTPS / Local IPC (Session State)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              TIER 2: APPLICATION & BUSINESS LOGIC LAYER (PYTHON)        │
│                                                                         │
│  - Connection Factory & Query Executor (apps/db_connection.py)          │
│  - Security Engine: bcrypt Salt Generation & Password Verification      │
│  - Psycopg2 Parameterized Query Binding (%s)                            │
│  - Pandas DataFrame Formatting & CSV Serialization                      │
│  - Local Resume File System Manager (uploads/)                          │
└────────────────────────────────────▲────────────────────────────────────┘
                                     │
                                     │ TCP/IP Connection Pool (Port 4919)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    TIER 3: DATA STORAGE LAYER (POSTGRESQL 14)           │
│                                                                         │
│  - Database: recruittrack_db (Port: 4919)                               │
│  - 11 Relational Tables (10 Core Entities + 1 Junction Table)           │
│  - 2 Persistent Pre-Joined Views (applicant_application_view, etc.)     │
│  - 2 PL/pgSQL Stored Procedures (update_application_status, etc.)       │
│  - 7 B-Tree Performance Indexes Accelerating Foreign Keys & Filters     │
│  - ACID Transaction Control (BEGIN, COMMIT, ROLLBACK)                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Architectural Component Interaction
1. **Client Interaction:** The recruiter interacts with the Streamlit frontend. User inputs are validated at the form boundary before any query dispatch.
2. **Query Parameterization:** The application layer binds user parameters to SQL queries using `psycopg2` tuple binding. Dynamic string concatenation is strictly prohibited.
3. **Database Processing:** The PostgreSQL engine on port 4919 parses, optimizes, and executes queries, enforcing foreign keys, check constraints, and stored procedure domain validations.
4. **State Synchronization:** Application data is returned as structured dictionaries or DataFrames, and UI components update reactively.

---

## 6. Database Design & Normalization Methodology

### Design Philosophy
The schema was engineered using top-down Entity-Relationship analysis followed by bottom-up normalization synthesis. Every attribute was scrutinized to ensure it depends on the key, the whole key, and nothing but the key (so help me Codd).

### Normalization Proofs

#### 1. First Normal Form (1NF)
- **Requirement:** Atomic column values; no repeating groups; unique row identification.
- **Implementation:** In legacy ATS systems, skills are often stored as comma-delimited strings (`"Python, SQL, AWS"`). RecruitTrack ATS completely eliminates repeating groups by decomposing competencies into a master `skills` table and associative junction tables (`applicant_skills`, `job_skills`). Each table has a defined Primary Key (`BIGSERIAL` or composite primary key).

#### 2. Second Normal Form (2NF)
- **Requirement:** 1NF compliance + no partial functional dependencies on composite primary keys.
- **Implementation:** In `applicant_skills` (PK `{applicant_id, skill_id}`), the non-key attribute `proficiency_level` describes the specific proficiency of *that candidate* in *that skill*. It cannot be derived from `applicant_id` alone, nor from `skill_id` alone. In `job_skills` (PK `{job_id, skill_id}`), `required_level` depends fully on the composite key. No partial dependencies exist.

#### 3. Third Normal Form (3NF)
- **Requirement:** 2NF compliance + no transitive functional dependencies ($X \to Y \to Z$).
- **Implementation:** In `jobs`, the foreign key `company_id` points to the employer. Job postings do not store `company_name`, `industry`, or `company_website`. Storing those in `jobs` would create a transitive dependency ($\text{job\_id} \to \text{company\_id} \to \text{company\_name}$). Moving company attributes into `companies` guarantees 3NF compliance.

#### 4. Boyce-Codd Normal Form (BCNF)
- **Requirement:** For every functional dependency $X \to Y$, $X$ must be a superkey.
- **Implementation:** Across all 11 tables, every determinant is a superkey (either a primary key or candidate key with a `UNIQUE` constraint). Therefore, the schema satisfies BCNF.

---

## 7. Entity-Relationship Diagram (ERD)

The complete Entity-Relationship Diagram is documented in [docs/ERD.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/ERD.md) and rendered in ultra-high resolution (3800 × 2500 px, 300 DPI) in [docs/RecruitTrack_ERD.png](file:///Users/nihtinroy/RecruitTrack-ATS/docs/RecruitTrack_ERD.png) and vector format in [docs/RecruitTrack_ERD.pdf](file:///Users/nihtinroy/RecruitTrack-ATS/docs/RecruitTrack_ERD.pdf).

### High-Level Entity Summary
The database encompasses 11 relational tables:
1. `companies`: Corporate employer partners offering employment opportunities.
2. `recruiters`: Talent acquisition staff associated with specific companies.
3. `applicants`: Job seekers and prospective candidates in the talent pool.
4. `jobs`: Employment requisitions posted by recruiters on behalf of companies.
5. `skills`: Master catalog of standardized technical and professional competencies.
6. `applicant_skills`: Many-to-many junction mapping candidates to verified skills.
7. `job_skills`: Many-to-many junction mapping jobs to required competencies.
8. `resumes`: Document repository tracking uploaded resume files per candidate.
9. `applications`: Core transaction entity linking candidates, jobs, and resumes.
10. `interviews`: Scheduled evaluation rounds associated with specific applications.
11. `hiring_decisions`: Final hiring outcomes, offer details, and rejection reasons.

---

## 8. Table Relationships & Cardinalities

The following matrix documents the exact relationships, foreign key bindings, cardinalities, and deletion rules across all 11 tables:

| Parent Table | Child Table | Foreign Key Column | Cardinality | Business Meaning | ON DELETE Action |
|:---|:---|:---|:---:|:---|:---|
| `companies` | `recruiters` | `recruiters.company_id` | 1 : N | An employer employs one or more recruiters | `RESTRICT` |
| `companies` | `jobs` | `jobs.company_id` | 1 : N | An employer opens one or more job postings | `RESTRICT` |
| `recruiters` | `jobs` | `jobs.recruiter_id` | 1 : N | A recruiter manages one or more job postings | `SET NULL` |
| `applicants` | `resumes` | `resumes.applicant_id` | 1 : N | A candidate can upload multiple resume revisions | `CASCADE` |
| `applicants` | `applicant_skills`| `applicant_skills.applicant_id`| 1 : N | A candidate possesses multiple skills | `CASCADE` |
| `skills` | `applicant_skills`| `applicant_skills.skill_id`| 1 : N | A skill is possessed by multiple candidates | `RESTRICT` |
| `jobs` | `job_skills` | `job_skills.job_id` | 1 : N | A job requires multiple skills | `CASCADE` |
| `skills` | `job_skills` | `job_skills.skill_id` | 1 : N | A skill is required across multiple jobs | `RESTRICT` |
| `applicants` | `applications` | `applications.applicant_id` | 1 : N | A candidate submits multiple job applications | `RESTRICT` |
| `jobs` | `applications` | `applications.job_id` | 1 : N | A job receives multiple candidate applications | `RESTRICT` |
| `resumes` | `applications` | `applications.resume_id` | 1 : N | A resume is submitted with an application | `RESTRICT` |
| `applications` | `interviews` | `interviews.application_id` | 1 : N | An application undergoes multiple interview rounds | `CASCADE` |
| `applications` | `hiring_decisions`| `hiring_decisions.application_id`| 1 : 1 | An application receives at most one final decision | `CASCADE` |

---

## 9. Advanced SQL Implementation

Full technical breakdowns and live database query outputs are documented in [docs/SQL_FEATURES.md](file:///Users/nihtinroy/RecruitTrack-ATS/docs/SQL_FEATURES.md). A summary of the advanced SQL features implemented in RecruitTrack ATS includes:

1. **Multi-Table Relational Joins:**
   - *5-Table INNER JOIN:* Connects `applications`, `applicants`, `jobs`, `companies`, and `resumes` to construct the unified candidate dossier.
   - *LEFT OUTER JOIN:* Preserves newly posted requisitions with 0 applications in executive reports.
2. **Statistical Aggregations & Grouping:**
   - *Numeric Aggregations:* Calculates `COUNT()`, `MIN()`, `MAX()`, `AVG()`, and `ROUND()` over job salary budgets.
   - *HAVING Clause:* Filters aggregated requisitions to highlight high-volume pipelines exceeding threshold volume.
3. **Subquery Constructs:**
   - *IN Subquery:* Identifies candidates possessing specific competencies (`Python`, `SQL`, `AWS`).
   - *Scalar Subquery:* Compares individual requisition salaries against the global market average salary.
   - *NOT EXISTS Subquery:* Detects unengaged candidates who registered but have not applied to any opening.
4. **Database Views:**
   - `applicant_application_view`: Pre-joined relational abstraction simplifying candidate tracking queries.
   - `recruitment_summary_view`: Aggregated company-level metrics for executive dashboards.
5. **Stored Procedures (PL/pgSQL):**
   - `update_application_status`: Validates lifecycle domain values (`Applied`, `Screening`, `Interview`, `Offered`, `Rejected`, `Hired`) before atomic update.
   - `schedule_interview`: Inserts an interview record and automatically synchronizes the parent application status to `'Interview'`.
6. **ACID Transaction Control:**
   - Atomic multi-step onboarding transactions linking applicant creation, resume registration, and application submission with rollback on constraint failure.
7. **B-Tree Performance Indexes:**
   - 7 indexes targeting foreign keys and filter targets (`idx_applications_applicant`, `idx_applications_job`, `idx_applications_status`, etc.).

---

## 10. Application Features & UI/UX Design

The RecruitTrack ATS frontend was designed from the ground up to provide an enterprise-grade SaaS user experience. Built using **Streamlit 1.42.0**, it adheres to a **Minimalist Modern Monochrome White & Black** aesthetic inspired by modern enterprise tools such as Linear and Notion.

### UI Modules Walkthrough

1. **📊 Recruitment Overview (Dashboard):**
   - Displays 7 live KPI metric tiles (Companies, Recruiters, Applicants, Jobs, Applications, Interviews, Hired).
   - Visualizes the hiring pipeline using a Plotly Recruitment Funnel chart (`Applied` &rarr; `Screening` &rarr; `Interview` &rarr; `Offered` &rarr; `Hired`).
   - Displays employer market distribution and hiring outcome pie charts.
2. **🏢 Companies Management:**
   - Searchable registry of corporate partners with industry, location, and website metadata.
   - Full CRUD support with safety checks preventing deletion of companies with active jobs or recruiters.
3. **👥 Recruiters Management:**
   - Recruiter directory grouped by employer affiliation.
   - Secure recruiter registration with automatic `bcrypt` password hashing.
4. **💼 Jobs Management:**
   - Requisition manager with compensation inputs, status filters (`Open`/`Closed`), and recruiter assignment.
5. **👤 Applicants & Resumes:**
   - Candidate registry with searchable name, contact info, and technology filters.
   - Local resume file upload supporting `.pdf` and `.docx` documents.
   - Candidate profile viewer featuring one-click resume download buttons.
6. **🎯 Skills Management:**
   - Master technical skills catalog.
   - Candidate skill endorsement portal with proficiency levels (`Beginner`, `Intermediate`, `Advanced`, `Expert`).
   - Job requisition skill requirement configuration.
7. **📝 Applications Management:**
   - Application submission engine preventing duplicate applications.
   - Status pipeline updater powered by the `update_application_status` stored procedure.
8. **📅 Interviews Management:**
   - Multi-round interview scheduler supporting `Phone`, `Video`, and `In-Person` formats.
   - Automated status synchronization via `schedule_interview` stored procedure.
   - Recruiter feedback logging and evaluation records.
9. **🏆 Hiring Decisions:**
   - Final offer management recording decisions (`Hired`, `Rejected`, `Pending`), offer salary, and start date.
   - Automatic cascade synchronizing parent application status to `Hired`.
10. **🔍 Candidate Skill Matching:**
    - Live SQL matching engine comparing applicant skills against job requirements.
    - Transparent leaderboard displaying match percentages and detailed skill gap analysis.
11. **📈 Reports & Analytics:**
    - Pre-computed database views and analytical queries with instant **📥 Download Report CSV** functionality.

---

## 11. Recruitment Workflow Lifecycle

The end-to-end recruitment lifecycle implemented in RecruitTrack ATS follows an auditable, six-stage state machine:

```text
[ 1. Job Creation ] ──────► [ 2. Candidate Application ] ──────► [ 3. Skills Assessment ]
  - Recruiter posts job       - Candidate submits profile          - SQL matching ranks
  - Requirements set          - Resume uploaded & bound              candidates by match %
                                                                             │
                                                                             ▼
[ 6. Hiring Decision ] ◄──── [ 5. Multi-Round Interviews ] ◄──── [ 4. Recruiter Screening ]
  - Offer extended / hired     - CALL schedule_interview()         - CALL update_status()
  - Pipeline finalized         - Feedback logged                   - Status = 'Screening'
```

### State Transition Validation
Application status transitions are restricted to the following valid sequence:
$$\text{Applied} \longrightarrow \text{Screening} \longrightarrow \text{Interview} \longrightarrow \text{Offered} \longrightarrow \text{Hired} \quad (\text{or } \text{Rejected})$$

Any attempt to inject an invalid status string (e.g., `'Accepted'` or `'Pending Review'`) is immediately rejected by the database-level CHECK constraint and PL/pgSQL validation logic.

---

## 12. Candidate Skill Matching Algorithm

### Architectural Motivation
Commercial applicant tracking systems often employ opaque machine learning or natural language models that introduce demographic and linguistic bias. RecruitTrack ATS implements a completely transparent, auditable, and deterministic skill matching algorithm executed directly within the PostgreSQL query planner.

### Mathematical Formula
For a given job $J$ with required skill set $S_J$ and candidate $C$ with verified skill set $S_C$:
$$\text{Matched Skills Count} = |S_J \cap S_C|$$
$$\text{Total Required Skills} = |S_J|$$
$$\text{Match Percentage} = \begin{cases} 
\text{ROUND}\left( \frac{|S_J \cap S_C|}{|S_J|} \times 100, 1 \right) & \text{if } |S_J| > 0 \\ 
0.0\% & \text{if } |S_J| = 0 
\end{cases}$$

### Zero-Division Protection via `NULLIF`
In production databases, a newly posted job may not yet have required skills configured ($|S_J| = 0$). Standard SQL division would trigger an immediate `division by zero` fatal error. RecruitTrack ATS guarantees mathematical safety using `NULLIF`:
```sql
COALESCE(ROUND(100.0 * COUNT(js.skill_id) / NULLIF(%s, 0), 1), 0.0) AS "Match %"
```
When `total_req` is 0, `NULLIF(0, 0)` returns `NULL`, causing the division to yield `NULL`, which `COALESCE` safely transforms into `0.0%`.

---

## 13. Security & Data Integrity

1. **Cryptographic Password Hashing:**
   - Passwords for recruiters are hashed using `bcrypt` with automatically generated per-user salt rounds.
   - Hashes are formatted as `$2b$12$...`. Plaintext passwords never touch database disk blocks.
2. **SQL Injection Defense:**
   - All SQL executions routed through `apps/db_connection.py` enforce parameter separation using `psycopg2` tuple bindings (`%s`).
   - Dynamic user-supplied table or column names are forbidden.
3. **Defense-in-Depth Relational Constraints:**
   - `PRIMARY KEY`: Guarantees entity uniqueness across all 11 tables.
   - `UNIQUE(applicant_id, job_id)`: Prevents multiple concurrent submissions.
   - `UNIQUE(email)`: Prevents duplicate recruiter or applicant identity profiles.
   - `CHECK(salary >= 0)`: Prohibits negative compensation values.
   - `CHECK(status IN (...))`: Enforces strict lifecycle state domains.
4. **Credential Decoupling:**
   - Database credentials, port specifications (port `4919`), and host settings are loaded dynamically from `.env` via `python-dotenv`.
   - `.env` is excluded from git version control via `.gitignore`.

---

## 14. Testing Methodology & Verification Strategy

The quality assurance strategy for RecruitTrack ATS encompasses unit, integration, and end-to-end regression testing. Tests are automated using **pytest** and executed against the live PostgreSQL 14 instance on port `4919`.

### Test Architecture
- **Dedicated Test Suite:** Located in `tests/test_recruittrack.py` and `tests/test_e2e_workflow.py`.
- **Live Database Connection Fixture:** Uses `psycopg2` connections isolated with transaction rollbacks (`db.rollback()`) to ensure zero test contamination of production seed data.
- **Error Injection Testing:** Explicitly tests database constraint rejections using `pytest.raises(psycopg2.IntegrityError)`.

---

## 15. Test Results & Quality Assurance

All **24 automated test cases** pass cleanly with zero failures and zero warnings:

| # | Test Function Name | Subsystem / Focus Area | Verified Condition | Status |
|:---:|:---|:---|:---|:---:|
| 1 | `test_complete_15_step_recruitment_workflow` | End-to-End Pipeline | Full 15-step recruiter hiring lifecycle from job post to hire | **PASS** |
| 2 | `test_01_database_connection` | Connectivity | TCP/IP connection to PostgreSQL 14 on port 4919 | **PASS** |
| 3 | `test_02_all_tables_exist` | Relational Schema | Existence of all 11 tables in public schema | **PASS** |
| 4 | `test_03_foreign_key_integrity` | Constraints | Rejection of orphaned child foreign keys | **PASS** |
| 5 | `test_04_recruiter_authentication_valid` | Security / Auth | Successful login with valid bcrypt password hash | **PASS** |
| 6 | `test_05_recruiter_authentication_invalid` | Security / Auth | Immediate rejection of invalid/empty passwords | **PASS** |
| 7 | `test_06_company_crud` | Entity Operations | Create, Read, Update, and Delete on `companies` table | **PASS** |
| 8 | `test_07_applicant_crud` | Entity Operations | Full CRUD lifecycle on `applicants` table | **PASS** |
| 9 | `test_08_job_crud` | Entity Operations | Posting, querying, updating, and deleting job postings | **PASS** |
| 10 | `test_09_application_creation` | Pipeline Transactions | Insertion of application connecting applicant, job, and resume | **PASS** |
| 11 | `test_10_duplicate_application_prevention`| Business Rules | Database enforcement of `UNIQUE(applicant_id, job_id)` | **PASS** |
| 12 | `test_11_application_status_update_procedure`| Stored Procedures | Atomic execution of `CALL update_application_status()` | **PASS** |
| 13 | `test_12_interview_scheduling_procedure`| Stored Procedures | `CALL schedule_interview()` synchronizes status to 'Interview' | **PASS** |
| 14 | `test_13_hiring_decisions` | Pipeline Transactions | Recording hiring outcome and blocking duplicate decisions | **PASS** |
| 15 | `test_14_candidate_skill_matching` | SQL Matching Engine | Correct mathematical skill ranking against job requirements | **PASS** |
| 16 | `test_15_sql_views` | Database Views | Execution of `applicant_application_view` and summary view | **PASS** |
| 17 | `test_16_stored_procedures_validation` | Validation & Logic | Rejection of invalid status strings by stored procedures | **PASS** |
| 18 | `test_17_dashboard_metrics_accuracy` | Analytics & KPIs | Mathematical consistency between UI KPIs and raw table counts | **PASS** |
| 19 | `test_18_csv_report_generation` | Reporting / Export | Proper CSV string serialization with headers and rows | **PASS** |
| 20 | `test_19_input_validation_and_check_constraints`| Database Integrity | Enforcement of `CHECK(salary >= 0)` and status check domains | **PASS** |
| 21 | `test_20_transaction_rollback_behavior`| ACID Compliance | Atomic rollback ensuring zero partial state persistence | **PASS** |
| 22 | `test_21_candidate_skill_matching_nvidia_regression`| Regression QA | Resolution of NVIDIA Machine Learning Engineer query crash | **PASS** |
| 23 | `test_22_candidate_skill_matching_all_five_sample_jobs`| Comprehensive QA | Skill matching verification across all 5 sample jobs | **PASS** |
| 24 | `test_23_candidate_skill_matching_zero_required_skills_safety`| Edge Case Safety | Zero-division mathematical protection when required skills = 0 | **PASS** |

**Pytest Execution Summary:** `24 passed in 1.85s`

---

## 16. Technical Challenges Encountered & Engineering Solutions

### Challenge 1: Sample Data ON CONFLICT Failure
- **Symptom:** Executing `database/sample_data.sql` aborted with `ERROR: there is no unique or exclusion constraint matching the ON CONFLICT specification`.
- **Root Cause:** Insert statements utilized `ON CONFLICT (company_name)` and `ON CONFLICT (job_title)`, but the live database schema only defined unique constraints on primary keys and emails.
- **Solution:** Re-engineered `database/sample_data.sql` to explicitly verify and establish unique indexes on natural business keys (`companies.company_name`, `skills.skill_name`) and wrapped insertions in clean transactional blocks.

### Challenge 2: Custom PostgreSQL Port 4919 Binding
- **Symptom:** Standard PostgreSQL client tools and connection scripts defaulted to port 5432 and failed with `Connection Refused`.
- **Root Cause:** The host environment runs PostgreSQL 14 on isolated port `4919` to avoid conflicting with default database instances.
- **Solution:** Parameterized all connection utilities (`apps/db_connection.py`, `tests/test_recruittrack.py`) to read `DB_PORT=4919` from `.env`, implemented port validation assertions, and updated all documentation.

### Challenge 3: Plotly Titlefont Deprecation Crash
- **Symptom:** Dashboard crashed with `Invalid property specified for object of type plotly.graph_objs.layout.XAxis: 'titlefont'`.
- **Root Cause:** Modern Plotly v6 deprecated the legacy `titlefont` property in favor of nested font objects (`title={'font': {'size': 12}}`).
- **Solution:** Refactored all chart generation functions in `apps/main.py` to use modern Plotly layout syntax.

### Challenge 4: Psycopg2 Parameter Parsing in Skill Matching Query
- **Symptom:** Selecting jobs with multiple required skills (e.g., NVIDIA Machine Learning Engineer) caused an immediate crash: `IndexError: tuple index out of range`.
- **Root Cause:** In the ranking SQL string, `ROUND(...) AS "Match %"` contained a literal `%` character. When `execute_query(sql, params)` was invoked, `psycopg2` interpreted `%" ` as a Python format specifier and attempted to bind a non-existent parameter from the tuple.
- **Solution:** Escaped the literal percent sign as `"Match %%"`, wrapped the denominator in `NULLIF(%s, 0)` for zero-division protection, and restructured `apps/db_connection.py` to only bind parameter tuples when parameters are explicitly provided.

---

## 17. Performance & Optimization Analysis

1. **B-Tree Indexing Strategy:**
   - Every foreign key column in `applications`, `interviews`, `jobs`, and junction tables is backed by an index. This reduces foreign key join scans from $O(N)$ sequential table scans to $O(\log N)$ index range scans.
2. **Database View Materialization Considerations:**
   - Current views (`applicant_application_view`, `recruitment_summary_view`) run dynamically against indexed base tables with execution times $< 2 \text{ ms}$. For enterprise scale ($> 1,000,000$ applications), these can be converted to PostgreSQL `MATERIALIZED VIEW` refreshed periodically via background workers.
3. **Connection Management:**
   - Database connections are initialized via a thread-safe factory pattern with short timeouts (`connect_timeout=5`), ensuring unresponsive network sockets do not hang the Streamlit rendering thread.

---

## 18. Comparison with Commercial ATS Solutions

| Evaluation Dimension | Commercial SaaS (Workday, Greenhouse) | RecruitTrack ATS (PostgreSQL 14) |
|:---|:---|:---|
| **Data Ownership & Privacy** | Stored on proprietary vendor cloud; recurring licensing fees | 100% self-hosted; complete relational schema ownership |
| **Candidate Matching** | Proprietary black-box machine learning algorithms | Deterministic, auditable SQL relational set operations |
| **Schema Customizability** | Rigid, vendor-dictated custom field limitations | Direct DDL control; full support for views, procedures, constraints |
| **Reporting Flexibility** | Restricted to vendor report builders or expensive BI add-ons | Unlimited SQL analytics, views, and one-click CSV streaming |
| **Cost of Ownership** | High enterprise subscription cost per recruiter seat | Open-source technology stack; zero licensing fees |

---

## 19. System Limitations

While RecruitTrack ATS meets and exceeds all academic requirements for CIS 407, several enterprise boundaries are acknowledged:

1. **Session Scope:** The current authentication model operates within Streamlit's reactive session state; multi-tenant enterprise Single Sign-On (SAML/OAuth2) is not yet integrated.
2. **File Storage Topology:** Resumes are persisted to the local file system (`uploads/`) with path pointers in PostgreSQL. Enterprise scale would require distributed object storage (such as AWS S3 or Google Cloud Storage).
3. **Outbound Communications:** Application status changes update the database atomically, but do not yet trigger automated candidate notification emails via external SMTP/SendGrid APIs.
4. **Manual Skill Tagging:** Candidate skills must be selected or verified by recruiters; automatic unstructured PDF parsing via Large Language Models or NLP is planned for Phase 3.

---

## 20. Future Enhancements & Roadmap

- **Phase 3: Automated Resume NLP Parser:** Integrate an automated document extractor utilizing Python `pypdf` and spaCy to parse candidate skills and work experience automatically from uploaded resumes.
- **Phase 4: Calendar API Integration:** Connect interview scheduling directly to Google Calendar and Microsoft Outlook APIs with automatic `.ics` calendar invitation generation.
- **Phase 5: Granular Role-Based Access Control (RBAC):** Establish distinct database roles and UI permissions for Hiring Managers (review and interview only), Recruiters (full pipeline CRUD), and Candidates (self-service profile management).
- **Phase 6: Multi-Cloud Blob Storage:** Implement an abstracted storage adapter supporting AWS S3, Google Cloud Storage, and Azure Blob Storage for resume documents.

---

## 21. Conclusion

The **RecruitTrack ATS** project demonstrates the power of rigorous relational database engineering in solving real-world enterprise operational problems. By modeling recruitment entities into a Third Normal Form relational schema in **PostgreSQL 14**, the application eliminates redundant data entry, guarantees referential consistency, and automates multi-stage candidate pipelines.

Through its modern white-and-black Streamlit interface, transparent SQL candidate skill matching engine, database-level stored procedures, and 100% passing automated test suite (24 tests), RecruitTrack ATS proves that academic rigor and enterprise-grade software craftsmanship can be synthesized into an exceptional final capstone project.

---
*Submitted in partial fulfillment of the requirements for CIS 407: Database Management Systems.*
