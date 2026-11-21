# RecruitTrack ATS — Recruiter User Guide & Operations Manual

**Course:** CIS 407 — Database Management Systems  
**Project:** RecruitTrack ATS (Job Recruitment and Applicant Tracking System)  
**Target Audience:** Recruiters, Talent Acquisition Leads, Hiring Managers, Course Evaluators  
**Application URL:** `http://localhost:8501`  
**Database Engine:** PostgreSQL 14 (Port `4919` / Database: `recruittrack_db`)  

---

## 1. System Access & Authentication

### 1.1 Launching the Application
1. Ensure your local PostgreSQL 14 service is running on **Port 4919**.
2. Activate your virtual environment and start the Streamlit server:
   ```bash
   source .venv/bin/activate
   .venv/bin/streamlit run apps/main.py
   ```
3. Open your browser and navigate to **`http://localhost:8501`**.

### 1.2 Verifying Database Connectivity
Observe the left sidebar indicator:
- **🟢 Connected:** Indicates a live, authenticated connection to PostgreSQL 14 on port `4919` (`recruittrack_db`).
- **🔴 Disconnected:** Check that PostgreSQL is running on port 4919 and that credentials in `.env` are accurate.

### 1.3 Recruiter Authentication
Under the **Recruiter Access** box in the left sidebar:
1. Enter your registered email:
   - **Demo Recruiter:** `sarah.johnson@example.com`
2. Enter your password:
   - **Demo Password:** `DemoRecruiter2026!`
3. Click **Sign In**.
4. Once verified against the database `bcrypt` hash, your recruiter badge, employer affiliation (e.g., `Google`), and initials avatar will appear in the top-left sidebar.

---

## 2. Navigating Core Modules

The left navigation sidebar provides access to all 11 specialized recruitment modules:

---

### 📊 Module 1: Recruitment Overview (Dashboard)
- **Executive Metric Cards:** Real-time counters showing total counts for Companies, Recruiters, Applicants, Jobs, Applications, Interviews, and Hired Candidates.
- **Recruitment Conversion Funnel:** Visualizes pipeline flow from initial application to final hire:
  $$\text{Applied} \longrightarrow \text{Screening} \longrightarrow \text{Interview} \longrightarrow \text{Offered} \longrightarrow \text{Hired}$$
- **Employer Distribution:** Chart displaying job requisitions and candidate volume grouped by employer.
- **Hiring Outcomes:** Visual breakdown of offers accepted, rejected, and pending.

---

### 🏢 Module 2: Companies Management
- **Search & Filter:** Search employers by company name, industry sector (e.g., AI, Cloud, E-commerce), or headquarters city.
- **Add Employer:** Register a new corporate client by providing Company Name, Industry, City/State Location, and Official Website URL.
- **Safety Deletion Guard:** The system prevents deleting companies with active job requisitions or affiliated recruiters to preserve relational integrity.

---

### 👥 Module 3: Recruiters Management
- **Recruiter Directory:** Review all talent acquisition specialists grouped by their corporate employer.
- **Onboard New Recruiter:** Enter the recruiter's Full Name, Corporate Email, and assign them to an employer company.
- **Cryptographic Security:** Set an initial password; the system automatically salts and hashes the password using `bcrypt` before storing it in PostgreSQL.

---

### 💼 Module 4: Jobs Management
- **Requisition Directory:** Browse open and closed jobs with compensation budgets and assigned recruiters.
- **Filter by Company & Status:** Filter job postings by specific employer (e.g., Google, Microsoft, NVIDIA) and toggle between `Open` and `Closed` requisitions.
- **Post New Job:** Enter Job Title, Minimum Annual Salary (validated by `CHECK(salary >= 0)`), Work Location (e.g., Remote, San Francisco, CA), Job Description, and assign an affiliated recruiter.
- **Close Requisition:** Update job status to `Closed` when an open position has been filled.

---

### 👤 Module 5: Applicants & Resumes
- **Candidate Registry:** Browse all registered candidates with full contact details and geographic locations.
- **Skill Filter:** Filter candidates possessing specific competencies (e.g., show all candidates skilled in `Python` or `Docker`).
- **Register Candidate:** Enter Candidate Name, Email, Phone Number, and Location.
- **Real File Resume Upload:** Attach a resume in `.pdf` or `.docx` format. The file is safely stored in `uploads/` and indexed in the `resumes` table.
- **One-Click Resume Download:** In the **Candidate Profile & Resumes** tab, click the **📥 Download Resume** button to retrieve the actual uploaded file.

---

