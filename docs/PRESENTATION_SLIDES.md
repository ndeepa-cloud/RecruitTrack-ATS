# RecruitTrack ATS — 9-Slide Presentation Guide

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Academic Term:** Spring 2026  
**Presentation Format:** 9-Slide Presentation Deck + Live System Walkthrough (5–7 Minutes Total)  
**Live Application URL:** `http://localhost:8501`  
**GitHub Repository:** `https://github.com/ndeepa-cloud/RecruitTrack-ATS`  
**Database:** PostgreSQL 14 (Port **4919** / Database: `recruittrack_db`)  

---

## 🎯 Alignment with CIS 407 Grading Rubric

This 9-slide presentation is structured to systematically address all eight rubric categories in order:

| Slide # | Slide Title | Rubric Category Addressed |
|:---:|:---|:---|
| **Slide 1** | Title, Academic Context & Executive Overview | Cat. 7 (Documentation), Cat. 1 (Requirements) |
| **Slide 2** | Business Problem, Motivation & Domain Rules | Cat. 1 (Requirements & Business Rules) |
| **Slide 3** | Relational Database Design, 3NF & ER Diagram | Cat. 1 (Database Design: ERD, Schema, Normalization) |
| **Slide 4** | Database Implementation: 11 Tables & Constraints | Cat. 2 (Implementation: Data Types, PK/FK/CHECK) |
| **Slide 5** | Core SQL Capabilities: CRUD, Joins & Aggregations | Cat. 3 (SQL Queries: SELECT, INSERT, UPDATE, DELETE) |
| **Slide 6** | Advanced Database Features: Procedures, Views & ACID | Cat. 5 (Advanced: PL/pgSQL, Views, Transactions) |
| **Slide 7** | Python & Streamlit UI: Architecture, Search & Forms | Cat. 4 (Python App & UI: Connected, Forms, Search) |
| **Slide 8** | Testing, Error Handling & 24 Automated Tests | Cat. 6 (Testing & Functionality: 24/24 Tests Passing) |
| **Slide 9** | Live Demonstration Roadmap & Conclusion | Cat. 8 (Presentation & Demonstration Walkthrough) |

---

## Slide 1: Title, Academic Context & Executive Overview
- **Header:** RecruitTrack ATS — Job Recruitment & Applicant Tracking System
- **Subtitle:** Enterprise Relational Data Engineering in PostgreSQL 14 & Streamlit
- **Presenter Info:** Student / Engineering Lead | CIS 407 Database Management Systems | Spring 2026
- **Key Points:**
  - Modern full-stack recruitment platform replacing fragmented spreadsheets with an ACID-compliant relational system.
  - End-to-end talent lifecycle: Employer onboarding &rarr; Job posting &rarr; Resume uploading &rarr; Candidate skill matching &rarr; Interview scheduling &rarr; Auditable hiring decisions.
  - **Technology Stack:** PostgreSQL 14 (Port 4919), Python 3.13, Streamlit 1.42, psycopg2, Pandas, Plotly, bcrypt, pytest.
- **Speaker Notes:**
  *"Good morning professor and evaluation panel. Today I am presenting RecruitTrack ATS, an enterprise-grade applicant tracking database system developed for CIS 407. Our goal was to demonstrate how foundational database theory—normalization, referential integrity, stored procedures, and set-based SQL algorithms—can transform recruitment operations into an auditable, high-performance data platform."*

---

## Slide 2: Business Problem, Motivation & Domain Rules
- **Header:** Business Problem & Domain Requirements
- **Key Challenges in Talent Acquisition:**
  - **Data Silos:** Candidate details, resumes, and interview feedback scattered across unlinked spreadsheets and email inboxes.
  - **Data Inconsistencies & Duplicates:** Lack of uniqueness constraints allows candidates to apply multiple times for the same job, wasting screening labor.
  - **Orphaned Resumes:** Document files stored without strict foreign key cascade rules, creating compliance and privacy liabilities.
  - **Opaque Candidate Ranking:** Reliance on black-box AI keyword parsers that lack mathematical transparency.
- **Core Domain Business Rules:**
  - An applicant must own the resume attached to an application (`UNIQUE(resume_id, applicant_id)` + composite foreign key).
  - An applicant cannot apply twice for the same requisition (`UNIQUE(applicant_id, job_id)`).
  - A recruiter must belong to the hiring company (`UNIQUE(recruiter_id, company_id)`).
  - Salaries must be strictly non-negative (`CHECK(salary >= 0)`).
  - Application lifecycle follows an explicit state machine: `Applied` &rarr; `Screening` &rarr; `Interview` &rarr; `Offered` &rarr; `Hired` (or `Rejected`).
- **Speaker Notes:**
  *"We began by analyzing the operational failures of legacy recruitment workflows: duplicate submissions, detached resume files, and lack of audit trails. To solve these, we established strict domain business rules at the database level rather than trusting the frontend."*

---

