"""
RecruitTrack ATS — Modern Enterprise Recruitment Management Platform
CIS 407 — Database Management Systems
Redesigned with a minimalist, premium White & Black SaaS aesthetic.
"""

import datetime
import os
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db_connection import (
    execute_procedure,
    execute_query,
    get_db_config,
    hash_password,
    test_connection,
    verify_password,
)

# Page configuration
st.set_page_config(
    page_title="RecruitTrack — Recruitment Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# GLOBAL WHITE & BLACK DESIGN SYSTEM (CSS)
# =========================================================
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        line-height: 1.55;
    }

    /* Streamlit top header bar removal/minimal */
    header[data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-bottom: 1px solid #E5E7EB !important;
    }

    /* Main container spacing & balanced screen presence */
    .block-container {
        padding-top: 1.75rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1380px !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Typography Hierarchy & High-Contrast Headings */
    h1, h2, h3, h4, h5, h6,
    .page-title, h1.page-title, div.page-title,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] .page-title,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        letter-spacing: -0.02em !important;
    }

    .page-title, h1.page-title {
        font-size: 30px !important;
        font-weight: 800 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.25 !important;
        margin-top: 0 !important;
        margin-bottom: 4px !important;
        display: block !important;
    }
    .page-desc, p.page-desc {
        font-size: 14.5px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
        margin-bottom: 24px !important;
        line-height: 1.5 !important;
        display: block !important;
    }
    .section-title, h2.section-title {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.35 !important;
        margin-top: 16px !important;
        margin-bottom: 10px !important;
        display: block !important;
    }
    .card-title, h3.card-title {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.4 !important;
        margin-bottom: 6px !important;
        display: block !important;
    }
    .caption-text {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        line-height: 1.45 !important;
    }

    div[data-testid="stCaptionContainer"] {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        line-height: 1.45 !important;
    }

    /* Sidebar Styling — Compact 270px Enterprise Nav */
    section[data-testid="stSidebar"] {
        min-width: 265px !important;
        max-width: 275px !important;
        width: 270px !important;
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
        padding-top: 0.85rem !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.25rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-bottom: 1.5rem !important;
    }

    /* Sidebar Navigation Buttons — Consistent 40-44px heights */
    section[data-testid="stSidebar"] button {
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 0 12px !important;
        font-size: 13.5px !important;
        border-radius: 6px !important;
        min-height: 40px !important;
        height: 42px !important;
        line-height: 42px !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.01em !important;
        display: flex !important;
        align-items: center !important;
        transition: all 0.12s ease !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"] {
        border: 1px solid transparent !important;
        color: #1F2937 !important;
        background: transparent !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #F3F4F6 !important;
        color: #111111 !important;
    }
    section[data-testid="stSidebar"] button[kind="primary"] {
        background: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #111111 !important;
        font-weight: 600 !important;
    }

    /* Compact Nav group header */
    .nav-category {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 10px 4px 3px 4px !important;
        margin-top: 4px !important;
    }

    /* Global Primary Buttons */
    .stButton > button[kind="primary"] {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #111111 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        padding: 9px 18px !important;
        min-height: 42px !important;
        letter-spacing: -0.01em !important;
        transition: background 0.15s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #27272A !important;
        border-color: #27272A !important;
        color: #FFFFFF !important;
    }

    /* Global Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        padding: 9px 18px !important;
        min-height: 42px !important;
        letter-spacing: -0.01em !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #F9FAFB !important;
        border-color: #9CA3AF !important;
        color: #111111 !important;
    }

    /* Form submit button */
    div[data-testid="stForm"] .stButton > button {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #111111 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
        min-height: 42px !important;
    }
    div[data-testid="stForm"] .stButton > button:hover {
        background-color: #27272A !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #111111 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        font-size: 14px !important;
        min-height: 40px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #27272A !important;
    }

    /* Form Labels */
    label[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #1F2937 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.4 !important;
        margin-bottom: 4px !important;
    }

    /* Input fields and selectboxes */
    input[type="text"], input[type="password"], input[type="number"], textarea,
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #1F2937 !important;
        font-size: 14.5px !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        padding: 8px 12px !important;
    }
    input:focus, textarea:focus {
        border-color: #111111 !important;
        box-shadow: 0 0 0 1px #111111 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        min-height: 42px !important;
    }
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span {
        font-size: 14.5px !important;
        font-weight: 500 !important;
        color: #1F2937 !important;
    }
    div[data-baseweb="select"]:focus-within > div {
        border-color: #111111 !important;
    }

    /* Form containers */
    div[data-testid="stForm"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 22px 26px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #475569 !important;
        padding: 10px 18px !important;
        border-bottom: 2px solid transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #111111 !important;
        font-weight: 700 !important;
        border-bottom-color: #111111 !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        box-shadow: none !important;
    }

    /* Native DataFrame Container Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    /* Enterprise Report & Data Table Styling */
    .table-container {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    table.report-table {
        width: 100% !important;
        border-collapse: collapse !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #FFFFFF !important;
        text-align: left !important;
        margin: 0 !important;
    }
    table.report-table th {
        background-color: #F8FAFC !important;
        color: #111827 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        padding: 13px 18px !important;
        text-align: left !important;
        border-bottom: 1px solid #E5E7EB !important;
        letter-spacing: -0.01em !important;
        position: sticky !important;
        top: 0 !important;
        z-index: 2 !important;
        white-space: nowrap !important;
    }
    table.report-table td {
        padding: 13px 18px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #1F2937 !important;
        border-bottom: 1px solid #F1F5F9 !important;
        line-height: 1.55 !important;
    }
    table.report-table tr:last-child td {
        border-bottom: none !important;
    }
    table.report-table tr:hover td {
        background-color: #F8FAFC !important;
    }

    /* Custom KPI Card */
    .kpi-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px 22px;
        margin-bottom: 12px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }
    .kpi-number {
        font-size: 2.25rem;
        font-weight: 800;
        color: #111111;
        letter-spacing: -0.035em;
        line-height: 1.1;
    }

    /* Subtle Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 13px;
        font-weight: 600;
    }
    .badge-applied { background-color: #F1F5F9; color: #475569; }
    .badge-screening { background-color: #FEF3C7; color: #92400E; }
    .badge-interview { background-color: #EFF6FF; color: #1E40AF; }
    .badge-offered { background-color: #ECFDF5; color: #065F46; }
    .badge-hired { background-color: #DCFCE7; color: #15803D; font-weight: 600; }
    .badge-rejected { background-color: #FEE2E2; color: #DC2626; }

    /* Alert callouts */
    div[data-testid="stAlert"] {
        border-radius: 6px !important;
        border: 1px solid #E5E7EB !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Upload directory verification
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "resumes")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# SESSION STATE & AUTHENTICATION
# =========================================================
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None

if "current_nav" not in st.session_state:
    st.session_state["current_nav"] = "Dashboard"

def is_authenticated() -> bool:
    return st.session_state["authenticated_user"] is not None

def require_auth():
    """Restricts write operations to authenticated recruiters."""
    if not is_authenticated():
        st.warning(
            "🔒 **Authentication Required:** You must be signed in as a recruiter "
            "to perform this action. Use the recruiter profile panel in the sidebar."
        )
        return False
    return True

def get_current_recruiter_company_id():
    """Returns the company_id of the currently authenticated recruiter, or None."""
    if is_authenticated():
        u = st.session_state.get("authenticated_user")
        if u and "company_id" in u:
            return u["company_id"]
    return None

def verify_company_access(target_company_id: int) -> bool:
    """
    Enforces tenant authorization: authenticated recruiters may only access or mutate
    records belonging to their own employer organization.
    """
    if not is_authenticated():
        return False
    rec_cid = get_current_recruiter_company_id()
    if rec_cid is None:
        return False
    return int(rec_cid) == int(target_company_id)


# =========================================================
# SIDEBAR: LOGO, HEALTH INDICATOR & NAVIGATION
# =========================================================

