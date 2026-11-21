# RecruitTrack ATS — Comprehensive Relational Database Design & Architecture

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Database Engine:** PostgreSQL 14.24 (`recruittrack_db`)  
**Network Endpoint:** `localhost:4919`  
**Relational Architecture:** 11 Tables | 3NF Normalized | ACID-Compliant  

---

## 1. Executive Summary & Design Philosophy

RecruitTrack ATS is an enterprise-grade recruitment and applicant tracking database system developed to manage candidate talent pools, multi-tenant employer requisitions, technical competency evaluations, interview schedules, and hiring decisions.

The database design adheres to the following core database engineering principles:
1. **Third Normal Form (3NF) Compliance:** Elimination of redundancy, insertion anomalies, update anomalies, and deletion anomalies.
2. **Strict Domain & Referential Integrity:** Mandatory primary keys, foreign key constraints, domain-level `CHECK` constraints, and composite uniqueness rules.
3. **Transparent Mathematical Scoring:** Dynamic SQL-based candidate ranking using junction tables (`applicant_skills`, `job_skills`) without opaque machine learning or unexplainable heuristics.
4. **Tenant Data Isolation:** Structural scoping linking recruiters, job requisitions, applications, and decisions to employer companies (`companies`).

---

## 2. Comprehensive Data Dictionary (All 11 Tables)

Below is the complete data dictionary extracted directly from the live PostgreSQL 14 `information_schema` catalogs.

### Table 1: `companies`
- **Purpose:** Represents employer organizations (clients or internal business units) that post job openings and employ recruiters.
- **Physical Table Name:** `public.companies`
- **Primary Key:** `company_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `company_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique surrogate identifier for the organization. |
| `company_name` | `VARCHAR(150)` | **NO** | *None* | `NOT NULL` | Registered corporate name of the employer. |
| `industry` | `VARCHAR(100)` | YES | *None* | *None* | Primary business domain (e.g., Financial Technology, Cloud Infrastructure). |
| `location` | `VARCHAR(150)` | YES | *None* | *None* | Corporate headquarters city and state/country. |
| `website` | `VARCHAR(255)` | YES | *None* | *None* | Official corporate website URL link. |

---

### Table 2: `recruiters`
- **Purpose:** Stores authenticated talent acquisition personnel and hiring managers associated with specific employer companies.
- **Physical Table Name:** `public.recruiters`
- **Primary Key:** `recruiter_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `recruiter_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique recruiter identifier. |
| `company_id` | `INT` | **NO** | *None* | **FK** &rarr; `companies.company_id` | Foreign key establishing organizational employment. |
| `full_name` | `VARCHAR(150)` | **NO** | *None* | `NOT NULL` | Full professional name of the recruiter. |
| `email` | `VARCHAR(150)` | **NO** | *None* | **UK**, `NOT NULL` | Corporate email address used as the unique authentication identity. |
| `password_hash` | `VARCHAR(255)` | **NO** | *None* | `NOT NULL` | One-way cryptographic salt-and-hashed password (bcrypt). |

---

### Table 3: `applicants`
- **Purpose:** Master repository of candidate profiles seeking employment opportunities.
- **Physical Table Name:** `public.applicants`
- **Primary Key:** `applicant_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `applicant_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique candidate identity number. |
| `full_name` | `VARCHAR(150)` | **NO** | *None* | `NOT NULL` | Full legal name of the candidate. |
| `email` | `VARCHAR(150)` | **NO** | *None* | **UK**, `NOT NULL` | Candidate email address, guaranteed unique across the platform. |
| `phone` | `VARCHAR(20)` | YES | *None* | *None* | Primary contact telephone number. |
| `location` | `VARCHAR(150)` | YES | *None* | *None* | Candidate geographic residence (city, state, region). |

---

