# RecruitTrack ATS — Step-by-Step Demonstration Guide

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Target Audience:** Course Instructor, Evaluator, Demo Presentation Grading Panel  
**Estimated Presentation Time:** 5 – 7 Minutes  
**Live Application URL:** `http://localhost:8501`  
**Database Engine:** PostgreSQL 14 (Port **4919** / Database: `recruittrack_db`)  

---

## 📋 Pre-Presentation Setup Checklist

Before presenting to your instructor or grading panel, ensure the following steps are complete:
1. **Verify PostgreSQL 14 is running on Port 4919:**
   ```bash
   /Library/PostgreSQL/14/bin/pg_ctl -D /Library/PostgreSQL/14/data status
   ```
2. **Activate the Virtual Environment & Launch Streamlit:**
   ```bash
   source .venv/bin/activate
   .venv/bin/streamlit run apps/main.py
   ```
3. **Open Application in Browser:** Navigate to `http://localhost:8501`.
4. **Have Terminal Ready for Test Execution:** Keep a second terminal open to run pytest on demand.

---

## ⏱️ 5-Minute Demonstration Script

### Step 1: System Health & Recruiter Authentication (1 Minute)
1. **Point to Sidebar Connection Indicator:**
   - Highlight the green indicator: **PostgreSQL 14 Connected** (`localhost:4919 / recruittrack_db`).
   - Explain that the database runs on dedicated port `4919` with decoupled `.env` configuration.
2. **Sign In as Demo Recruiter:**
   - Under the **Recruiter Access** box, enter:
     - **Email:** `sarah.johnson@example.com`
     - **Password:** `DemoRecruiter2026!`
   - Click **Sign In**.
   - **Key Academic Talking Point:** Explain that the database verifies the password against a cryptographic `bcrypt` hash (`$2b$12$...`), with zero plaintext credentials stored.
   - Point out that the session updates with Sarah Johnson's initials avatar and corporate affiliation (`Google`).

---

### Step 2: Executive Dashboard & Analytics (45 Seconds)
1. **Highlight the 7 Real-Time Metric Tiles:**
   - Point to Companies, Recruiters, Applicants, Jobs, Applications, Interviews, and Hired counts.
2. **Demonstrate the Recruitment Conversion Funnel:**
   - Point to the Plotly funnel chart showing pipeline flow:
     $$\text{Applied} \longrightarrow \text{Screening} \longrightarrow \text{Interview} \longrightarrow \text{Offered} \longrightarrow \text{Hired}$$
3. **Key Academic Talking Point:** Explain that these metrics are computed live using SQL aggregate queries (`COUNT()`, `COUNT(DISTINCT)`) without stale cached data.

---

### Step 3: Candidate Registration & Real File Resume Upload (1 Minute)
1. **Navigate to:** **👤 Applicants & Resumes** &rarr; **Register New Applicant**.
2. **Enter Candidate Details:**
   - **Full Name:** `Jordan Rivera`
   - **Email:** `jordan.rivera@demo.edu`
   - **Phone:** `555-0188`
   - **Location:** `Austin, TX`
   - **Upload Resume:** Attach any sample `.pdf` or `.docx` file from your computer.
3. **Click Register Applicant:**
   - Point out the confirmation message showing candidate and resume creation.
4. **Demonstrate File Retrieval:**
   - Switch to **Candidate Profile & Resumes**.
   - Select `Jordan Rivera` and click **📥 Download Resume**.
   - Show that the actual uploaded file is retrieved directly from local storage (`uploads/`).
5. **Key Academic Talking Point:** Explain that the `resumes` table stores metadata and file paths with an `ON DELETE CASCADE` constraint linked to `applicants`.

---

### Step 4: Skills Assignment & Candidate Skill Matching (1.5 Minutes)
1. **Navigate to:** **🎯 Skills Management** &rarr; **Assign Candidate Skills**.
   - Assign `Python` (`Expert`) and `Docker` (`Advanced`) to `Jordan Rivera`.