## Slide 3: Relational Database Design, 3NF & ER Diagram
- **Header:** Database Design: Relational Schema & 3NF Normalization
- **Entity-Relationship Overview:**
  - **11 Normalized Tables:** 10 core entities + 1 extension junction table (`job_skills`).
  - **Cardinalities:**
    - 1:1 (`applications` &rarr; `hiring_decisions`)
    - 1:N (`companies` &rarr; `jobs`, `companies` &rarr; `recruiters`, `applicants` &rarr; `resumes`, `jobs` &rarr; `applications`, `applications` &rarr; `interviews`)
    - M:N (`applicants` &harr; `skills` via `applicant_skills`, `jobs` &harr; `skills` via `job_skills`)
- **Normalization Proofs:**
  - **1NF:** Atomic attributes; multi-valued skills decomposed into junction tables.
  - **2NF:** No partial key dependencies; composite PK attributes in junction tables depend on the full composite key.
  - **3NF & BCNF:** Zero transitive dependencies ($X \to Y \to Z$); every determinant is a candidate superkey.
- **Visual Artifacts:** High-resolution 3800x2500 px ER diagram (`docs/RecruitTrack_ERD.png`) and vector PDF (`docs/RecruitTrack_ERD.pdf`).
- **Speaker Notes:**
  *"Here is our Entity-Relationship Diagram. We modeled 11 normalized tables adhering strictly to Boyce-Codd and Third Normal Form. Notice our junction tables for skills: instead of comma-separated strings, we use applicant_skills and job_skills to enable relational set operations."*

---

## Slide 4: Database Implementation: 11 Tables & Constraints
- **Header:** Database Implementation in PostgreSQL 14 (Port 4919)
- **Table Catalog & Data Types:**
  - `companies`, `recruiters`, `applicants`, `jobs`, `skills`, `applicant_skills`, `job_skills`, `resumes`, `applications`, `interviews`, `hiring_decisions`.
  - Typed with `SERIAL`, `INT`, `VARCHAR`, `TEXT`, `DECIMAL(12,2)`, `DATE`, `TIMESTAMP`.
- **Integrity Constraints & Defense-in-Depth:**
  - **Primary Keys:** Explicit PK on all 11 tables.
  - **Foreign Keys:** Enforced across all relationships with explicit `ON DELETE CASCADE` (for child resumes/interviews) and `ON DELETE RESTRICT` (for master reference entities).
  - **Domain CHECK Constraints:** Validating salary non-negativity, proficiency levels, and lifecycle status domains.
  - **Uniqueness Constraints:** Preventing duplicate emails, duplicate company names, and duplicate candidate submissions.
- **Meaningful Sample Data:**
  - Comprehensive seed data in `database/sample_data.sql`: 5 enterprise companies, 5 recruiters (with valid bcrypt hash), 10 candidates, 5 jobs, 10 skills, 10 resumes, 10 applications, 5 interviews, 3 decisions. All fictional identities.
- **Speaker Notes:**
  *"Our implementation runs on PostgreSQL 14 on port 4919. We enforced defense-in-depth: every relationship has foreign key cascades or restrictions, and domain check constraints ensure that invalid data can never be committed."*

---

## Slide 5: Core SQL Capabilities: CRUD, Joins & Aggregations
- **Header:** SQL Query Implementation: Full CRUD, Joins & Aggregations
- **Complete CRUD Operations:**
  - **SELECT:** Over 40 parameterized queries powering dashboards, pipeline tables, and candidate filters.
  - **INSERT:** Verified across companies, recruiters, jobs, applicants, skills, applications, interviews, and decisions.
  - **UPDATE:** Safe editing for company profiles, recruiter data, job statuses (`Open`/`Closed`), and application states.
  - **DELETE:** Referentially guarded deletions for companies; cascading teardown demonstrated in `queries.sql` and test suites.
- **Multi-Table Relational JOINs:**
  - **5-Table INNER JOIN:** Connects `applications`, `applicants`, `jobs`, `companies`, and `resumes` for the unified applicant dossier.
  - **LEFT OUTER JOIN:** Preserves brand-new job postings with 0 applications in executive reports.
- **Statistical Aggregations & Subqueries:**
  - `COUNT()`, `MIN()`, `MAX()`, `ROUND(AVG(), 2)` compensation benchmarks.
  - `HAVING COUNT(application_id) > 1` filtering high-volume funnels.
  - `IN`, `Scalar`, and `NOT EXISTS` subqueries isolating qualified candidates and identifying unengaged talent.
- **Speaker Notes:**
  *"In our SQL implementation, we demonstrate full CRUD capabilities. We utilize 5-table inner joins to synthesize candidate dossiers, left outer joins to prevent zero-applicant postings from dropping out of reports, and statistical aggregations with HAVING clauses."*

---

## Slide 6: Advanced Database Features: Procedures, Views & ACID
- **Header:** Advanced Database Features & Deterministic Skill Matching
- **Stored Procedures (PL/pgSQL):**
  - `CALL update_application_status(aid, new_status)`: Validates lifecycle domain values before atomic update.
  - `CALL schedule_interview(aid, date, type, notes)`: Inserts interview round and automatically synchronizes application status to `'Interview'`.
- **Persistent Database Views:**
  - `applicant_application_view`: Pre-joined relational abstraction for candidate tracking.
  - `recruitment_summary_view`: Aggregated company-level metrics for executive dashboards.
