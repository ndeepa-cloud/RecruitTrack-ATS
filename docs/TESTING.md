# RecruitTrack ATS — Quality Assurance & Testing Report

**Course:** CIS 407 — Database Management Systems  
**Framework:** pytest 9.2.0 (Python 3.13)  
**Database:** PostgreSQL 14 (Port 4919 / Database: `recruittrack_db`)  
**Total Test Count:** 24 Automated Tests  
**Test Status:** 24 Passed, 0 Failed, 0 Warnings  

---

## 1. Test Suite Architecture

The test suite is structured into two complementary test modules:
1. `tests/test_recruittrack.py`: 23 unit, integration, constraint, stored procedure, security, and regression test scenarios covering individual database components.
2. `tests/test_e2e_workflow.py`: A 15-stage end-to-end integration scenario validating the complete recruiter workflow from login to final report export.

---

## 2. Test Execution Command

To execute the complete automated test suite against the live PostgreSQL server:

```bash
.venv/bin/pytest tests/ -v
```

---

## 3. Detailed Results by Scenario

| # | Test Identifier | Module | Description | Result |
|:---:|---|---|---|:---:|
| 1 | `test_complete_15_step_recruitment_workflow` | `test_e2e_workflow.py` | Full 15-step recruiter lifecycle from login to CSV export | **PASSED** |
| 2 | `test_01_database_connection` | `test_recruittrack.py` | Live PostgreSQL connection on port 4919 (`SELECT 1;`) | **PASSED** |
| 3 | `test_02_all_tables_exist` | `test_recruittrack.py` | Confirms all 11 tables exist in public schema | **PASSED** |
| 4 | `test_03_foreign_key_integrity` | `test_recruittrack.py` | Blocks insertion of orphaned child records | **PASSED** |
| 5 | `test_04_recruiter_authentication_valid` | `test_recruittrack.py` | Validates demo account with bcrypt password hash | **PASSED** |
| 6 | `test_05_recruiter_authentication_invalid` | `test_recruittrack.py` | Blocks invalid passwords & placeholder DEMO_HASH_* | **PASSED** |
| 7 | `test_06_company_crud` | `test_recruittrack.py` | Create, Read, Update, Delete for companies table | **PASSED** |
| 8 | `test_07_applicant_crud` | `test_recruittrack.py` | Create, Read, Update, Delete for applicants table | **PASSED** |
| 9 | `test_08_job_crud` | `test_recruittrack.py` | Create, Read, Update, Delete for jobs table | **PASSED** |
| 10 | `test_09_application_creation` | `test_recruittrack.py` | Submits application linking candidate, job, and resume | **PASSED** |
| 11 | `test_10_duplicate_application_prevention`| `test_recruittrack.py` | UNIQUE (applicant_id, job_id) blocks duplicates | **PASSED** |
| 12 | `test_11_application_status_update_procedure` | `test_recruittrack.py` | Tests `update_application_status` stored procedure | **PASSED** |
| 13 | `test_12_interview_scheduling_procedure`| `test_recruittrack.py` | Tests `schedule_interview` stored procedure | **PASSED** |
| 14 | `test_13_hiring_decisions` | `test_recruittrack.py` | Records decision & prevents duplicate per application | **PASSED** |
| 15 | `test_14_candidate_skill_matching` | `test_recruittrack.py` | Transparent SQL ranking & match percentage | **PASSED** |
| 16 | `test_15_sql_views` | `test_recruittrack.py` | Confirms views return live aggregated data | **PASSED** |
| 17 | `test_16_stored_procedures_validation` | `test_recruittrack.py` | Rejects invalid domain values and nonexistent IDs | **PASSED** |
| 18 | `test_17_dashboard_metrics_accuracy` | `test_recruittrack.py` | Verifies single-row executive metric query accuracy | **PASSED** |
| 19 | `test_18_csv_report_generation` | `test_recruittrack.py` | Verifies DataFrame CSV serialization of reports | **PASSED** |
| 20 | `test_19_input_validation_and_check_constraints` | `test_recruittrack.py` | Rejects negative salary and duplicate emails | **PASSED** |
| 21 | `test_20_transaction_rollback_behavior` | `test_recruittrack.py` | Confirms explicit `ROLLBACK` reverts uncommitted state | **PASSED** |
| 22 | `test_21_candidate_skill_matching_nvidia_regression`| `test_recruittrack.py` | Verifies NVIDIA ML Engineer query parsing and ranking | **PASSED** |
| 23 | `test_22_candidate_skill_matching_all_five_sample_jobs`| `test_recruittrack.py` | Comprehensive skill ranking across all 5 sample jobs | **PASSED** |
| 24 | `test_23_candidate_skill_matching_zero_required_skills_safety`| `test_recruittrack.py` | Mathematical zero-division safety when required skills = 0 | **PASSED** |

---

## 4. Test Isolation and Safety

All integration tests are wrapped inside transaction blocks with explicit `db.rollback()` or targeted temporary cleanup blocks. **Existing sample records are never truncated, overwritten, or modified.**