2. **Navigate to:** **🔍 Candidate Skill Matching**.
3. **Select Open Requisition:** Choose `Machine Learning Engineer @ NVIDIA`.
4. **Highlight the SQL Matching Engine:**
   - Show the dynamic candidate leaderboard with exact mathematical match percentages:
     $$\text{Match Percentage} = \text{ROUND}\left( \frac{\text{Candidate Matched Skills}}{\text{Job Required Skills}} \times 100, 1 \right)$$
   - Show that `Jordan Rivera` is ranked with matched competencies (✅ `Python`, ✅ `Docker`) and missing requirements (❌ `Machine Learning`).
5. **Key Academic Talking Point:** Emphasize that this is not an opaque AI black box—it is a deterministic SQL set-intersection query powered by `job_skills` and `applicant_skills` junction tables, equipped with `NULLIF(..., 0)` to prevent division-by-zero errors.

---

### Step 5: Application Submission & Stored Procedure Execution (1 Minute)
1. **Navigate to:** **📝 Applications Management** &rarr; **Submit Application**.
   - Select `Jordan Rivera`, `Machine Learning Engineer @ NVIDIA`, and Jordan's resume.
   - Click **Submit Application**.
2. **Demonstrate Duplicate Prevention:**
   - Attempt to submit the exact same combination again.
   - Show that PostgreSQL rejects the duplicate submission via the database-level `UNIQUE(applicant_id, job_id)` constraint.
3. **Execute Stored Procedure Status Update:**
   - Switch to the **Update Status** tab.
   - Select Jordan's application and advance the status to `Screening`.
   - **Key Academic Talking Point:** Explain that this executes `CALL update_application_status(?, 'Screening')` inside PostgreSQL with domain validation logic.

---

### Step 6: Interview Scheduling & Hiring Decision (45 Seconds)
1. **Navigate to:** **📅 Interviews Management** &rarr; **Schedule New Interview**.
   - Select Jordan's application, choose tomorrow's date, format `Video`, and click **Schedule Interview**.
   - Explain that `CALL schedule_interview(...)` automatically updated the parent application status to `'Interview'`.
2. **Navigate to:** **🏆 Hiring Decisions** &rarr; **Record Decision**.
   - Select Jordan's application, choose `Hired`, enter salary `$135,000`, and submit.
3. **Verify Live Dashboard Synchronization:**
   - Return to **📊 Recruitment Overview** (Dashboard).
   - Point out that the **Hired** metric tile has incremented live!

---

### Step 7: Exportable Audit Reports & Test Suite (30 Seconds)
1. **Navigate to:** **📈 Reports & Analytics**.
   - Select **Company Recruitment Summary** or **Compensation Benchmarks**.
   - Click **📥 Download Report CSV** to demonstrate instant CSV export.
   - Point out that these reports are powered by underlying database views (`recruitment_summary_view`, `applicant_application_view`).
2. **Run the 24 Automated Tests in Terminal:**
   ```bash
   .venv/bin/pytest tests/ -v
   ```
   - Show the grading panel all 24 tests passing in under 2 seconds:
     ```text
     ============================== 24 passed in 1.85s ==============================
     ```

---

## 🎯 Summary of Key Academic Talking Points

| Concept | Implementation in RecruitTrack ATS |
|:---|:---|
| **Normalization** | 11 tables strictly adhering to 3NF and BCNF, eliminating redundancy |
| **Referential Integrity** | Primary keys, foreign keys, and cascading delete rules (`ON DELETE CASCADE` / `RESTRICT`) |
| **Advanced SQL** | 5-table INNER JOINs, LEFT JOINs preserving zero-application jobs, HAVING clauses, IN/NOT EXISTS subqueries |
| **Stored Procedures** | PL/pgSQL routines (`update_application_status`, `schedule_interview`) with domain validation |
| **ACID Transactions** | Multi-table atomic onboarding transactions with full rollback on error |
| **Security** | `bcrypt` cryptographic password hashing and `psycopg2` parameterized queries |
| **Automated Testing** | 24 automated pytest tests covering all CRUD, constraints, auth, and regression scenarios |