### Table 4: `jobs`
- **Purpose:** Stores open and closed employment requisitions created by recruiters on behalf of employer organizations.
- **Physical Table Name:** `public.jobs`
- **Primary Key:** `job_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `job_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique requisition tracking identifier. |
| `company_id` | `INT` | **NO** | *None* | **FK** &rarr; `companies.company_id` | Organization offering the position. |
| `recruiter_id` | `INT` | **NO** | *None* | **FK** &rarr; `recruiters.recruiter_id` | Hiring manager owning the requisition. |
| `job_title` | `VARCHAR(150)` | **NO** | *None* | `NOT NULL` | Position title (e.g., Senior Systems Architect). |
| `description` | `TEXT` | YES | *None* | *None* | Comprehensive role duties and qualification narrative. |
| `location` | `VARCHAR(150)` | YES | *None* | *None* | Geographic workplace or Remote/Hybrid specification. |
| `salary` | `NUMERIC` | YES | *None* | `CHECK (salary >= 0)` | Annual compensation in USD; non-negative domain check. |
| `posted_date` | `DATE` | YES | `CURRENT_DATE` | *None* | Date requisition was published. |
| `status` | `VARCHAR(20)` | YES | `'Open'` | `CHECK (status IN ('Open', 'Closed'))` | Lifecycle state of requisition. |

---

### Table 5: `skills`
- **Purpose:** Master standardized catalog of technical, domain, and soft competencies.
- **Physical Table Name:** `public.skills`
- **Primary Key:** `skill_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `skill_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Standardized skill identifier. |
| `skill_name` | `VARCHAR(100)` | **NO** | *None* | **UK**, `NOT NULL` | Distinct competency name (e.g., Python, Docker, SQL, LangChain). |

---