### 🎯 Module 6: Skills Management
- **Master Competencies Catalog:** Review standardized technical skills (e.g., Python, SQL, React, AWS, Docker) or create new competencies.
- **Candidate Endorsements:** Assign skills to candidates with proficiency levels:
  - `Beginner`
  - `Intermediate`
  - `Advanced`
  - `Expert`
- **Job Requirements:** Configure required skills and minimum proficiency levels for each job requisition to enable automated candidate matching.

---

### 📝 Module 7: Applications Management
- **Submit Application:**
  1. Select a Candidate from the talent pool.
  2. Select an Open Job Requisition.
  3. Select a Verified Resume belonging to that candidate.
  4. Click **Submit Application**.
- **Duplicate Prevention:** The database enforces `UNIQUE(applicant_id, job_id)`. If a candidate has already applied for this role, the submission is rejected with an informative warning.
- **Stored Procedure Status Advancement:**
  - Select an active application and choose the target status (`Screening`, `Interview`, `Offered`, `Rejected`, `Hired`).
  - Click **Update Status**. The system executes `CALL update_application_status(?, ?)` inside PostgreSQL with strict domain validation.

---

### 📅 Module 8: Interviews Management
- **Schedule Interview Round:**
  1. Select an application currently in `Applied` or `Screening` status.
  2. Choose the Interview Date & Time.
  3. Select Interview Format (`Phone`, `Video`, `In-Person`).
  4. Enter interviewer guidance or focus areas.
  5. Click **Schedule Interview**.
- **Automatic Status Synchronization:** Executing `CALL schedule_interview(...)` automatically transitions the parent application status to `'Interview'`.
- **Log Feedback:** Record technical evaluation scores and interviewer feedback, and update round status to `Completed`.

---

### 🏆 Module 9: Hiring Decisions
- **Record Final Outcome:**
  1. Select a candidate who completed interview rounds.
  2. Choose Final Decision (`Hired`, `Rejected`, `Pending`).
  3. Enter Offered Annual Salary, Proposed Start Date, and Decision Notes.
  4. Click **Save Decision**.
- **Automatic Pipeline Finalization:** When `Hired` is recorded, the system automatically synchronizes the parent application status to `Hired` and reflects in dashboard metrics.

---

### 🔍 Module 10: Candidate Skill Matching
- **Select Job Requisition:** Choose any open position (e.g., `Machine Learning Engineer @ NVIDIA`).
- **Real-Time Qualification Leaderboard:** The SQL matching engine computes:
  $$\text{Match Percentage} = \text{ROUND}\left( \frac{\text{Candidate Matched Skills}}{\text{Job Required Skills}} \times 100, 1 \right)$$
- **Competency Gap Analysis:** View exactly which required skills the candidate possesses (✅ Matched) versus missing prerequisites (❌ Missing).
- **One-Click Application:** Recruiters can submit a pre-qualified candidate directly from the matching leaderboard with a single click.

---

### 📈 Module 11: Reports & Analytics
- **Pre-Joined Database Views:**
  - **Company Recruitment Summary:** Aggregated view (`recruitment_summary_view`) of total requisitions and application volume per employer.
  - **Comprehensive Pipeline Dossier:** Pre-joined view (`applicant_application_view`) tracking application progression.
  - **Compensation Benchmark Report:** Minimum, maximum, and average salaries across departments.
  - **Interview Schedules & Feedback Log:** Detailed evaluation records across all interview rounds.
- **Instant CSV Export:** Every analytical table includes an **📥 Download Report CSV** button that generates compliant CSV files for corporate audit and reporting.

---

## 3. Frequently Asked Questions & Troubleshooting

| Issue / Question | Root Cause | Recommended Action |
|:---|:---|:---|
| **Sidebar shows red "Disconnected" indicator** | PostgreSQL server not running or wrong port | Verify PostgreSQL is running on port `4919` via `/Library/PostgreSQL/14/bin/pg_ctl status` and verify `.env` settings. |
| **Duplicate application error message** | Candidate has already applied for this job | This is intentional. The database enforces `UNIQUE(applicant_id, job_id)` to prevent redundant applications. |
| **Invalid application status error** | Stored procedure domain check rejection | Allowed statuses are strictly: `Applied`, `Screening`, `Interview`, `Offered`, `Rejected`, `Hired`. |
| **Uploaded resume not downloading** | File missing from `uploads/` directory | Ensure the application has write permissions to `uploads/`. Verify the file path matches the database record. |
| **Candidate shows 0.0% match** | Job has no required skills or candidate has no matching skills | Configure required competencies in **Skills Management** &rarr; **Job Requirements**. The system safely displays 0.0% without crashing. |