# Platform Branding
st.sidebar.markdown(
    """
    <div style="padding: 4px 0 10px 0; border-bottom: 1px solid #E5E7EB; margin-bottom: 8px;">
        <div style="font-size: 1.25rem; font-weight: 800; color: #111111; letter-spacing: -0.03em; display: flex; align-items: center; gap: 8px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#111111" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
            </svg>
            RecruitTrack
        </div>
        <div style="font-size: 0.76rem; color: #64748B; font-weight: 500; margin-top: 2px; letter-spacing: -0.01em;">
            Recruitment Management
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compact Database Connection Indicator
db_ok, db_status_msg = test_connection()
config = get_db_config()

if db_ok:
    st.sidebar.markdown(
        f"""
        <div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 6px; font-size: 11px; color: #111827; margin-bottom: 8px; width: 100%;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #15803D; display: inline-block;"></span>
            <span style="font-weight: 600;">PostgreSQL 14</span>
            <span style="color: #64748B; font-weight: 500;">• Port {config['port']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        f"""
        <div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; background: #FEF2F2; border: 1px solid #FECACA; border-radius: 6px; font-size: 11px; color: #DC2626; margin-bottom: 8px; width: 100%;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #DC2626; display: inline-block;"></span>
            <span style="font-weight: 600;">Disconnected</span>
            <span style="color: #64748B; font-weight: 500;">• Port {config['port']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Recruiter Profile & Session Box (Circular Initials Avatar Redesign)
if is_authenticated():
    u = st.session_state["authenticated_user"]
    full_name = u.get("full_name", "Recruiter")
    parts = full_name.strip().split()
    initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else (parts[0][:2]).upper() if parts else "RT"
    company_name = u.get("company_name", "Recruiter")

    st.sidebar.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; padding: 8px 10px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 8px; margin-bottom: 6px;">
            <div style="width: 36px; height: 36px; min-width: 36px; border-radius: 50%; background: #111111; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; letter-spacing: 0.02em;">
                {initials}
            </div>
            <div style="overflow: hidden; flex: 1;">
                <div style="font-size: 13px; font-weight: 700; color: #111111; line-height: 1.2; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;" title="{full_name}">{full_name}</div>
                <div style="font-size: 11px; color: #64748B; font-weight: 500; margin-top: 2px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;" title="{company_name}">{company_name}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Sign Out", key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state["authenticated_user"] = None
        st.session_state["jump_to_action"] = None
        st.rerun()
else:
    with st.sidebar.expander("🔐 Recruiter Sign In", expanded=False):
        login_email = st.text_input("Email", value="sarah.johnson@example.com", key="sb_login_email")
        login_password = st.text_input("Password", type="password", value="DemoRecruiter2026!", key="sb_login_pw")
        if st.button("Sign In", key="sb_signin_btn", use_container_width=True, type="primary"):
            if not login_email or not login_password:
                st.error("Enter email and password.")
            elif not db_ok:
                st.error("Database unavailable.")
            else:
                try:
                    query = """
                        SELECT r.recruiter_id, r.company_id, r.full_name, r.email, r.password_hash, c.company_name
                        FROM recruiters r
                        JOIN companies c ON r.company_id = c.company_id
                        WHERE r.email = %s;
                    """
                    users = execute_query(query, (login_email.strip(),))
                    if users and verify_password(login_password, users[0]["password_hash"]):
                        st.session_state["authenticated_user"] = users[0]
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except Exception as e:
                    st.error(f"Login failed: {e}")

# Sidebar Categorized Navigation (40-44px heights & monochrome icons)
NAV_GROUPS = {
    "Overview": [
        ("Dashboard", "⊞"),
        ("Reports & Analytics", "◫"),
    ],
    "Recruitment": [
        ("Companies", "🏢"),
        ("Recruiters", "👥"),
        ("Jobs", "💼"),
        ("Applicants & Resumes", "👤"),
        ("Applications", "📝"),
        ("Interviews", "📅"),
        ("Hiring Decisions", "🏆"),
    ],
    "Intelligence": [
        ("Skills Management", "🎯"),
        ("Candidate Skill Matching", "🔍"),
    ],
}

for group_name, items in NAV_GROUPS.items():
    st.sidebar.markdown(f'<div class="nav-category">{group_name}</div>', unsafe_allow_html=True)
    for title, icon in items:
        is_active = (st.session_state["current_nav"] == title)
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(f"{icon}  {title}", key=f"nav_btn_{title}", use_container_width=True, type=btn_type):
            st.session_state["current_nav"] = title
            st.session_state["jump_to_action"] = None
            st.rerun()

current_page = st.session_state["current_nav"]


# =========================================================
# REUSABLE DATABASE READ HELPERS
# =========================================================
def load_companies():
    return execute_query("SELECT company_id, company_name, industry, location, website FROM companies ORDER BY company_name;")

def load_recruiters(company_id=None):
    if company_id:
        return execute_query(
            "SELECT r.recruiter_id, r.company_id, r.full_name, r.email, c.company_name "
            "FROM recruiters r JOIN companies c ON r.company_id = c.company_id "
            "WHERE r.company_id = %s ORDER BY r.full_name;",
            (company_id,),
        )
    return execute_query(
        "SELECT r.recruiter_id, r.company_id, r.full_name, r.email, c.company_name "
        "FROM recruiters r JOIN companies c ON r.company_id = c.company_id "
        "ORDER BY c.company_name, r.full_name;"
    )

def load_skills():
    return execute_query("SELECT skill_id, skill_name FROM skills ORDER BY skill_name;")

def load_applicants():
    return execute_query("SELECT applicant_id, full_name, email, phone, location FROM applicants ORDER BY full_name;")

def load_resumes(applicant_id=None):
    if applicant_id:
        return execute_query(
            "SELECT resume_id, applicant_id, file_name, file_path, uploaded_date FROM resumes WHERE applicant_id = %s ORDER BY uploaded_date DESC;",
            (applicant_id,),
        )
    return execute_query(
        "SELECT r.resume_id, r.applicant_id, a.full_name, r.file_name, r.file_path, r.uploaded_date "
        "FROM resumes r JOIN applicants a ON r.applicant_id = a.applicant_id ORDER BY r.uploaded_date DESC;"
    )

def load_jobs(open_only=False):
    sql = """
        SELECT j.job_id, j.company_id, c.company_name, j.recruiter_id, r.full_name AS recruiter_name,
               j.job_title, j.description, j.location, j.salary, j.posted_date, j.status
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        JOIN recruiters r ON j.recruiter_id = r.recruiter_id
    """
    if open_only:
        sql += " WHERE j.status = 'Open'"
    sql += " ORDER BY j.posted_date DESC, j.job_title ASC;"
    return execute_query(sql)


# =========================================================
# HELPER: ENTERPRISE DATA TABLE RENDERER
# =========================================================
def render_styled_table(df, max_height: int = 540):
    """
    Renders a high-readability enterprise table with strong typography:
    - 14px bold #111827 header on #F8FAFC with 13px 18px padding
    - 14px font-weight 500 rows (#1F2937) with 13px 18px padding
    - Thin borders (#E5E7EB) and subtle hover
    """
    if df is None:
        return
    if isinstance(df, list):
        df = pd.DataFrame(df)
    if df.empty:
        st.info("No records to display.")
        return

    display_df = df.copy()
    for col in display_df.columns:
        col_str = str(col).lower()
        if "salary" in col_str or "compensation" in col_str:
            display_df[col] = display_df[col].apply(
                lambda v: f"${float(v):,.2f}" if pd.notnull(v) and str(v).replace('.', '', 1).isdigit() else v
            )
        elif pd.api.types.is_float_dtype(display_df[col]):
            display_df[col] = display_df[col].apply(lambda v: f"{v:,.1f}" if pd.notnull(v) else "")

    table_html = display_df.to_html(classes="report-table", index=False, escape=True)
    st.markdown(
        f"""
        <div class="table-container" style="max-height: {max_height}px; overflow-y: auto; overflow-x: auto; margin-bottom: 16px;">
            {table_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HELPER: HIGH-CONTRAST PAGE HEADER
# =========================================================
def render_page_header(title: str, description: str):
    """Renders bold, high-contrast page titles and descriptions that cannot be overridden by CSS/theme conflicts."""
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <h1 class="page-title" style="color: #111111 !important; -webkit-text-fill-color: #111111 !important; font-size: 30px !important; font-weight: 800 !important; margin: 0 0 6px 0 !important; letter-spacing: -0.03em !important; line-height: 1.25 !important;">
                {title}
            </h1>
            <p class="page-desc" style="color: #475569 !important; -webkit-text-fill-color: #475569 !important; font-size: 14.5px !important; font-weight: 500 !important; margin: 0 !important; line-height: 1.5 !important;">
                {description}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HELPER: MODERN PLOTLY THEME
# =========================================================
def apply_saas_chart_theme(fig, title=""):
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=16, color="#111111", family="Inter")),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#1F2937", family="Inter", size=13),
        margin=dict(l=24, r=24, t=48, b=24),
        hoverlabel=dict(bgcolor="#111111", font_color="#FFFFFF", font_size=13, font_family="Inter"),
        xaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#475569", size=12, family="Inter"),
            title=dict(font=dict(color="#111111", size=13, family="Inter")),
        ),
        yaxis=dict(
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0",
            tickfont=dict(color="#475569", size=12, family="Inter"),
            title=dict(font=dict(color="#111111", size=13, family="Inter")),
        ),
    )
    return fig


# =========================================================
# PAGE 1: DASHBOARD
# =========================================================
if current_page == "Dashboard":
    render_page_header(
        "Recruitment Overview",
        "Manage hiring operations, track applicants, and monitor recruitment performance."
    )

    if not db_ok:
        st.error(f"Cannot load live dashboard metrics: {db_status_msg}")
    else:
        try:
            # 7 KPI Cards Query
            metrics_sql = """
                SELECT
                    (SELECT COUNT(*) FROM companies) AS total_companies,
                    (SELECT COUNT(*) FROM recruiters) AS total_recruiters,
                    (SELECT COUNT(*) FROM applicants) AS total_applicants,
                    (SELECT COUNT(*) FROM jobs WHERE status = 'Open') AS active_jobs,
                    (SELECT COUNT(*) FROM applications) AS total_applications,
                    (SELECT COUNT(*) FROM interviews) AS total_interviews,
                    (SELECT COUNT(*) FROM hiring_decisions WHERE decision = 'Hired') AS total_hired;
            """
            m = execute_query(metrics_sql)[0]

            # Row 1: 4 KPI Cards
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Total Companies</div>
                        <div class="kpi-number">{m['total_companies']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Total Recruiters</div>
                        <div class="kpi-number">{m['total_recruiters']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Total Applicants</div>
                        <div class="kpi-number">{m['total_applicants']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c4:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Active Jobs</div>
                        <div class="kpi-number">{m['active_jobs']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Row 2: 3 KPI Cards
            c5, c6, c7 = st.columns(3)
            with c5:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Applications Submitted</div>
                        <div class="kpi-number">{m['total_applications']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c6:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Interviews Conducted</div>
                        <div class="kpi-number">{m['total_interviews']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c7:
                st.markdown(
                    f"""<div class="kpi-box">
                        <div class="kpi-title">Hired Candidates</div>
                        <div class="kpi-number">{m['total_hired']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Quick Operations Action Card
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 14px 18px; margin: 16px 0 20px 0;">
                    <div style="font-size: 13px; font-weight: 700; color: #111111; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">
                        ⚡ Quick Operations
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            qa_col1, qa_col2, qa_col3 = st.columns(3)
            with qa_col1:
                if st.button("➕ Register Candidate", key="qa_btn_cand", use_container_width=True, type="secondary"):
                    st.session_state["current_nav"] = "Applicants & Resumes"
                    st.session_state["jump_to_action"] = "register_candidate"
                    st.rerun()
            with qa_col2:
                if st.button("💼 Post Job Requisition", key="qa_btn_job", use_container_width=True, type="secondary"):
                    st.session_state["current_nav"] = "Jobs"
                    st.session_state["jump_to_action"] = "post_job"
                    st.rerun()
            with qa_col3:
                if st.button("📅 Schedule Interview", key="qa_btn_int", use_container_width=True, type="secondary"):
                    st.session_state["current_nav"] = "Interviews"
                    st.session_state["jump_to_action"] = "schedule_interview"
                    st.rerun()

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Charts Row 1: Status Distribution & Funnel
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                status_data = execute_query(
                    "SELECT status, COUNT(*) AS count FROM applications GROUP BY status ORDER BY count DESC;"
                )
                if status_data:
                    df_status = pd.DataFrame(status_data)
                    fig1 = px.pie(
                        df_status,
                        values="count",
                        names="status",
                        hole=0.55,
                        color_discrete_sequence=["#111111", "#334155", "#475569", "#64748B", "#94A3B8", "#CBD5E1"],
                    )
                    fig1.update_traces(textposition="outside", textinfo="label+value")
                    apply_saas_chart_theme(fig1, "Applications by Status")
                    st.plotly_chart(fig1, use_container_width=True)

            with col_chart2:
                funnel_sql = """
                    SELECT
                        'Applied' AS stage, (SELECT COUNT(*) FROM applications) AS count, 1 AS ord
                    UNION ALL
                    SELECT
                        'Screening', (SELECT COUNT(*) FROM applications WHERE status IN ('Screening', 'Interview', 'Offered', 'Hired')), 2
                    UNION ALL
                    SELECT
                        'Interview', (SELECT COUNT(*) FROM applications WHERE status IN ('Interview', 'Offered', 'Hired')), 3
                    UNION ALL
                    SELECT
                        'Offered', (SELECT COUNT(*) FROM applications WHERE status IN ('Offered', 'Hired')), 4
                    UNION ALL
                    SELECT
                        'Hired', (SELECT COUNT(*) FROM hiring_decisions WHERE decision = 'Hired'), 5
                    ORDER BY ord;
                """
                funnel_data = execute_query(funnel_sql)
                if funnel_data:
                    df_funnel = pd.DataFrame(funnel_data)
                    fig_funnel = go.Figure(
                        go.Funnel(
                            y=df_funnel["stage"],
                            x=df_funnel["count"],
                            textinfo="value+percent initial",
                            marker=dict(color=["#111111", "#334155", "#475569", "#64748B", "#15803D"]),
                        )
                    )
                    apply_saas_chart_theme(fig_funnel, "Recruitment Pipeline Funnel")
                    st.plotly_chart(fig_funnel, use_container_width=True)

            # Charts Row 2: Applications per Employer & Hiring Decisions
            col_chart3, col_chart4 = st.columns(2)

            with col_chart3:
                comp_data = execute_query("""
                    SELECT c.company_name, COUNT(ap.application_id) AS applications
                    FROM companies c
                    LEFT JOIN jobs j ON c.company_id = j.company_id
                    LEFT JOIN applications ap ON j.job_id = ap.job_id
                    GROUP BY c.company_name
                    ORDER BY applications DESC;
                """)
                if comp_data:
                    df_comp = pd.DataFrame(comp_data)
                    fig3 = px.bar(
                        df_comp,
                        x="company_name",
                        y="applications",
                        color_discrete_sequence=["#111111"],
                        labels={"company_name": "Employer", "applications": "Applications"},
                    )
                    apply_saas_chart_theme(fig3, "Applications per Employer")
                    st.plotly_chart(fig3, use_container_width=True)

            with col_chart4:
                hiring_data = execute_query(
                    "SELECT decision, COUNT(*) AS count FROM hiring_decisions GROUP BY decision ORDER BY count DESC;"
                )
                if hiring_data:
                    df_hiring = pd.DataFrame(hiring_data)
                    color_map = {"Hired": "#15803D", "Rejected": "#DC2626", "Pending": "#D97706"}
                    fig4 = px.bar(
                        df_hiring,
                        x="decision",
                        y="count",
                        color="decision",
                        color_discrete_map=color_map,
                        labels={"decision": "Decision", "count": "Count"},
                    )
                    apply_saas_chart_theme(fig4, "Hiring Decisions Breakdown")
                    st.plotly_chart(fig4, use_container_width=True)

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">Recent Applications</div>', unsafe_allow_html=True)
            recent_apps = execute_query("""
                SELECT a.full_name AS "Candidate", j.job_title AS "Position", c.company_name AS "Employer",
                       ap.status AS "Stage", ap.applied_date AS "Applied Date", ap.application_id AS "ID"
                FROM applications ap
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                ORDER BY ap.applied_date DESC, ap.application_id DESC
                LIMIT 5;
            """)
            if recent_apps:
                render_styled_table(pd.DataFrame(recent_apps))
        except Exception as e:
            st.error(f"Error rendering dashboard: {e}")


# =========================================================
# PAGE 2: COMPANIES
# =========================================================
elif current_page == "Companies":
    render_page_header(
        "Companies",
        "Manage client employer organizations, industry classifications, and headquarters."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        tab_v, tab_a, tab_e = st.tabs(["Company Directory", "Register Company", "Edit Company"])

        with tab_v:
            col_c_s1, col_c_s2, col_c_s3 = st.columns([2, 1, 1])
            with col_c_s1:
                search_comp = st.text_input("Search companies", "", placeholder="Search by name or headquarters...", key="c_search")
            with col_c_s2:
                all_comps = execute_query("SELECT DISTINCT industry FROM companies WHERE industry IS NOT NULL ORDER BY industry;")
                ind_opts = ["All Industries"] + [r["industry"] for r in (all_comps or [])]
                ind_filter = st.selectbox("Industry", ind_opts, key="c_ind_filter")
            with col_c_s3:
                sort_c = st.selectbox("Sort By", ["Name (A-Z)", "Name (Z-A)", "Industry (A-Z)"], key="c_sort")

            sql_comp = """
                SELECT company_name AS "Company Name", industry AS "Industry",
                       location AS "Headquarters", website AS "Website", company_id AS "ID"
                FROM companies
                WHERE 1=1
            """
            params_comp = []
            if ind_filter != "All Industries":
                sql_comp += " AND industry = %s"
                params_comp.append(ind_filter)
            if search_comp.strip():
                sql_comp += " AND (company_name ILIKE %s OR location ILIKE %s OR industry ILIKE %s)"
                kw = f"%{search_comp.strip()}%"
                params_comp.extend([kw, kw, kw])

            if sort_c == "Name (A-Z)":
                sql_comp += " ORDER BY company_name ASC;"
            elif sort_c == "Name (Z-A)":
                sql_comp += " ORDER BY company_name DESC;"
            else:
                sql_comp += " ORDER BY industry ASC, company_name ASC;"

            companies_df = pd.DataFrame(execute_query(sql_comp, tuple(params_comp) if params_comp else None))
            render_styled_table(companies_df)

        with tab_a:
            with st.form("add_comp_form", clear_on_submit=True):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    c_name = st.text_input("Company Name *", placeholder="e.g. Stripe Inc.")
                    c_ind = st.text_input("Industry *", placeholder="e.g. Financial Technology")
                with col_c2:
                    c_loc = st.text_input("Location", placeholder="e.g. San Francisco, CA")
                    c_web = st.text_input("Website", placeholder="https://stripe.com")
                submit_comp = st.form_submit_button("Register Company")

                if submit_comp:
                    if require_auth():
                        if not c_name.strip() or not c_ind.strip():
                            st.error("Company Name and Industry are required.")
                        else:
                            try:
                                execute_query(
                                    "INSERT INTO companies (company_name, industry, location, website) VALUES (%s, %s, %s, %s);",
                                    (c_name.strip(), c_ind.strip(), c_loc.strip(), c_web.strip()),
                                    fetch=False,
                                    commit=True,
                                )
                                st.success(f"Company '{c_name}' created.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to add company: {e}")

        with tab_e:
            companies = load_companies()
            if companies:
                c_map = {f"{c['company_name']} (ID: {c['company_id']})": c for c in companies}
                sel_c_lbl = st.selectbox("Select Company", list(c_map.keys()), key="sel_c_edit")
                sel_c = c_map[sel_c_lbl]

                rec_cid = get_current_recruiter_company_id()
                is_authorized = (rec_cid is None or int(rec_cid) == int(sel_c["company_id"]))

                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    with st.form("edit_comp_form"):
                        e_cname = st.text_input("Company Name *", value=sel_c["company_name"])
                        e_cind = st.text_input("Industry *", value=sel_c["industry"] or "")
                        e_cloc = st.text_input("Headquarters Location", value=sel_c["location"] or "")
                        e_cweb = st.text_input("Corporate Website", value=sel_c["website"] or "")
                        submit_u_c = st.form_submit_button("Save Changes")
                        if submit_u_c:
                            if require_auth():
                                if not is_authorized:
                                    st.error("⛔ Tenant Isolation: You are authenticated with another organization and cannot edit this company.")
                                elif not e_cname.strip() or not e_cind.strip():
                                    st.error("Company Name and Industry are required.")
                                else:
                                    try:
                                        execute_query(
                                            "UPDATE companies SET company_name = %s, industry = %s, location = %s, website = %s WHERE company_id = %s;",
                                            (e_cname.strip(), e_cind.strip(), e_cloc.strip(), e_cweb.strip(), sel_c["company_id"]),
                                            fetch=False,
                                            commit=True,
                                        )
                                        st.success("Company updated successfully.")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Update failed: {e}")

                with col_e2:
                    st.markdown("<div style='font-size: 0.9rem; font-weight: 600; margin-bottom: 6px;'>Delete Organization</div>", unsafe_allow_html=True)
                    st.caption("Cannot delete companies with associated jobs or active recruiters.")
                    del_conf = st.checkbox(f"Confirm deletion of '{sel_c['company_name']}'", key="cb_del_c")
                    if st.button("Delete Company", disabled=not del_conf, key="del_c_btn"):
                        if require_auth():
                            if not is_authorized:
                                st.error("⛔ Tenant Isolation: You cannot delete an organization you do not belong to.")
                            else:
                                try:
                                    execute_query("DELETE FROM companies WHERE company_id = %s;", (sel_c["company_id"],), fetch=False, commit=True)
                                    st.success(f"Company '{sel_c['company_name']}' deleted.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Cannot delete company: {e}")


# =========================================================
# PAGE 3: RECRUITERS
# =========================================================
elif current_page == "Recruiters":
    render_page_header(
        "Recruiters",
        "Manage talent acquisition personnel, employer associations, and authentication credentials."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        tab_rv, tab_ra, tab_re = st.tabs(["Recruiter Directory", "Add Recruiter", "Edit Recruiter"])

        with tab_rv:
            col_r_s1, col_r_s2, col_r_s3 = st.columns([2, 1, 1])
            with col_r_s1:
                search_rec = st.text_input("Search recruiters", "", placeholder="Search by name or email...", key="r_search")
            with col_r_s2:
                all_c = load_companies()
                rec_c_opts = ["All Employers"] + [c["company_name"] for c in (all_c or [])]
                emp_filter = st.selectbox("Employer", rec_c_opts, key="r_emp_filter")
            with col_r_s3:
                sort_r = st.selectbox("Sort By", ["Name (A-Z)", "Name (Z-A)", "Employer (A-Z)"], key="r_sort")

            sql_rec = """
                SELECT r.full_name AS "Recruiter Name", c.company_name AS "Employer",
                       r.email AS "Corporate Email", r.recruiter_id AS "ID"
                FROM recruiters r
                JOIN companies c ON r.company_id = c.company_id
                WHERE 1=1
            """
            params_rec = []
            if emp_filter != "All Employers":
                sql_rec += " AND c.company_name = %s"
                params_rec.append(emp_filter)
            if search_rec.strip():
                sql_rec += " AND (r.full_name ILIKE %s OR r.email ILIKE %s)"
                kw = f"%{search_rec.strip()}%"
                params_rec.extend([kw, kw])

            if sort_r == "Name (A-Z)":
                sql_rec += " ORDER BY r.full_name ASC;"
            elif sort_r == "Name (Z-A)":
                sql_rec += " ORDER BY r.full_name DESC;"
            else:
                sql_rec += " ORDER BY c.company_name ASC, r.full_name ASC;"

            recs_df = pd.DataFrame(execute_query(sql_rec, tuple(params_rec) if params_rec else None))
            render_styled_table(recs_df)

        with tab_ra:
            companies = load_companies()
            if not companies:
                st.warning("Please add at least one company first.")
            else:
                c_map = {c["company_name"]: c["company_id"] for c in companies}
                rec_cid = get_current_recruiter_company_id()
                c_names = list(c_map.keys())
                def_c_idx = 0
                if rec_cid:
                    for idx, c in enumerate(companies):
                        if c["company_id"] == rec_cid:
                            def_c_idx = idx
                            break

                with st.form("add_rec_form", clear_on_submit=True):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        r_name = st.text_input("Full Name *", placeholder="Alex Rivera")
                        r_email = st.text_input("Corporate Email *", placeholder="alex.rivera@company.com")
                    with col_r2:
                        r_comp = st.selectbox("Associated Company *", c_names, index=def_c_idx)
                        r_pass = st.text_input("Password *", type="password", placeholder="Minimum 6 characters")
                    submit_r = st.form_submit_button("Register Recruiter")

                    if submit_r:
                        if require_auth():
                            target_cid = c_map[r_comp]
                            if rec_cid and int(rec_cid) != int(target_cid):
                                st.error("⛔ Tenant Isolation: You may only register recruiters for your own company.")
                            elif not r_name.strip() or not r_email.strip() or not r_pass.strip():
                                st.error("All marked fields are required.")
                            elif len(r_pass) < 6:
                                st.error("Password must be at least 6 characters.")
                            else:
                                try:
                                    hp = hash_password(r_pass)
                                    execute_query(
                                        "INSERT INTO recruiters (company_id, full_name, email, password_hash) VALUES (%s, %s, %s, %s);",
                                        (target_cid, r_name.strip(), r_email.strip(), hp),
                                        fetch=False,
                                        commit=True,
                                    )
                                    st.success(f"Recruiter '{r_name}' registered successfully.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to add recruiter: {e}")

        with tab_re:
            recs = load_recruiters()
            companies = load_companies()
            if recs and companies:
                rec_dict = {f"{r['full_name']} ({r['email']})": r for r in recs}
                sel_r_lbl = st.selectbox("Select Recruiter", list(rec_dict.keys()), key="sel_r_edit")
                sel_r = rec_dict[sel_r_lbl]
                c_map = {c["company_name"]: c["company_id"] for c in companies}

                rec_cid = get_current_recruiter_company_id()
                is_authorized = (rec_cid is None or int(rec_cid) == int(sel_r["company_id"]))

                with st.form("edit_rec_form"):
                    u_rname = st.text_input("Full Name *", value=sel_r["full_name"])
                    u_remail = st.text_input("Email *", value=sel_r["email"])
                    u_rcomp = st.selectbox("Company *", list(c_map.keys()), index=list(c_map.keys()).index(sel_r["company_name"]) if sel_r["company_name"] in c_map else 0)
                    u_rpass = st.text_input("Update Password (optional)", type="password")
                    submit_re = st.form_submit_button("Update Recruiter")

                    if submit_re:
                        if require_auth():
                            if not is_authorized:
                                st.error("⛔ Tenant Isolation: You cannot modify recruiters from other organizations.")
                            elif not u_rname.strip() or not u_remail.strip():
                                st.error("Full Name and Email are required.")
                            else:
                                try:
                                    target_comp_id = c_map[u_rcomp]
                                    if u_rpass.strip():
                                        execute_query(
                                            "UPDATE recruiters SET full_name = %s, email = %s, company_id = %s, password_hash = %s WHERE recruiter_id = %s;",
                                            (u_rname.strip(), u_remail.strip(), target_comp_id, hash_password(u_rpass.strip()), sel_r["recruiter_id"]),
                                            fetch=False,
                                            commit=True,
                                        )
                                    else:
                                        execute_query(
                                            "UPDATE recruiters SET full_name = %s, email = %s, company_id = %s WHERE recruiter_id = %s;",
                                            (u_rname.strip(), u_remail.strip(), target_comp_id, sel_r["recruiter_id"]),
                                            fetch=False,
                                            commit=True,
                                        )
                                    st.success("Recruiter profile updated.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Update failed: {e}")


# =========================================================
# PAGE 4: JOBS
# =========================================================
elif current_page == "Jobs":
    render_page_header(
        "Job Requisitions",
        "Create and track open job postings, salary bands, and assigned hiring managers."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        is_post_jump = (st.session_state.get("jump_to_action") == "post_job")
        if is_post_jump:
            c_banner1, c_banner2 = st.columns([4, 1])
            c_banner1.info("⚡ Quick Action: Create and publish a new job requisition below.")
            if c_banner2.button("← Directory", key="exit_qa_job"):
                st.session_state["jump_to_action"] = None
                st.rerun()
            tab_ja, tab_jv, tab_je = st.tabs(["Post Requisition", "Active Requisitions", "Edit Requisition"])
        else:
            tab_jv, tab_ja, tab_je = st.tabs(["Active Requisitions", "Post Requisition", "Edit Requisition"])

        with tab_jv:
            col_j_s1, col_j_s2, col_j_s3, col_j_s4 = st.columns([2, 1, 1, 1])
            with col_j_s1:
                search_job = st.text_input("Search requisitions", "", placeholder="Search title or location...", key="j_search")
            with col_j_s2:
                companies = load_companies()
                comp_filter = st.selectbox("Employer", ["All Employers"] + [c["company_name"] for c in (companies or [])], key="j_comp_filt")
            with col_j_s3:
                status_filter = st.selectbox("Status", ["All Statuses", "Open", "Closed"], key="j_stat_filt")
            with col_j_s4:
                sort_j = st.selectbox("Sort By", ["Newest First", "Oldest First", "Salary (High-Low)", "Salary (Low-High)", "Title (A-Z)"], key="j_sort")

            sql_j = """
                SELECT j.job_title AS "Position Title", c.company_name AS "Employer", j.location AS "Location",
                       j.salary AS "Annual Salary", j.status AS "Status", r.full_name AS "Recruiter",
                       j.posted_date AS "Posted Date", j.job_id AS "ID"
                FROM jobs j
                JOIN companies c ON j.company_id = c.company_id
                JOIN recruiters r ON j.recruiter_id = r.recruiter_id
                WHERE 1=1
            """
            params_j = []
            if comp_filter != "All Employers":
                sql_j += " AND c.company_name = %s"
                params_j.append(comp_filter)
            if status_filter != "All Statuses":
                sql_j += " AND j.status = %s"
                params_j.append(status_filter)
            if search_job.strip():
                sql_j += " AND (j.job_title ILIKE %s OR j.location ILIKE %s)"
                kw = f"%{search_job.strip()}%"
                params_j.extend([kw, kw])

            if sort_j == "Newest First":
                sql_j += " ORDER BY j.posted_date DESC, j.job_id DESC;"
            elif sort_j == "Oldest First":
                sql_j += " ORDER BY j.posted_date ASC, j.job_id ASC;"
            elif sort_j == "Salary (High-Low)":
                sql_j += " ORDER BY j.salary DESC NULLS LAST;"
            elif sort_j == "Salary (Low-High)":
                sql_j += " ORDER BY j.salary ASC NULLS LAST;"
            else:
                sql_j += " ORDER BY j.job_title ASC;"

            jobs_df = pd.DataFrame(execute_query(sql_j, tuple(params_j) if params_j else None))
            render_styled_table(jobs_df)

        with tab_ja:
            companies = load_companies()
            if companies:
                c_map = {c["company_name"]: c["company_id"] for c in companies}
                rec_cid = get_current_recruiter_company_id()
                c_names = list(c_map.keys())
                def_c_idx = 0
                if rec_cid:
                    for idx, c in enumerate(companies):
                        if c["company_id"] == rec_cid:
                            def_c_idx = idx
                            break

                sel_c_name = st.selectbox("Employer Organization *", c_names, index=def_c_idx, key="job_add_comp_sel")
                sel_cid = c_map[sel_c_name]

                # Recruiter selection: Enforces that recruiter belongs to the selected company
                comp_recs = load_recruiters(company_id=sel_cid)
                if not comp_recs:
                    st.warning(f"No recruiters registered for {sel_c_name}. Register a recruiter first.")
                else:
                    rec_map = {f"{r['full_name']} ({r['email']})": r["recruiter_id"] for r in comp_recs}
                    with st.form("add_job_form", clear_on_submit=True):
                        j_title = st.text_input("Position Title *", placeholder="e.g. Senior Backend Engineer")
                        j_rec = st.selectbox("Assigned Recruiter *", list(rec_map.keys()))
                        col_j1, col_j2 = st.columns(2)
                        with col_j1:
                            j_salary = st.number_input("Annual Salary ($ USD)", min_value=0.0, step=5000.0, value=120000.0)
                        with col_j2:
                            j_loc = st.text_input("Location", value="Remote / Hybrid")
                        j_desc = st.text_area("Position Description", placeholder="Key responsibilities and qualifications...")
                        j_status = st.selectbox("Status", ["Open", "Closed"])
                        submit_j = st.form_submit_button("Post Requisition")

                        if submit_j:
                            if require_auth():
                                if rec_cid and int(rec_cid) != int(sel_cid):
                                    st.error("⛔ Tenant Isolation: You cannot post requisitions for an organization you do not belong to.")
                                elif not j_title.strip():
                                    st.error("Position Title is required.")
                                else:
                                    try:
                                        execute_query(
                                            """
                                            INSERT INTO jobs (company_id, recruiter_id, job_title, description, location, salary, posted_date, status)
                                            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, %s);
                                            """,
                                            (sel_cid, rec_map[j_rec], j_title.strip(), j_desc.strip(), j_loc.strip(), j_salary, j_status),
                                            fetch=False,
                                            commit=True,
                                        )
                                        st.success(f"Requisition '{j_title}' posted.")
                                        st.session_state["jump_to_action"] = None
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Failed to post job: {e}")

        with tab_je:
            jobs = load_jobs()
            if jobs:
                j_dict = {f"{j['job_title']} @ {j['company_name']} (ID: {j['job_id']})": j for j in jobs}
                sel_j_lbl = st.selectbox("Select Requisition to Edit", list(j_dict.keys()), key="sel_j_edit")
                sel_j = j_dict[sel_j_lbl]

                rec_cid = get_current_recruiter_company_id()
                is_authorized = (rec_cid is None or int(rec_cid) == int(sel_j["company_id"]))

                with st.form("edit_job_form"):
                    u_jtitle = st.text_input("Position Title *", value=sel_j["job_title"])
                    u_jsalary = st.number_input("Annual Salary ($ USD)", min_value=0.0, value=float(sel_j["salary"] or 0), step=5000.0)
                    u_jloc = st.text_input("Location", value=sel_j["location"] or "")
                    u_jstatus = st.selectbox("Status", ["Open", "Closed"], index=0 if sel_j["status"] == "Open" else 1)
                    u_jdesc = st.text_area("Description", value=sel_j["description"] or "")
                    submit_uj = st.form_submit_button("Update Requisition")

                    if submit_uj:
                        if require_auth():
                            if not is_authorized:
                                st.error("⛔ Tenant Isolation: You cannot modify requisitions belonging to another organization.")
                            elif not u_jtitle.strip():
                                st.error("Position Title is required.")
                            else:
                                try:
                                    execute_query(
                                        "UPDATE jobs SET job_title = %s, salary = %s, location = %s, status = %s, description = %s WHERE job_id = %s;",
                                        (u_jtitle.strip(), u_jsalary, u_jloc.strip(), u_jstatus, u_jdesc.strip(), sel_j["job_id"]),
                                        fetch=False,
                                        commit=True,
                                    )
                                    st.success("Requisition updated successfully.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Update failed: {e}")


# =========================================================
# PAGE 5: APPLICANTS & RESUMES
# =========================================================
elif current_page == "Applicants & Resumes":
    render_page_header(
        "Applicants & Resumes",
        "Candidate talent pools, verified resume files, and competency profiles."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        is_cand_jump = (st.session_state.get("jump_to_action") == "register_candidate")
        if is_cand_jump:
            c_banner1, c_banner2 = st.columns([4, 1])
            c_banner1.info("⚡ Quick Action: Register a candidate profile and attach resume below.")
            if c_banner2.button("← Directory", key="exit_qa_cand"):
                st.session_state["jump_to_action"] = None
                st.rerun()
            tab_aa, tab_av, tab_ap = st.tabs(["Register Candidate", "Talent Directory", "Candidate Dossier & Resumes"])
        else:
            tab_av, tab_aa, tab_ap = st.tabs(["Talent Directory", "Register Candidate", "Candidate Dossier & Resumes"])

        with tab_av:
            col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
            with col_s1:
                search_cand = st.text_input("Search candidates", "", placeholder="Search name, email, or city...", key="cand_search")
            with col_s2:
                skills_list = load_skills()
                skill_filt = st.selectbox("Endorsed Skill", ["All Skills"] + [s["skill_name"] for s in (skills_list or [])], key="cand_sk_filt")
            with col_s3:
                sort_cand = st.selectbox("Sort By", ["Name (A-Z)", "Name (Z-A)", "Location (A-Z)"], key="cand_sort")

            sql_app = """
                SELECT a.full_name AS "Candidate", a.email AS "Email Address",
                       a.phone AS "Phone", a.location AS "Location", a.applicant_id AS "ID"
                FROM applicants a
            """
            params_app = []
            if skill_filt != "All Skills":
                sql_app += """
                    JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
                    JOIN skills s ON aps.skill_id = s.skill_id
                    WHERE s.skill_name = %s
                """
                params_app.append(skill_filt)
            else:
                sql_app += " WHERE 1=1"

            if search_cand.strip():
                sql_app += " AND (a.full_name ILIKE %s OR a.email ILIKE %s OR a.location ILIKE %s)"
                kw = f"%{search_cand.strip()}%"
                params_app.extend([kw, kw, kw])

            if sort_cand == "Name (A-Z)":
                sql_app += " ORDER BY a.full_name ASC;"
            elif sort_cand == "Name (Z-A)":
                sql_app += " ORDER BY a.full_name DESC;"
            else:
                sql_app += " ORDER BY a.location ASC NULLS LAST, a.full_name ASC;"

            applicants_df = pd.DataFrame(execute_query(sql_app, tuple(params_app) if params_app else None))
            render_styled_table(applicants_df)

        with tab_aa:
            with st.form("add_cand_form", clear_on_submit=True):
                col_a1, col_a2 = st.columns(2)
                with col_a1:
                    a_name = st.text_input("Full Name *", placeholder="Jane Carter")
                    a_email = st.text_input("Email Address *", placeholder="jane.carter@example.com")
                with col_a2:
                    a_phone = st.text_input("Phone Number", placeholder="555-0199")
                    a_loc = st.text_input("Location / State", placeholder="California")
                cv_file = st.file_uploader("Upload Resume Document (.pdf, .docx)", type=["pdf", "docx"], key="cv_file_init")
                submit_cand = st.form_submit_button("Register Candidate")

                if submit_cand:
                    if require_auth():
                        if not a_name.strip() or not a_email.strip():
                            st.error("Full Name and Email are required.")
                        else:
                            try:
                                new_app = execute_query(
                                    "INSERT INTO applicants (full_name, email, phone, location) VALUES (%s, %s, %s, %s) RETURNING applicant_id;",
                                    (a_name.strip(), a_email.strip(), a_phone.strip(), a_loc.strip()),
                                    commit=True,
                                )
                                new_aid = new_app[0]["applicant_id"]

                                safe_cand_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', a_name.lower().replace(" ", "_"))
                                if cv_file is not None:
                                    ext = os.path.splitext(cv_file.name)[1].lower()
                                    fname = f"{safe_cand_name}_resume{ext}"
                                    rel_p = f"uploads/resumes/{fname}"
                                    full_p = os.path.join(os.getcwd(), rel_p)
                                    with open(full_p, "wb") as f:
                                        f.write(cv_file.getbuffer())
                                else:
                                    fname = f"{safe_cand_name}_resume.pdf"
                                    rel_p = f"uploads/resumes/{fname}"
                                    full_p = os.path.join(os.getcwd(), rel_p)
                                    with open(full_p, "w") as f:
                                        f.write(f"Resume document for {a_name}\nEmail: {a_email}")

                                execute_query(
                                    "INSERT INTO resumes (applicant_id, file_name, file_path, uploaded_date) VALUES (%s, %s, %s, CURRENT_DATE);",
                                    (new_aid, fname, rel_p),
                                    fetch=False,
                                    commit=True,
                                )
                                st.success(f"Candidate '{a_name}' registered with resume document.")
                                st.session_state["jump_to_action"] = None
                                st.rerun()
                            except Exception as e:
                                st.error(f"Registration failed: {e}")

        with tab_ap:
            applicants = load_applicants()
            if applicants:
                a_dict = {f"{a['full_name']} ({a['email']})": a for a in applicants}
                sel_a_lbl = st.selectbox("Select Candidate Dossier", list(a_dict.keys()), key="sel_a_dossier")
                sel_a = a_dict[sel_a_lbl]
                cand_id = sel_a["applicant_id"]

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown('<div class="card-title">Resume Documents on File</div>', unsafe_allow_html=True)
                    resumes = load_resumes(applicant_id=cand_id)
                    if resumes:
                        for r in resumes:
                            c_r1, c_r2 = st.columns([3, 1])
                            c_r1.markdown(f"**{r['file_name']}** (Uploaded: {r['uploaded_date']})")
                            f_path = os.path.join(os.getcwd(), r["file_path"])
                            if os.path.exists(f_path):
                                with open(f_path, "rb") as f_obj:
                                    f_bytes = f_obj.read()
                                c_r2.download_button("📥 Download", f_bytes, file_name=r["file_name"], key=f"dl_{r['resume_id']}")
                            else:
                                c_r2.caption("Stored Reference")
                    else:
                        st.info("No resumes uploaded.")

                    with st.expander("Upload Replacement / Supplementary Resume"):
                        new_doc = st.file_uploader("Select Resume (.pdf, .docx)", type=["pdf", "docx"], key="rep_cv_file")
                        if st.button("Upload Document", key="btn_upload_rep"):
                            if require_auth():
                                if new_doc is None:
                                    st.error("Select a document first.")
                                else:
                                    safe_fn = re.sub(r'[^a-zA-Z0-9_.-]', '_', new_doc.name)
                                    rel_fp = f"uploads/resumes/{safe_fn}"
                                    full_fp = os.path.join(os.getcwd(), rel_fp)
                                    with open(full_fp, "wb") as f_out:
                                        f_out.write(new_doc.getbuffer())
                                    execute_query(
                                        "INSERT INTO resumes (applicant_id, file_name, file_path, uploaded_date) VALUES (%s, %s, %s, CURRENT_DATE);",
                                        (cand_id, safe_fn, rel_fp),
                                        fetch=False,
                                        commit=True,
                                    )
                                    st.success(f"Resume '{safe_fn}' attached.")
                                    st.rerun()

                with col_d2:
                    st.markdown('<div class="card-title">Endorsed Competencies</div>', unsafe_allow_html=True)
                    c_skills = execute_query(
                        "SELECT s.skill_name, aps.proficiency_level FROM applicant_skills aps JOIN skills s ON aps.skill_id = s.skill_id WHERE aps.applicant_id = %s;",
                        (cand_id,),
                    )
                    if c_skills:
                        render_styled_table(pd.DataFrame(c_skills))
                    else:
                        st.info("No skills linked yet.")


# =========================================================
# PAGE 6: APPLICATIONS
# =========================================================
elif current_page == "Applications":
    render_page_header(
        "Applications",
        "Process candidate applications, verify attached resumes, and transition pipeline stages."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        tab_app_v, tab_app_s, tab_app_p = st.tabs(["Application Log", "Submit Application", "Status Transition (Stored Procedure)"])

        with tab_app_v:
            col_ap1, col_ap2, col_ap3, col_ap4 = st.columns([2, 1, 1, 1])
            with col_ap1:
                search_app = st.text_input("Search applications", "", placeholder="Search candidate or position...", key="app_search")
            with col_ap2:
                filt_st = st.selectbox("Pipeline Stage", ["All Stages", "Applied", "Screening", "Interview", "Offered", "Rejected", "Hired"], key="app_st_filt")
            with col_ap3:
                companies = load_companies()
                filt_emp = st.selectbox("Employer", ["All Employers"] + [c["company_name"] for c in (companies or [])], key="app_emp_filt")
            with col_ap4:
                sort_app = st.selectbox("Sort By", ["Newest First", "Oldest First", "Candidate (A-Z)"], key="app_sort")

            sql = """
                SELECT a.full_name AS "Candidate", j.job_title AS "Position", c.company_name AS "Employer",
                       ap.status AS "Stage", ap.applied_date AS "Applied Date",
                       r.file_name AS "Verified Resume", ap.application_id AS "ID"
                FROM applications ap
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                JOIN resumes r ON ap.resume_id = r.resume_id
                WHERE 1=1
            """
            params_ap = []
            if filt_st != "All Stages":
                sql += " AND ap.status = %s"
                params_ap.append(filt_st)
            if filt_emp != "All Employers":
                sql += " AND c.company_name = %s"
                params_ap.append(filt_emp)
            if search_app.strip():
                sql += " AND (a.full_name ILIKE %s OR j.job_title ILIKE %s)"
                kw = f"%{search_app.strip()}%"
                params_ap.extend([kw, kw])

            if sort_app == "Newest First":
                sql += " ORDER BY ap.applied_date DESC, ap.application_id DESC;"
            elif sort_app == "Oldest First":
                sql += " ORDER BY ap.applied_date ASC, ap.application_id ASC;"
            else:
                sql += " ORDER BY a.full_name ASC;"

            apps_df = pd.DataFrame(execute_query(sql, tuple(params_ap) if params_ap else None))
            render_styled_table(apps_df)

        with tab_app_s:
            applicants = load_applicants()
            jobs = load_jobs(open_only=True)

            if applicants and jobs:
                a_map = {f"{a['full_name']} ({a['email']})": a["applicant_id"] for a in applicants}
                j_map = {f"{j['job_title']} @ {j['company_name']} (${float(j['salary']):,.0f})": j["job_id"] for j in jobs}

                sel_cand_lbl = st.selectbox("1. Candidate *", list(a_map.keys()), key="app_cand_sel")
                cid = a_map[sel_cand_lbl]

                sel_job_lbl = st.selectbox("2. Job Requisition *", list(j_map.keys()), key="app_job_sel")
                jid = j_map[sel_job_lbl]

                cand_res = load_resumes(applicant_id=cid)
                if not cand_res:
                    st.warning("⚠️ Candidate has no resume document on file. Please upload one under 'Applicants & Resumes' first.")
                else:
                    res_map = {f"{r['file_name']} (Uploaded: {r['uploaded_date']})": r["resume_id"] for r in cand_res}
                    sel_res_lbl = st.selectbox("3. Candidate Verified Resume *", list(res_map.keys()), key="app_res_sel")
                    rid = res_map[sel_res_lbl]

                    with st.form("sub_app_form"):
                        submit_app_btn = st.form_submit_button("Submit Application")
                        if submit_app_btn:
                            if require_auth():
                                try:
                                    existing = execute_query(
                                        "SELECT application_id FROM applications WHERE applicant_id = %s AND job_id = %s;",
                                        (cid, jid),
                                    )
                                    if existing:
                                        st.error("Duplicate application prevented: Candidate has already applied for this requisition.")
                                    else:
                                        execute_query(
                                            "INSERT INTO applications (applicant_id, job_id, resume_id, applied_date, status) VALUES (%s, %s, %s, CURRENT_DATE, 'Applied');",
                                            (cid, jid, rid),
                                            fetch=False,
                                            commit=True,
                                        )
                                        st.success("Application submitted successfully.")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Submission failed: {e}")

        with tab_app_p:
            st.markdown('<div class="card-title">Advance Stage via Stored Procedure</div>', unsafe_allow_html=True)
            st.caption("Executes `CALL update_application_status(p_application_id, p_new_status);` with relational domain validation.")

            apps = execute_query("""
                SELECT ap.application_id, a.full_name AS candidate, j.job_title, c.company_name, ap.status, j.company_id
                FROM applications ap
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                ORDER BY ap.application_id ASC;
            """)

            if apps:
                app_options = {
                    f"App #{a['application_id']}: {a['candidate']} - {a['job_title']} @ {a['company_name']} (Current: {a['status']})": a
                    for a in apps
                }
                sel_app_k = st.selectbox("Select Application", list(app_options.keys()), key="proc_app_sel")
                sel_app_obj = app_options[sel_app_k]

                rec_cid = get_current_recruiter_company_id()
                is_authorized = (rec_cid is None or int(rec_cid) == int(sel_app_obj["company_id"]))

                with st.form("proc_status_form"):
                    allowed_st = ["Applied", "Screening", "Interview", "Offered", "Rejected", "Hired"]
                    new_st = st.selectbox(
                        "New Status Stage",
                        allowed_st,
                        index=allowed_st.index(sel_app_obj["status"]) if sel_app_obj["status"] in allowed_st else 0,
                    )
                    sub_proc = st.form_submit_button("Execute Status Transition")

                    if sub_proc:
                        if require_auth():
                            if not is_authorized:
                                st.error("⛔ Tenant Isolation: You cannot transition application stages for another organization.")
                            else:
                                try:
                                    execute_procedure("update_application_status", (sel_app_obj["application_id"], new_st))
                                    st.success(f"Stored procedure executed. Application #{sel_app_obj['application_id']} transitioned to '{new_st}'.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Procedure error: {e}")


# =========================================================
# PAGE 7: INTERVIEWS
# =========================================================
elif current_page == "Interviews":
    render_page_header(
        "Interviews",
        "Schedule candidate interviews, log technical evaluations, and sync recruitment stages."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        is_int_jump = (st.session_state.get("jump_to_action") == "schedule_interview")
        if is_int_jump:
            c_banner1, c_banner2 = st.columns([4, 1])
            c_banner1.info("⚡ Quick Action: Schedule an interview for an active candidate requisition below.")
            if c_banner2.button("← Directory", key="exit_qa_int"):
                st.session_state["jump_to_action"] = None
                st.rerun()
            tab_int_s, tab_int_v, tab_int_f = st.tabs(["Schedule Interview", "Interview Pipeline", "Log Evaluation Feedback"])
        else:
            tab_int_v, tab_int_s, tab_int_f = st.tabs(["Interview Pipeline", "Schedule Interview", "Log Evaluation Feedback"])

        with tab_int_v:
            col_i1, col_i2, col_i3, col_i4 = st.columns([2, 1, 1, 1])
            with col_i1:
                search_int = st.text_input("Search interviews", "", placeholder="Search candidate, position, employer...", key="int_search")
            with col_i2:
                filt_int = st.selectbox("Status", ["All Statuses", "Scheduled", "Completed", "Cancelled"], key="int_st_filt")
            with col_i3:
                filt_fmt = st.selectbox("Format", ["All Formats", "Video", "Phone", "In-Person"], key="int_fmt_filt")
            with col_i4:
                sort_int = st.selectbox("Sort By", ["Date (Earliest)", "Date (Latest)", "Candidate (A-Z)"], key="int_sort")

            sql = """
                SELECT a.full_name AS "Candidate", j.job_title AS "Position", c.company_name AS "Employer",
                       i.interview_date AS "Scheduled Time", i.interview_type AS "Format", i.status AS "Status",
                       i.feedback AS "Evaluation Notes", i.interview_id AS "ID"
                FROM interviews i
                JOIN applications ap ON i.application_id = ap.application_id
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                WHERE 1=1
            """
            params_int = []
            if filt_int != "All Statuses":
                sql += " AND i.status = %s"
                params_int.append(filt_int)
            if filt_fmt != "All Formats":
                sql += " AND i.interview_type = %s"
                params_int.append(filt_fmt)
            if search_int.strip():
                sql += " AND (a.full_name ILIKE %s OR j.job_title ILIKE %s OR c.company_name ILIKE %s)"
                kw = f"%{search_int.strip()}%"
                params_int.extend([kw, kw, kw])

            if sort_int == "Date (Earliest)":
                sql += " ORDER BY i.interview_date ASC;"
            elif sort_int == "Date (Latest)":
                sql += " ORDER BY i.interview_date DESC;"
            else:
                sql += " ORDER BY a.full_name ASC;"

            interviews_df = pd.DataFrame(execute_query(sql, tuple(params_int) if params_int else None))
            render_styled_table(interviews_df)

        with tab_int_s:
            apps = execute_query("""
                SELECT ap.application_id, a.full_name AS candidate, j.job_title, c.company_name, ap.status, j.company_id
                FROM applications ap
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                WHERE ap.status NOT IN ('Rejected', 'Hired')
                ORDER BY ap.application_id DESC;
            """)

            if not apps:
                st.warning("No eligible active applications found.")
            else:
                app_dict = {
                    f"App #{a['application_id']}: {a['candidate']} - {a['job_title']} @ {a['company_name']} ({a['status']})": a
                    for a in apps
                }
                with st.form("sched_int_form"):
                    sel_app_lbl = st.selectbox("Select Application *", list(app_dict.keys()))
                    sel_app = app_dict[sel_app_lbl]

                    col_dt1, col_dt2 = st.columns(2)
                    with col_dt1:
                        int_d = st.date_input("Interview Date *", datetime.date.today() + datetime.timedelta(days=2))
                    with col_dt2:
                        int_t = st.time_input("Interview Time *", datetime.time(10, 0))
                    int_fmt = st.selectbox("Interview Format *", ["Video", "Phone", "In-Person"])
                    int_notes = st.text_area("Initial Agenda & Notes", placeholder="Technical screen: System architecture & problem solving.")
                    submit_int = st.form_submit_button("Schedule via Stored Procedure")

                    if submit_int:
                        if require_auth():
                            rec_cid = get_current_recruiter_company_id()
                            if rec_cid and int(rec_cid) != int(sel_app["company_id"]):
                                st.error("⛔ Tenant Isolation: You cannot schedule interviews for positions outside your company.")
                            else:
                                try:
                                    aid = sel_app["application_id"]
                                    int_dt = datetime.datetime.combine(int_d, int_t)
                                    execute_procedure("schedule_interview", (aid, int_dt, int_fmt, int_notes.strip()))
                                    st.success("Interview scheduled and application status synchronized to 'Interview'.")
                                    st.session_state["jump_to_action"] = None
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Scheduling failed: {e}")

        with tab_int_f:
            interviews = execute_query("""
                SELECT i.interview_id, a.full_name AS candidate, j.job_title, i.interview_date, i.status, i.feedback, j.company_id
                FROM interviews i
                JOIN applications ap ON i.application_id = ap.application_id
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                ORDER BY i.interview_date DESC;
            """)
            if interviews:
                int_opts = {f"Interview #{i['interview_id']}: {i['candidate']} ({i['job_title']}) - {i['status']}": i for i in interviews}
                sel_int_lbl = st.selectbox("Select Interview Record", list(int_opts.keys()))
                sel_int_obj = int_opts[sel_int_lbl]

                rec_cid = get_current_recruiter_company_id()
                is_authorized = (rec_cid is None or int(rec_cid) == int(sel_int_obj["company_id"]))

                with st.form("upd_int_form"):
                    u_istatus = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"], index=["Scheduled", "Completed", "Cancelled"].index(sel_int_obj["status"]))
                    u_ifeedback = st.text_area("Evaluation Notes & Score", value=sel_int_obj["feedback"] or "")
                    submit_u_int = st.form_submit_button("Save Feedback")

                    if submit_u_int:
                        if require_auth():
                            if not is_authorized:
                                st.error("⛔ Tenant Isolation: You cannot update interview evaluations for another organization.")
                            else:
                                try:
                                    execute_query(
                                        "UPDATE interviews SET status = %s, feedback = %s WHERE interview_id = %s;",
                                        (u_istatus, u_ifeedback.strip(), sel_int_obj["interview_id"]),
                                        fetch=False,
                                        commit=True,
                                    )
                                    st.success("Interview evaluation saved.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Update failed: {e}")


# =========================================================
# PAGE 8: HIRING DECISIONS
# =========================================================
elif current_page == "Hiring Decisions":
    render_page_header(
        "Hiring Decisions",
        "Record final employment outcomes, offer details, and maintain recruitment velocity audit trails."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        tab_hd_v, tab_hd_r = st.tabs(["Decisions History", "Record Final Decision"])

        with tab_hd_v:
            col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
            with col_h1:
                search_hd = st.text_input("Search decisions", "", placeholder="Search candidate, position, employer...", key="hd_search")
            with col_h2:
                filt_dec = st.selectbox("Outcome", ["All Outcomes", "Hired", "Rejected", "Pending"], key="hd_out_filt")
            with col_h3:
                sort_hd = st.selectbox("Sort By", ["Decision Date (Newest)", "Decision Date (Oldest)", "Pipeline Days (Longest)"], key="hd_sort")

            sql = """
                SELECT a.full_name AS "Candidate", j.job_title AS "Position", c.company_name AS "Employer",
                       hd.decision AS "Decision", hd.decision_date AS "Decision Date",
                       (hd.decision_date - ap.applied_date) AS "Days in Pipeline",
                       hd.remarks AS "Offer Terms / Remarks", hd.decision_id AS "ID"
                FROM hiring_decisions hd
                JOIN applications ap ON hd.application_id = ap.application_id
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                WHERE 1=1
            """
            params_hd = []
            if filt_dec != "All Outcomes":
                sql += " AND hd.decision = %s"
                params_hd.append(filt_dec)
            if search_hd.strip():
                sql += " AND (a.full_name ILIKE %s OR j.job_title ILIKE %s OR c.company_name ILIKE %s)"
                kw = f"%{search_hd.strip()}%"
                params_hd.extend([kw, kw, kw])

            if sort_hd == "Decision Date (Newest)":
                sql += " ORDER BY hd.decision_date DESC, hd.decision_id DESC;"
            elif sort_hd == "Decision Date (Oldest)":
                sql += " ORDER BY hd.decision_date ASC, hd.decision_id ASC;"
            else:
                sql += " ORDER BY (hd.decision_date - ap.applied_date) DESC NULLS LAST;"

            decisions_df = pd.DataFrame(execute_query(sql, tuple(params_hd) if params_hd else None))
            render_styled_table(decisions_df)

        with tab_hd_r:
            eligible_apps = execute_query("""
                SELECT ap.application_id, a.full_name AS candidate, j.job_title, c.company_name, ap.status, j.company_id
                FROM applications ap
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                WHERE ap.application_id NOT IN (SELECT application_id FROM hiring_decisions)
                ORDER BY ap.application_id DESC;
            """)

            if not eligible_apps:
                st.info("All existing applications currently have a final decision recorded.")
            else:
                app_dict = {
                    f"App #{a['application_id']}: {a['candidate']} - {a['job_title']} @ {a['company_name']} ({a['status']})": a
                    for a in eligible_apps
                }

                with st.form("rec_dec_form"):
                    sel_app_lbl = st.selectbox("Select Application *", list(app_dict.keys()))
                    sel_app_obj = app_dict[sel_app_lbl]
                    dec_val = st.selectbox("Decision Outcome *", ["Hired", "Rejected", "Pending"])
                    rem = st.text_area("Remarks / Offer Terms", placeholder="Candidate accepted formal offer starting next month.")
                    sub_dec = st.form_submit_button("Record Decision")

                    if sub_dec:
                        if require_auth():
                            rec_cid = get_current_recruiter_company_id()
                            if rec_cid and int(rec_cid) != int(sel_app_obj["company_id"]):
                                st.error("⛔ Tenant Isolation: You cannot record hiring decisions for other organizations.")
                            else:
                                try:
                                    aid = sel_app_obj["application_id"]
                                    execute_query(
                                        "INSERT INTO hiring_decisions (application_id, decision, decision_date, remarks) VALUES (%s, %s, CURRENT_DATE, %s);",
                                        (aid, dec_val, rem.strip()),
                                        fetch=False,
                                        commit=True,
                                    )
                                    if dec_val in ("Hired", "Rejected"):
                                        execute_procedure("update_application_status", (aid, dec_val))
                                    st.success(f"Decision '{dec_val}' recorded successfully.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to record decision: {e}")


# =========================================================
# PAGE 9: SKILLS MANAGEMENT
# =========================================================
elif current_page == "Skills Management":
    render_page_header(
        "Skills & Requirements",
        "Maintain master technical skill catalogs, candidate endorsements, and job requisition requirements."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        tab_sk_c, tab_sk_a, tab_sk_j, tab_sk_m = st.tabs(["Skills Catalog", "Candidate Skills", "Job Skill Requirements", "Skills Matrix"])

        with tab_sk_c:
            col_sc1, col_sc2 = st.columns(2)
            with col_sc1:
                st.markdown('<div class="card-title">Standardized Skills Catalog</div>', unsafe_allow_html=True)
                skills = execute_query("SELECT skill_name AS \"Skill Name\", skill_id AS \"ID\" FROM skills ORDER BY skill_name;")
                if skills:
                    render_styled_table(pd.DataFrame(skills))
            with col_sc2:
                st.markdown('<div class="card-title">Register New Skill</div>', unsafe_allow_html=True)
                with st.form("add_sk_form", clear_on_submit=True):
                    new_sk = st.text_input("Skill Name *", placeholder="e.g. GraphQL, Kubernetes")
                    submit_sk = st.form_submit_button("Add Skill")
                    if submit_sk:
                        if require_auth():
                            if not new_sk.strip():
                                st.error("Skill name cannot be empty.")
                            else:
                                try:
                                    execute_query("INSERT INTO skills (skill_name) VALUES (%s);", (new_sk.strip(),), fetch=False, commit=True)
                                    st.success(f"Skill '{new_sk}' added.")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")

        with tab_sk_a:
            applicants = load_applicants()
            skills = load_skills()
            if applicants and skills:
                a_map = {f"{a['full_name']} ({a['email']})": a["applicant_id"] for a in applicants}
                s_map = {s["skill_name"]: s["skill_id"] for s in skills}

                with st.form("assign_cand_sk_form"):
                    sel_a = st.selectbox("Candidate", list(a_map.keys()))
                    sel_s = st.selectbox("Skill", list(s_map.keys()))
                    prof = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1)
                    sub_ask = st.form_submit_button("Assign Competency")
                    if sub_ask:
                        if require_auth():
                            try:
                                execute_query(
                                    """
                                    INSERT INTO applicant_skills (applicant_id, skill_id, proficiency_level)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (applicant_id, skill_id) DO UPDATE SET proficiency_level = EXCLUDED.proficiency_level;
                                    """,
                                    (a_map[sel_a], s_map[sel_s], prof),
                                    fetch=False,
                                    commit=True,
                                )
                                st.success("Candidate competency endorsed.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Assignment failed: {e}")

        with tab_sk_j:
            jobs = load_jobs(open_only=True)
            skills = load_skills()
            if jobs and skills:
                j_map = {f"{j['job_title']} @ {j['company_name']} (ID: {j['job_id']})": j["job_id"] for j in jobs}
                s_map = {s["skill_name"]: s["skill_id"] for s in skills}
                sel_j = st.selectbox("Select Requisition", list(j_map.keys()), key="sel_j_req_sk")
                jid = j_map[sel_j]

                cur_reqs = execute_query(
                    "SELECT s.skill_name AS \"Competency\", js.required_level AS \"Minimum Required Level\" FROM job_skills js JOIN skills s ON js.skill_id = s.skill_id WHERE js.job_id = %s ORDER BY s.skill_name;",
                    (jid,),
                )
                if cur_reqs:
                    st.markdown('<div class="card-title">Currently Required Competencies</div>', unsafe_allow_html=True)
                    render_styled_table(pd.DataFrame(cur_reqs))

                with st.form("add_req_sk_form"):
                    req_s = st.selectbox("Add Competency Requirement", list(s_map.keys()))
                    req_l = st.selectbox("Required Minimum Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1)
                    sub_jsk = st.form_submit_button("Add Requirement")
                    if sub_jsk:
                        if require_auth():
                            try:
                                execute_query(
                                    """
                                    INSERT INTO job_skills (job_id, skill_id, required_level)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (job_id, skill_id) DO UPDATE SET required_level = EXCLUDED.required_level;
                                    """,
                                    (jid, s_map[req_s], req_l),
                                    fetch=False,
                                    commit=True,
                                )
                                st.success(f"Requirement '{req_s}' mapped to job.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")

        with tab_sk_m:
            matrix_data = execute_query("""
                SELECT a.full_name AS "Candidate", s.skill_name AS "Competency", aps.proficiency_level AS "Endorsed Level"
                FROM applicants a
                JOIN applicant_skills aps ON a.applicant_id = aps.applicant_id
                JOIN skills s ON aps.skill_id = s.skill_id
                ORDER BY a.full_name, s.skill_name;
            """)
            if matrix_data:
                render_styled_table(pd.DataFrame(matrix_data))


# =========================================================
# PAGE 10: CANDIDATE SKILL MATCHING
# =========================================================
elif current_page == "Candidate Skill Matching":
    render_page_header(
        "Candidate Skill Matching",
        "Transparent SQL-based ranking engine comparing candidate competencies with requisition requirements."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        jobs = load_jobs(open_only=True)
        if not jobs:
            st.info("No active job requisitions available.")
        else:
            job_dict = {f"{j['job_title']} @ {j['company_name']} (ID: {j['job_id']})": j for j in jobs}
            sel_job_lbl = st.selectbox("Select Target Job Requisition", list(job_dict.keys()), key="match_job_select")
            target_job = job_dict[sel_job_lbl]
            target_jid = target_job["job_id"]

            st.markdown(
                f"""
                <div style="padding: 16px 20px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 8px; margin: 12px 0 18px 0;">
                    <div style="font-size: 17px; font-weight: 700; color: #111111;">{target_job['job_title']} • {target_job['company_name']}</div>
                    <div style="font-size: 14px; color: #475569; font-weight: 500; margin-top: 4px;">📍 {target_job['location']} • 💰 ${float(target_job['salary']):,.0f} Annual Compensation</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            job_reqs = execute_query(
                "SELECT s.skill_id, s.skill_name, js.required_level FROM job_skills js JOIN skills s ON js.skill_id = s.skill_id WHERE js.job_id = %s ORDER BY s.skill_name;",
                (target_jid,),
            )

            if not job_reqs:
                st.info("ℹ️ No competencies are currently mapped to this position. To enable candidate matching, add required skills under **Skills Management**.")
            else:
                req_badges = [f"<span style='display:inline-block; padding: 4px 10px; background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 5px; font-size: 13.5px; font-weight: 600; color: #1F2937; margin: 3px;'>{r['skill_name']} ({r['required_level']})</span>" for r in job_reqs]
                st.markdown(f"<div style='font-size: 14.5px; font-weight: 600; color: #111111; margin-bottom: 8px;'>Required Competencies ({len(job_reqs)}):</div>" + " ".join(req_badges), unsafe_allow_html=True)
                total_req = len(job_reqs)
                req_names = {r["skill_id"]: r["skill_name"] for r in job_reqs}

                ranking_sql = """
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
                ranked = execute_query(ranking_sql, (total_req, target_jid))

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">Ranked Candidate Matches</div>', unsafe_allow_html=True)

                if ranked:
                    df_r = pd.DataFrame(ranked).drop(columns=["applicant_id"])
                    render_styled_table(df_r)

                    top = ranked[0]
                    if top['Matched Competencies'] > 0:
                        st.markdown(
                            f"""
                            <div style="padding: 16px 20px; background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; margin: 16px 0;">
                                <div style="font-size: 16px; font-weight: 700; color: #15803D;">Top Match: {top['Candidate']} ({top['Match %']}%)</div>
                                <div style="font-size: 14px; font-weight: 500; color: #166534; margin-top: 3px;">{top['Matched Competencies']} of {total_req} competencies matched: {top['Matched Skills']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.info("No candidates in the talent pool currently match any of the required competencies for this position.")

                    # Individual Candidate Gap Inspection
                    st.markdown('<div class="section-title" style="margin-top: 24px;">Competency Gap Breakdown</div>', unsafe_allow_html=True)
                    cand_opts = {f"{c['Candidate']} ({c['Match %']}%)": c for c in ranked}
                    sel_cand_k = st.selectbox("Inspect Candidate", list(cand_opts.keys()))
                    ci_cand = cand_opts[sel_cand_k]
                    ci_aid = ci_cand["applicant_id"]

                    cand_skills_data = execute_query("SELECT skill_id, proficiency_level FROM applicant_skills WHERE applicant_id = %s;", (ci_aid,))
                    cand_s_map = {cs["skill_id"]: cs["proficiency_level"] for cs in (cand_skills_data or [])}

                    gap_list = []
                    for rid, rname in req_names.items():
                        if rid in cand_s_map:
                            gap_list.append({"Competency": rname, "Status": "Matched", "Proficiency": cand_s_map[rid]})
                        else:
                            gap_list.append({"Competency": rname, "Status": "Missing", "Proficiency": "Not Endorsed"})
                    render_styled_table(pd.DataFrame(gap_list))

                    # Action button
                    existing_app = execute_query(
                        "SELECT application_id FROM applications WHERE applicant_id = %s AND job_id = %s;",
                        (ci_aid, target_jid),
                    )
                    if existing_app:
                        st.info(f"Candidate {ci_cand['Candidate']} has application #{existing_app[0]['application_id']} on file.")
                    else:
                        if st.button(f"Submit Application for {ci_cand['Candidate']}", key="btn_match_sub"):
                            if require_auth():
                                r_res = load_resumes(applicant_id=ci_aid)
                                if not r_res:
                                    st.error("Candidate has no resume on file.")
                                else:
                                    execute_query(
                                        "INSERT INTO applications (applicant_id, job_id, resume_id, applied_date, status) VALUES (%s, %s, %s, CURRENT_DATE, 'Applied');",
                                        (ci_aid, target_jid, r_res[0]["resume_id"]),
                                        fetch=False,
                                        commit=True,
                                    )
                                    st.success("Application created.")
                                    st.rerun()
                else:
                    st.info("No candidates available for skill matching.")


# =========================================================
# PAGE 11: REPORTS & ANALYTICS
# =========================================================
elif current_page == "Reports & Analytics":
    render_page_header(
        "Reports & Analytics",
        "Comprehensive database views, operational audit logs, and compliance CSV exports."
    )

    if not db_ok:
        st.error(f"Database error: {db_status_msg}")
    else:
        rep_options = [
            "Company Recruitment Summary (View)",
            "Applicant Application Details (View)",
            "Applications by Company",
            "Applications by Job Requisition",
            "Applicants by Technical Skill",
            "Comprehensive Interview Schedule Audit",
            "Hiring Decisions & Pipeline Velocity",
            "Candidate Skill Matching Report",
        ]
        sel_rep = st.selectbox("Select Audit Report", rep_options, key="rep_sel_box")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # White Report Card Container with Subtle Border
        st.markdown("<div style='background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 22px 24px; margin-bottom: 20px;'>", unsafe_allow_html=True)

        if sel_rep == "Company Recruitment Summary (View)":
            st.markdown('<div class="card-title">Company Recruitment Summary</div>', unsafe_allow_html=True)
            st.caption("Leverages database view `recruitment_summary_view` joining companies, jobs, and applications.")
            data = execute_query("SELECT * FROM recruitment_summary_view ORDER BY company_name;")
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "recruitment_summary_view.csv", "text/csv")

        elif sel_rep == "Applicant Application Details (View)":
            st.markdown('<div class="card-title">Applicant Application Details</div>', unsafe_allow_html=True)
            st.caption("Consolidated pipeline view `applicant_application_view` spanning candidates, requisitions, and employer accounts.")
            data = execute_query("SELECT * FROM applicant_application_view ORDER BY application_id;")
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "applicant_application_view.csv", "text/csv")

        elif sel_rep == "Applications by Company":
            st.markdown('<div class="card-title">Applications by Employer Organization</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT c.company_name, c.industry, COUNT(ap.application_id) AS total_applications
                FROM companies c
                LEFT JOIN jobs j ON c.company_id = j.company_id
                LEFT JOIN applications ap ON j.job_id = ap.job_id
                GROUP BY c.company_name, c.industry
                ORDER BY total_applications DESC;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "applications_by_company.csv", "text/csv")

        elif sel_rep == "Applications by Job Requisition":
            st.markdown('<div class="card-title">Applications by Requisition (HAVING Clause)</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT j.job_id, j.job_title, c.company_name, j.salary, j.status, COUNT(ap.application_id) AS total_applications
                FROM jobs j
                JOIN companies c ON j.company_id = c.company_id
                LEFT JOIN applications ap ON j.job_id = ap.job_id
                GROUP BY j.job_id, j.job_title, c.company_name, j.salary, j.status
                ORDER BY total_applications DESC;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "applications_by_job.csv", "text/csv")

        elif sel_rep == "Applicants by Technical Skill":
            st.markdown('<div class="card-title">Applicants by Technical Skill</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT s.skill_name, COUNT(aps.applicant_id) AS candidate_count,
                       STRING_AGG(a.full_name, ', ' ORDER BY a.full_name) AS candidates
                FROM skills s
                LEFT JOIN applicant_skills aps ON s.skill_id = aps.skill_id
                LEFT JOIN applicants a ON aps.applicant_id = a.applicant_id
                GROUP BY s.skill_name
                ORDER BY candidate_count DESC, s.skill_name;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "applicants_by_skill.csv", "text/csv")

        elif sel_rep == "Comprehensive Interview Schedule Audit":
            st.markdown('<div class="card-title">Interview Schedule Audit Log</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT i.interview_id, a.full_name AS candidate, a.email, j.job_title, c.company_name,
                       i.interview_date, i.interview_type AS format, i.status, i.feedback
                FROM interviews i
                JOIN applications ap ON i.application_id = ap.application_id
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                ORDER BY i.interview_date ASC;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "interview_audit_log.csv", "text/csv")

        elif sel_rep == "Hiring Decisions & Pipeline Velocity":
            st.markdown('<div class="card-title">Hiring Outcomes & Pipeline Velocity</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT hd.decision_id, a.full_name AS candidate, j.job_title, c.company_name,
                       ap.applied_date, hd.decision_date,
                       (hd.decision_date - ap.applied_date) AS days_in_pipeline,
                       hd.decision, hd.remarks
                FROM hiring_decisions hd
                JOIN applications ap ON hd.application_id = ap.application_id
                JOIN applicants a ON ap.applicant_id = a.applicant_id
                JOIN jobs j ON ap.job_id = j.job_id
                JOIN companies c ON j.company_id = c.company_id
                ORDER BY hd.decision_date DESC;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "hiring_decisions_report.csv", "text/csv")

        elif sel_rep == "Candidate Skill Matching Report":
            st.markdown('<div class="card-title">Candidate Skill Matching Benchmark</div>', unsafe_allow_html=True)
            data = execute_query("""
                SELECT
                    j.job_title,
                    c.company_name,
                    a.full_name AS candidate_name,
                    COUNT(js.skill_id) AS matching_skills,
                    ROUND(100.0 * COUNT(js.skill_id) / NULLIF((SELECT COUNT(*) FROM job_skills WHERE job_id = j.job_id), 0), 1) AS match_pct
                FROM jobs j
                JOIN companies c ON j.company_id = c.company_id
                JOIN job_skills js ON j.job_id = js.job_id
                JOIN applicant_skills aps ON js.skill_id = aps.skill_id
                JOIN applicants a ON aps.applicant_id = a.applicant_id
                GROUP BY j.job_id, j.job_title, c.company_name, a.applicant_id, a.full_name
                ORDER BY j.job_title, matching_skills DESC;
            """)
            if data:
                df = pd.DataFrame(data)
                render_styled_table(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "candidate_skill_matching_report.csv", "text/csv")

        st.markdown("</div>", unsafe_allow_html=True)