- **Performance B-Tree Indexes:**
  - 7 indexes accelerating foreign key navigation, status filtering, and date queries.
- **Transparent SQL Candidate Skill Matching:**
  - Set-intersection query calculating exact mathematical match percentages:
    $$\text{Match \%} = \text{ROUND}\left( \frac{\text{Candidate Matched Skills}}{\text{Job Required Skills}} \times 100, 1 \right)$$
  - Equipped with `NULLIF(total_req, 0)` for zero-division mathematical safety.
- **ACID Transaction Guarantees:** Multi-table onboarding operations wrapped in atomic `BEGIN`, `COMMIT`, `ROLLBACK` blocks.
- **Speaker Notes:**
  *"For advanced features, we implemented PL/pgSQL stored procedures that enforce business rules directly inside the engine. Our views simplify reporting queries, and our SQL skill matching query uses set intersection with NULLIF division-by-zero protection to rank candidates with 100% mathematical transparency."*

---

## Slide 7: Python & Streamlit UI: Architecture, Search & Forms
- **Header:** Python Application Architecture & Modern Streamlit Interface
- **3-Tier Architecture:**
  - **Presentation Layer:** Modern monochrome white & black SaaS UI inspired by Linear and Notion (`apps/main.py`).
  - **Application / Logic Layer:** Thread-safe connection factory, bcrypt authentication engine, query parameterization (`apps/db_connection.py`).
  - **Data Storage Layer:** PostgreSQL 14 on port 4919 (`recruittrack_db`).
- **11 Specialized Modules with Full Search & Filtering:**
  - Real-time search inputs across Companies, Recruiters, Jobs, Applicants, Applications, Interviews, and Decisions.
  - Dropdown filters for Industry, Employer, Job Status, Skill proficiency, and Pipeline stage.
- **Interactive Visualizations & File Handling:**
  - Plotly recruitment conversion funnel (`Applied` &rarr; `Screening` &rarr; `Interview` &rarr; `Offered` &rarr; `Hired`).
  - Real file resume uploader supporting `.pdf` and `.docx` with one-click download buttons.
  - Instant CSV report generation across all analytical views.
- **Speaker Notes:**
  *"Our Python interface is built using Streamlit with a clean, professional monochrome design. It features 11 dedicated modules, real-time keyword search and dropdown filtering, interactive Plotly funnel charts, real resume file downloads, and instant CSV exports."*

---

## Slide 8: Testing, Error Handling & 24 Automated Tests
- **Header:** Quality Assurance, Robust Error Handling & Automated Testing
- **Comprehensive 24-Test Automated Suite (`pytest`):**
  - **Connectivity & Schema:** Database connectivity on port 4919, 11-table existence, foreign key integrity violations.
  - **Security & Authentication:** Bcrypt password hashing validation and rejection of invalid passwords.
  - **CRUD Operations:** Company, Applicant, and Job lifecycle operations.
  - **Business Logic & Stored Procedures:** Application status updates, interview scheduling, hiring decision uniqueness.
  - **Skill Matching & Regression Safety:** NVIDIA ML Engineer query parsing, 5-job ranking verification, zero-required-skills division safety.
  - **ACID & Rollback:** Transaction rollback verification ensuring zero state contamination.
  - **End-to-End Workflow:** 15-step recruiter hiring lifecycle from job posting to CSV export.
- **Test Results:** **24 passed in 2.75 seconds** with zero failures.
- **Speaker Notes:**
  *"Reliability is paramount. We built an automated test suite of 24 pytest tests that validate every database constraint, stored procedure, CRUD operation, and security boundary. Every test passes in under 3 seconds, and tests run within isolated transactions so sample data is never contaminated."*

---

## Slide 9: Live Demonstration Roadmap & Conclusion
- **Header:** Live Demonstration Roadmap & Project Conclusion
- **5-Minute Demonstration Flow (`docs/DEMO_GUIDE.md`):**
  1. *System Health & Auth (1 min):* Sidebar PostgreSQL indicator, bcrypt login as Sarah Johnson (Google).
  2. *Executive Dashboard (45 sec):* 7 live KPI counters, Plotly recruitment conversion funnel.
  3. *Candidate Registration & Resume Upload (1 min):* Add candidate, upload `.pdf` resume, download file.
  4. *Skills & Transparent Matching (1.5 min):* Select NVIDIA ML Engineer, view mathematical match leaderboard and skill gap breakdown.
  5. *Application & Stored Procedures (1 min):* Submit application (duplicate prevention demo), execute `CALL update_application_status(...)`.
  6. *Interviews & Hiring (45 sec):* Schedule interview round, record `Hired` decision, observe live dashboard update.
  7. *Exportable Reports & Test Run (30 sec):* Export CSV report, run 24 automated tests in terminal.
- **Conclusion:** RecruitTrack ATS proves how foundational relational database engineering delivers an enterprise-grade talent acquisition platform.
- **Thank You:** Questions & Discussion.
- **Speaker Notes:**
  *"Now we will transition directly to our live demonstration following the 7-step walkthrough in our Demo Guide. Thank you, and I look forward to your questions."*