### Table 6: `applicant_skills` (Junction Table)
- **Purpose:** Resolves the Many-to-Many ($M:N$) relationship between `applicants` and `skills`, tracking endorsed competencies and proficiency levels.
- **Physical Table Name:** `public.applicant_skills`
- **Primary Key:** Composite `{applicant_id, skill_id}` (`pk_applicant_skills`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `applicant_id` | `INT` | **NO** | *None* | **PK**, **FK** &rarr; `applicants.applicant_id` | Candidate holding the competency. |
| `skill_id` | `INT` | **NO** | *None* | **PK**, **FK** &rarr; `skills.skill_id` | Competency possessed by the candidate. |
| `proficiency_level` | `VARCHAR(30)` | YES | *None* | `CHECK (proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert'))` | Endorsed capability depth. |

---

### Table 7: `job_skills` (Junction Table)
- **Purpose:** Resolves the Many-to-Many ($M:N$) relationship between `jobs` and `skills`, defining required competencies and expected minimum mastery.
- **Physical Table Name:** `public.job_skills`
- **Primary Key:** Composite `{job_id, skill_id}` (`pk_job_skills`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `job_id` | `INT` | **NO** | *None* | **PK**, **FK** &rarr; `jobs.job_id` `ON DELETE CASCADE` | Job requisition mandating the competency. |
| `skill_id` | `INT` | **NO** | *None* | **PK**, **FK** &rarr; `skills.skill_id` `ON DELETE RESTRICT` | Required standardized competency. |
| `required_level` | `VARCHAR(30)` | YES | `'Intermediate'` | `CHECK (required_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert'))` | Minimum expected candidate proficiency. |

---

### Table 8: `resumes`
- **Purpose:** Tracks binary document files uploaded on behalf of candidates.
- **Physical Table Name:** `public.resumes`
- **Primary Key:** `resume_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `resume_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique document identifier. |
| `applicant_id` | `INT` | **NO** | *None* | **FK** &rarr; `applicants.applicant_id` `ON DELETE CASCADE` | Candidate who owns the resume file. |
| `file_name` | `VARCHAR(255)` | **NO** | *None* | `NOT NULL` | Uploaded document filename (e.g., `alex_carter_resume.pdf`). |
| `file_path` | `VARCHAR(500)` | **NO** | *None* | `NOT NULL` | Relative path to local file storage (`uploads/resumes/...`). |
| `uploaded_date` | `DATE` | YES | `CURRENT_DATE` | *None* | Timestamp when file was registered. |

---

### Table 9: `applications` (Central Junction & Pipeline Entity)
- **Purpose:** Core recruitment transaction entity linking an applicant, a job requisition, and a specific verified resume.
- **Physical Table Name:** `public.applications`
- **Primary Key:** `application_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `application_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique application tracking record. |
| `applicant_id` | `INT` | **NO** | *None* | **FK** &rarr; `applicants.applicant_id` | Submitting candidate. |
| `job_id` | `INT` | **NO** | *None* | **FK** &rarr; `jobs.job_id` | Target job requisition. |
| `resume_id` | `INT` | **NO** | *None* | **FK** &rarr; `resumes.resume_id` | Submitted resume version. |
| `applied_date` | `DATE` | YES | `CURRENT_DATE` | *None* | Submission date. |
| `status` | `VARCHAR(30)` | YES | `'Applied'` | `CHECK (status IN ('Applied', 'Screening', 'Interview', 'Offered', 'Rejected', 'Hired'))` | Current lifecycle stage. |

> **Critical Constraint:** `UNIQUE (applicant_id, job_id)` prevents an applicant from submitting duplicate applications for the same job requisition.

---

### Table 10: `interviews`
- **Purpose:** Tracks sequential interview stages, evaluation feedback, and interview statuses for an application.
- **Physical Table Name:** `public.interviews`
- **Primary Key:** `interview_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `interview_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique interview event identifier. |
| `application_id` | `INT` | **NO** | *None* | **FK** &rarr; `applications.application_id` | Parent application being evaluated. |
| `interview_date` | `TIMESTAMP` | **NO** | *None* | `NOT NULL` | Exact date and time of scheduled session. |
| `interview_type` | `VARCHAR(30)` | YES | *None* | `CHECK (interview_type IN ('Phone', 'Video', 'In-Person'))` | Interview format. |
| `feedback` | `TEXT` | YES | *None* | *None* | Recruiter/evaluator interview notes and technical rating. |
| `status` | `VARCHAR(30)` | YES | `'Scheduled'` | `CHECK (status IN ('Scheduled', 'Completed', 'Cancelled'))` | Interview completion state. |

---

### Table 11: `hiring_decisions`
- **Purpose:** Records the final outcome, decision audit date, and offer terms concluding an application.
- **Physical Table Name:** `public.hiring_decisions`
- **Primary Key:** `decision_id` (Surrogate, auto-incrementing `SERIAL`)

| Column Name | Data Type | Nullable | Default | Constraints | Description |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `decision_id` | `INT` (SERIAL) | **NO** | `nextval(...)` | **PK** | Unique decision outcome record. |
| `application_id` | `INT` | **NO** | *None* | **UK**, **FK** &rarr; `applications.application_id` | Evaluated application record. |
| `decision` | `VARCHAR(30)` | **NO** | *None* | `CHECK (decision IN ('Hired', 'Rejected', 'Pending'))` | Final outcome determination. |
| `decision_date` | `DATE` | YES | `CURRENT_DATE` | *None* | Audit timestamp of formal decision. |
| `remarks` | `TEXT` | YES | *None* | *None* | Offer compensation terms, start date, or decline reasoning. |

> **Critical Constraint:** `UNIQUE (application_id)` enforces a strict One-to-One ($1:1$) relationship ensuring an application can conclude with at most one final hiring decision.

---

## 3. Database Normalization Analysis (1NF, 2NF, 3NF, BCNF)

The schema was constructed through formal normalization up to Third Normal Form (3NF) and Boyce-Codd Normal Form (BCNF) to eliminate operational anomalies.

```
+-------------------------------------------------------------------------------------------------+
|                                 NORMALIZATION PROGRESSION                                       |
+-------------------------------------------------------------------------------------------------+
|  [UNNORMALIZED]                                                                                 |
|  Single table containing company info, job info, applicant info, comma-separated skills         |
|  --> Anomaly: Updating company headquarters requires modifying 1,000 application rows.        |
+-------------------------------------------------------------------------------------------------+
|  [FIRST NORMAL FORM (1NF)]                                                                      |
|  - All attribute values are strictly atomic (no comma-delimited strings).                       |
|  - Each table has a defined primary key.                                                        |
|  - Competencies split into distinct rows in applicant_skills and job_skills.                    |
+-------------------------------------------------------------------------------------------------+
|  [SECOND NORMAL FORM (2NF)]                                                                     |
|  - Satisfies 1NF.                                                                               |
|  - No partial key dependencies exist in composite-key junction tables.                          |
|    In applicant_skills {applicant_id, skill_id} -> proficiency_level depends on BOTH.           |
|    In job_skills {job_id, skill_id} -> required_level depends on BOTH.                          |
+-------------------------------------------------------------------------------------------------+
|  [THIRD NORMAL FORM (3NF) & BCNF]                                                               |
|  - Satisfies 2NF.                                                                               |
|  - Zero transitive dependencies (X -> Y and Y -> Z).                                            |
|    Non-key attributes depend exclusively on the candidate key:                                  |
|    applications -> applicant_id (not applicant phone/email directly).                           |
|    jobs -> company_id (not company headquarters directly).                                      |
|  - Every determinant is a superkey (BCNF compliant).                                            |
+-------------------------------------------------------------------------------------------------+
```

### Anomaly Elimination Proofs:

1. **Insertion Anomaly Prevention:**
   - In a non-normalized structure, a new skill cannot be entered without an applicant possessing it. In RecruitTrack ATS, master competencies are entered independently into `skills`.
   - A client company can be registered in `companies` before posting any job requisitions.
2. **Update Anomaly Prevention:**
   - If an employer changes headquarters or corporate website, only one record in `companies` is updated. All existing job requisitions dynamically reflect the change via foreign key join.
   - If a candidate updates their telephone number, only `applicants` is modified; historical applications and interview notes remain untouched and accurate.
3. **Deletion Anomaly Prevention:**
   - Deleting a closed job requisition does not delete the client company or the recruiter profile.
   - Removing an applicant's resume document does not delete the candidate's core identity in `applicants`.

---

## 4. Architectural Analysis of Junction Tables

RecruitTrack ATS implements three critical junction tables to maintain relational integrity:

### 1. `applicant_skills` (Candidate Competency Inventory)
- **Cardinality:** Many-to-Many ($M:N$) between `applicants` and `skills`.
- **Composite Primary Key:** `{applicant_id, skill_id}`.
- **Attributes:** `proficiency_level` (`Beginner`, `Intermediate`, `Advanced`, `Expert`).
- **Relational Role:** Allows a candidate to possess multiple technical competencies while allowing each standardized skill to be endorsed across thousands of candidates.

### 2. `job_skills` (Requisition Requirement Specification)
- **Cardinality:** Many-to-Many ($M:N$) between `jobs` and `skills`.
- **Composite Primary Key:** `{job_id, skill_id}`.
- **Attributes:** `required_level` (`Beginner`, `Intermediate`, `Advanced`, `Expert`).
- **Relational Role:** Enables hiring teams to map multiple competencies with required minimum levels to a job opening. Serves as the mathematical benchmark for the Candidate Skill Matching algorithm.

### 3. `applications` (Recruitment Pipeline Hub)
- **Cardinality:** Many-to-Many ($M:N$) between `applicants` and `jobs`, with a Foreign Key to `resumes`.
- **Surrogate Key:** `application_id`.
- **Natural Composite Unique Key:** `{applicant_id, job_id}`.
- **Relational Role:** Connects the candidate, the job posting, and the submitted resume version while serving as the parent entity for downstream interview evaluations (`interviews`) and formal employment outcomes (`hiring_decisions`).

---

## 5. Database Views & Stored Procedures

### Production Views:
1. **`applicant_application_view`**:
   Consolidates candidate names, corporate emails, target position titles, employer company names, applied dates, and current pipeline stages across 4 tables for operational dashboards.
2. **`recruitment_summary_view`**:
   Aggregates total posted job requisitions and total application volumes per employer organization, preserving zero-activity employers.

### Production Stored Procedures:
1. **`update_application_status(p_application_id, p_new_status)`**:
   Validates domain stage transitions (`Applied`, `Screening`, `Interview`, `Offered`, `Rejected`, `Hired`) and updates application state within a managed transaction.
2. **`schedule_interview(p_application_id, p_interview_date, p_interview_type, p_feedback)`**:
   Inserts a new scheduled interview record and automatically synchronizes the parent application status to `'Interview'`.
