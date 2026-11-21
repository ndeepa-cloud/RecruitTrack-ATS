# RecruitTrack ATS — Job Recruitment & Applicant Tracking System

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.24-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Tests-24%20Passing-success?logo=pytest&logoColor=white)](https://pytest.org/)
[![License](https://img.shields.io/badge/Academic-CIS%20407-blue)](#academic-context)

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Database:** PostgreSQL 14 (Port **4919** / Database: `recruittrack_db`)  
**Backend:** Python 3.13 (`psycopg2`, `bcrypt`, `pandas`)  
**Frontend:** Streamlit Modern Monochrome SaaS UI (`apps/main.py`)  

---

## 📋 Executive Overview

**RecruitTrack ATS** is an enterprise-grade recruitment and applicant tracking database system developed for **CIS 407 (Database Management Systems)**. It replaces fragmented spreadsheets and ad-hoc email chains with a fully normalized, ACID-compliant relational data platform and an interactive Streamlit dashboard.

The system manages the entire talent acquisition lifecycle: corporate employer partner onboarding, recruiter credential management, job requisition posting, candidate profile indexing, real file resume uploads, application pipeline tracking, multi-round interview scheduling, auditable hiring decisions, and an automated SQL-driven candidate skill matching engine.

---

## 🎯 Business Problem & Solution

### The Business Problem
Recruitment teams face significant operational friction when tracking candidate pipelines across disparate tools:
- **Data Fragmentation & Inconsistency:** Candidate contact details, resumes, and interview feedback get scattered across emails, spreadsheets, and shared drives.
- **Accidental Duplicate Applications:** Candidates apply multiple times for the same job, leading to redundant screening rounds and recruiter confusion.
- **Unverified Candidate Matching:** Recruiters spend excessive manual hours cross-referencing required job competencies against candidate skill sets.
- **Data Integrity Failures:** Manual record keeping lacks foreign key constraints, resulting in orphaned resumes, invalid pipeline statuses, and uncoordinated interview scheduling.

### The RecruitTrack Solution
RecruitTrack ATS solves these challenges through strict database-driven relational integrity and a modern recruiter web portal:
1. **Third Normal Form (3NF) Relational Architecture:** 11 normalized tables eliminate redundancy and prevent insert/update/delete anomalies.
2. **Database-Level Integrity Constraints:** Unique constraints prevent duplicate submissions (`UNIQUE(applicant_id, job_id)`), check constraints enforce domain values, and cascade rules protect against orphaned files.
3. **Transparent SQL Skill Matching Engine:** Ranks candidates against job requirements mathematically using set-based SQL joins without opaque black-box AI.
4. **Stored Procedure Pipeline Advancement:** State transitions (`Applied` &rarr; `Screening` &rarr; `Interview` &rarr; `Offered` &rarr; `Hired`) execute through PL/pgSQL stored procedures with full domain validation.
5. **Secure Authentication & Data Layer:** Industry-standard bcrypt password hashing, parameter-bound SQL queries preventing injection, and decoupled environment configurations.

---

## 🏗️ System Architecture

RecruitTrack ATS follows a modular **3-Tier Architecture**:

```text
┌─────────────────────────────────────────────────────────────┐
│             PRESENTATION LAYER (STREAMLIT UI)               │
│  Modern Monochrome White & Black SaaS Interface             │
│  Interactive KPIs, Plotly Visualizations, Recruiter Forms   │
└──────────────────────────────▲──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│           APPLICATION & BUSINESS LOGIC LAYER (PYTHON)       │
│  apps/main.py (Page Routing & View Rendering)               │
│  apps/db_connection.py (Connection Pool & Safe SQL Binding) │
│  Security Layer (Bcrypt Hashing, Session Management)        │
└──────────────────────────────▲──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│         DATA STORAGE LAYER (POSTGRESQL 14 @ PORT 4919)      │
│  11 Normalized Relational Tables (10 Core + 1 Junction)     │
│  Database Views (Reporting & Pipeline Aggregations)         │
│  Stored Procedures (PL/pgSQL Business Logic)                │
│  B-Tree Performance Indexes & ACID Transactions             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Complete Technology Stack

| Component | Technology | Version | Purpose |
|:---|:---|:---|:---|
| **Database Engine** | PostgreSQL | 14.24 | Relational schema, ACID transactions, stored procedures, views, indexes |
| **Database Port** | TCP/IP Port | **4919** | Isolated PostgreSQL instance port (configured to prevent standard 5432 conflicts) |
| **Backend Language** | Python | 3.13 | Core business logic, data wrangling, and pipeline execution |
| **Database Driver** | psycopg2-binary | 2.9.10 | Low-level PostgreSQL adapter with parameterized query binding |
| **Frontend Framework** | Streamlit | 1.42.0 | Responsive web interface, form validation, and reactive session state |
| **Data Analytics** | Pandas | 2.2.3 | Tabular data manipulation, query result formatting, and CSV report export |
| **Data Visualization**| Plotly | 6.0.0 | Interactive pipeline conversion funnels, salary distribution charts |
| **Security & Auth** | bcrypt | 4.3.0 | Secure password salt generation and cryptographic verification |
| **Automated Testing** | pytest | 8.3.4 | Automated validation suite covering 24 comprehensive database test cases |
| **Configuration** | python-dotenv | 1.0.1 | Secure environment variable injection from `.env` |

---

## 📁 Project Directory Structure

```text
RecruitTrack-ATS/
├── .env                       # Local environment configuration (DB credentials & port 4919)
├── .env.example               # Template environment configuration
├── requirements.txt           # Python dependency definitions
├── README.md                  # Root project documentation (this file)
│
├── apps/                      # Application Layer
│   ├── __init__.py
│   ├── db_connection.py       # Thread-safe PostgreSQL connection factory & query executor
│   └── main.py                # Streamlit web application & multi-page UI router
│
├── database/                  # Database Layer DDL & DML
│   ├── schema.sql             # 11-table DDL, foreign keys, constraints, views & procedures
│   ├── sample_data.sql        # Realistic seed data for employers, applicants, skills & jobs
│   └── queries.sql            # Complex queries, multi-table joins, subqueries & aggregations
│
├── docs/                      # Comprehensive University & Technical Documentation
│   ├── ERD.md                 # Mermaid ER diagram, relationship cardinalities & catalog
│   ├── RecruitTrack_ERD.png   # High-resolution (3800x2500 px, 300 DPI) visual ER diagram
│   ├── RecruitTrack_ERD.pdf   # Vector PDF edition of the Entity-Relationship Diagram
│   ├── DATABASE_DESIGN.md     # 11-table data dictionaries, constraints & 3NF proofs
│   ├── SQL_FEATURES.md        # Advanced SQL queries, joins, subqueries, views & verified outputs
│   ├── FINAL_PROJECT_REPORT.md# Complete 21-section university academic final report
│   ├── USER_GUIDE.md          # Step-by-step recruiter user manual
│   ├── DEMO_GUIDE.md          # 5-minute presentation demonstration walkthrough script
│   └── TESTING.md             # Test strategy, execution guide & test case inventory
│
├── scripts/                   # Utility Scripts
│   └── generate_erd_diagram.py# Pillow-based visual ERD generator rendering high-res diagram
│
├── tests/                     # Automated QA & Testing Suite
│   ├── __init__.py
│   └── test_recruittrack.py   # 24 automated pytest test cases validating live DB operations
│
└── uploads/                   # Local secure repository for candidate resume documents
```

---

## 🚀 Setup & Installation Guide

### 1. Prerequisites
- **macOS / Linux / Windows**
- **Python 3.10+** (Python 3.13 recommended)
- **PostgreSQL 14** running on **Port 4919**

---

### 2. Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
Ensure your `.env` contains your active PostgreSQL instance settings:
```ini
DB_HOST=localhost
DB_PORT=4919
DB_NAME=recruittrack_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```
> [!IMPORTANT]
> RecruitTrack ATS connects to PostgreSQL on **Port 4919**. Ensure your database service is listening on port 4919, not the default port 5432.

---

### 3. Virtual Environment Setup
```bash
# Create isolated Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Database Initialization
Initialize the database schema, views, stored procedures, and initial seed data:
```bash
# Execute DDL schema creation
/Library/PostgreSQL/14/bin/psql -h localhost -p 4919 -U postgres -d recruittrack_db -v ON_ERROR_STOP=1 -f database/schema.sql

# Seed initial demonstration data
/Library/PostgreSQL/14/bin/psql -h localhost -p 4919 -U postgres -d recruittrack_db -v ON_ERROR_STOP=1 -f database/sample_data.sql
```

---

### 5. Launching the Streamlit Application
Start the interactive recruiter web application:
```bash
.venv/bin/streamlit run apps/main.py
```
Access the application in your browser at:  
👉 **`http://localhost:8501`**

---

### 6. Executing Automated Test Suite
Run the 24 automated unit and integration tests:
```bash
.venv/bin/pytest tests/ -v
```
**Expected Test Output:**
```text
============================== 24 passed in 2.35s ==============================
```

---

## 🔑 Pre-Configured Recruiter Demo Account

For university evaluators and demo presentations, a pre-configured recruiter account is available:

| Field | Value |
|:---|:---|
| **Email** | `sarah.johnson@example.com` |
| **Password** | `DemoRecruiter2026!` |
| **Affiliation** | Google (Lead Technical Recruiter) |

---

## 📑 Documentation Index

Comprehensive academic and engineering documentation is provided in the `docs/` directory:

| Document | Description | Format |
|:---|:---|:---:|
| [**docs/ERD.md**](docs/ERD.md) | Mermaid ER diagram, relationship cardinality matrix & schema catalog | Markdown |
| [**docs/RecruitTrack_ERD.png**](docs/RecruitTrack_ERD.png) | High-Resolution 300 DPI Visual Diagram (3800 × 2500 px) | Image |
| [**docs/RecruitTrack_ERD.pdf**](docs/RecruitTrack_ERD.pdf) | High-Resolution Print-Ready Vector PDF Edition | PDF |
| [**docs/DATABASE_DESIGN.md**](docs/DATABASE_DESIGN.md) | Complete 11-table data dictionary, 3NF normalization proofs & integrity constraints | Markdown |
| [**docs/SQL_FEATURES.md**](docs/SQL_FEATURES.md) | Advanced SQL queries, joins, subqueries, views, procedures & verified live outputs | Markdown |
| [**docs/FINAL_PROJECT_REPORT.md**](docs/FINAL_PROJECT_REPORT.md) | Complete 21-section university academic final project report | Markdown |
| [**docs/USER_GUIDE.md**](docs/USER_GUIDE.md) | Step-by-step recruiter user manual covering all 10 application modules | Markdown |
| [**docs/DEMO_GUIDE.md**](docs/DEMO_GUIDE.md) | 5-minute presentation demonstration script for course grading | Markdown |
| [**docs/TESTING.md**](docs/TESTING.md) | Quality assurance test strategy, test matrix & verification results | Markdown |

---

## 🔒 Security & Data Integrity

- **Password Hashing:** Recruiter credentials are never stored in plaintext. Passwords are salted and hashed using `bcrypt` prior to database persistence.
- **SQL Injection Prevention:** Every query executed through `apps/db_connection.py` utilizes `psycopg2` parameterized queries (`%s`), strictly preventing SQL injection vulnerabilities.
- **Credential Isolation:** Database credentials and secrets are managed exclusively through local environment variables (`.env`) excluded from version control via `.gitignore`.
- **Relational Integrity:** Cascading deletes (`ON DELETE CASCADE`) are restricted strictly to child documents (`resumes`), while master entities enforce referential blocks (`ON DELETE RESTRICT`) to prevent accidental data loss.

---

## ⚖️ Known Limitations & Future Roadmap

### Current Limitations
1. **Single Recruiter Active Session:** Recruiter login is handled via Streamlit session state; multi-tenant enterprise Single Sign-On (SSO) is not yet implemented.
2. **Local Resume Storage:** Resumes are saved to the local `uploads/` directory rather than distributed cloud blob storage (AWS S3 / Google Cloud Storage).
3. **No Direct Email Notifications:** System logs status changes to the database without outbound SMTP email triggers.

### Future Roadmap
- **Resume NLP Parsing:** Automated entity extraction parsing candidate PDF resumes directly into skills and experience profiles.
- **Calendar Synchronization:** Integration with Google Calendar and Microsoft Outlook APIs for real-time interview scheduling.
- **Granular RBAC:** Distinct permission tiers for Hiring Managers, Recruiters, and Candidate self-service portals.
- **Cloud Blob Storage:** Automated S3 bucket synchronization for candidate attachment durability.

---

## 🎓 Academic Context
- **Course:** CIS 407 — Database Management Systems
- **Term:** Spring 2026
- **System:** RecruitTrack ATS
