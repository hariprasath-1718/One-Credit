import datetime
import html
import time
from typing import Any, Dict, List, Optional
import pandas as pd
import requests
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="EduSphere • Student Management Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Constants & Configuration
# ---------------------------------------------------------
API_URL = "http://127.0.0.1:8000"

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics & Communication",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Data Science & AI",
    "Business Administration",
]

DEPT_COLORS = {
    "Computer Science": {"bg": "rgba(6, 182, 212, 0.15)", "text": "#38bdf8", "border": "#0284c7"},
    "Information Technology": {"bg": "rgba(59, 130, 246, 0.15)", "text": "#60a5fa", "border": "#2563eb"},
    "Electronics & Communication": {"bg": "rgba(16, 185, 129, 0.15)", "text": "#34d399", "border": "#059669"},
    "Electrical Engineering": {"bg": "rgba(245, 158, 11, 0.15)", "text": "#fbbf24", "border": "#d97706"},
    "Mechanical Engineering": {"bg": "rgba(249, 115, 22, 0.15)", "text": "#fb923c", "border": "#ea580c"},
    "Civil Engineering": {"bg": "rgba(244, 63, 94, 0.15)", "text": "#fb7185", "border": "#e11d48"},
    "Data Science & AI": {"bg": "rgba(168, 85, 247, 0.15)", "text": "#c084fc", "border": "#9333ea"},
    "Business Administration": {"bg": "rgba(99, 102, 241, 0.15)", "text": "#818cf8", "border": "#4f46e5"},
}

# ---------------------------------------------------------
# Custom Styling & Glassmorphic CSS
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

h1, h2, h3, .font-heading {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em;
}

/* App Background Subtle Glow */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.05) 0%, transparent 60%);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(17, 24, 39, 0.98) 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* Glassmorphic Cards */
.glass-panel {
    background: rgba(30, 41, 59, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-panel:hover {
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 12px 36px 0 rgba(99, 102, 241, 0.12);
}

/* Stat Metric Card */
.metric-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.metric-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.4);
    border-color: rgba(99, 102, 241, 0.4);
}

.metric-box::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #06b6d4);
}

.metric-title {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
    margin-bottom: 6px;
}

.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.1;
}

.metric-desc {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Live Student ID Badge Card */
.id-card {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 60%, #1e293b 100%);
    border: 1px solid rgba(129, 140, 248, 0.35);
    border-radius: 20px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.3);
    color: #f8fafc;
}

.id-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
    pointer-events: none;
}

.id-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 14px;
    margin-bottom: 18px;
}

.id-card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #a5b4fc;
}

.id-chip {
    width: 32px;
    height: 24px;
    background: linear-gradient(135deg, #fcd34d 0%, #d97706 100%);
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.2);
}

.id-avatar {
    width: 68px;
    height: 68px;
    border-radius: 16px;
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    box-shadow: 0 8px 16px rgba(99, 102, 241, 0.35);
    border: 2px solid rgba(255, 255, 255, 0.2);
}

/* Department Badges */
.dept-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: 1px solid;
    margin-top: 4px;
}

/* Live Status Pulse Dot */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 20px;
}

.status-online {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-offline {
    background: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: currentColor;
    box-shadow: 0 0 10px currentColor;
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.25); opacity: 1; }
    100% { transform: scale(0.95); opacity: 0.8; }
}

/* Student Directory Grid Cards */
.student-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 18px;
    transition: all 0.2s ease;
    height: 100%;
}

.student-card:hover {
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(99, 102, 241, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 10px 24px -6px rgba(0, 0, 0, 0.3);
}

/* Streamlit Button Tweaks */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.25) !important;
}

/* Primary Action Buttons */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    border: 1px solid #818cf8 !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
}

/* Inputs refinement */
div[data-baseweb="input"], div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* Modern Pill Badges */
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 30px;
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), rgba(6, 182, 212, 0.15));
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 12px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Helper Functions & Backend Connectivity
# ---------------------------------------------------------
def check_backend_status() -> Dict[str, Any]:
    """Test health and latency of the FastAPI backend."""
    start = time.perf_counter()
    try:
        res = requests.get(f"{API_URL}/", timeout=2)
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        if res.status_code == 200:
            return {"online": True, "latency": latency_ms, "msg": "API Online"}
        return {"online": False, "latency": None, "msg": f"Status {res.status_code}"}
    except Exception:
        return {"online": False, "latency": None, "msg": "Offline"}


def extract_error_message(response: requests.Response) -> str:
    """Helper function to extract human-readable error from FastAPI."""
    try:
        error_data = response.json()
        detail = error_data.get("detail", "An unexpected error occurred.")
        if isinstance(detail, list):
            messages = []
            for err in detail:
                field = err.get("loc", ["field"])[-1]
                msg = err.get("msg", "Invalid value")
                messages.append(f"{field}: {msg}")
            return "; ".join(messages)
        return str(detail)
    except Exception:
        return f"Request failed with status code {response.status_code}."


def fetch_all_students() -> Optional[List[Dict[str, Any]]]:
    """Retrieve full list of students with error handling."""
    try:
        response = requests.get(f"{API_URL}/students", timeout=4)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def get_initials(name: str) -> str:
    """Generate up to 2 uppercase initials for avatars."""
    cleaned = "".join([c for c in name if c.isalnum() or c.isspace()]).strip()
    parts = cleaned.split()
    if not parts:
        return "ST"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()


def render_dept_badge(dept: str) -> str:
    """Generate HTML pill badge for a department."""
    cfg = DEPT_COLORS.get(
        dept,
        {"bg": "rgba(148, 163, 184, 0.15)", "text": "#cbd5e1", "border": "#64748b"}
    )
    safe_dept = html.escape(dept)
    return (
        f'<span class="dept-pill" style="background-color: {cfg["bg"]}; '
        f'color: {cfg["text"]}; border-color: {cfg["border"]};">'
        f'{safe_dept}</span>'
    )


# ---------------------------------------------------------
# Sidebar Component
# ---------------------------------------------------------
backend_info = check_backend_status()

with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 2.2rem; background: linear-gradient(135deg, #6366f1, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎓</div>
            <div>
                <div style="font-family: 'Outfit'; font-size: 1.25rem; font-weight: 800; color: #f8fafc; line-height: 1.1;">EduSphere</div>
                <div style="font-size: 0.72rem; color: #94a3b8; letter-spacing: 0.05em; text-transform: uppercase;">FASTAPI • SQLITE • STREAMLIT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Backend Connection Status Pill
    if backend_info["online"]:
        st.markdown(
            f"""
            <div class="status-indicator status-online" style="margin-bottom: 20px;">
                <span class="pulse-dot"></span>
                <span>FastAPI Backend Active</span>
                <span style="font-size: 0.7rem; opacity: 0.8; margin-left: auto;">{backend_info['latency']} ms</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="status-indicator status-offline" style="margin-bottom: 20px;">
                <span class="pulse-dot"></span>
                <span>Backend Disconnected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("⚠️ Run: `python -m uvicorn backend.main:app --reload`")

    st.markdown('<div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: #64748b; letter-spacing: 0.08em; margin-bottom: 8px;">Workspace Views</div>', unsafe_allow_html=True)
    menu_options = [
        "📊 Dashboard Overview",
        "✨ Add New Student",
        "📋 Directory & Records",
        "🔍 Search & Lookup",
        "✏️ Modify Record",
        "🗑️ Delete Student",
    ]
    choice = st.radio("Navigation Menu", menu_options, label_visibility="collapsed")

    st.markdown("---")
    # Quick DB summary in sidebar
    students_cache = fetch_all_students()
    total_count = len(students_cache) if students_cache is not None else 0

    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;">Database Registry</div>
            <div style="font-size: 1.4rem; font-weight: 800; font-family: 'Outfit'; color: #f8fafc; margin-top: 2px;">{total_count} <span style="font-size: 0.85rem; color: #64748b; font-weight: 400;">Students Enrolled</span></div>
            <div style="font-size: 0.72rem; color: #38bdf8; margin-top: 4px;">SQLite • SQLAlchemy ORM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.caption("EduSphere v2.0 • Modern Fullstack Edition")


# ---------------------------------------------------------
# 1. DASHBOARD OVERVIEW PAGE
# ---------------------------------------------------------
if choice == "📊 Dashboard Overview":
    st.markdown(
        """
        <div class="hero-tag">⚡ HIGH-PERFORMANCE REST ARCHITECTURE</div>
        <h1 style="margin: 0; font-size: 2.4rem; background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Student Operations & Insights
        </h1>
        <p style="color: #94a3b8; font-size: 0.98rem; margin-top: 6px; margin-bottom: 24px;">
            Real-time telemetry, enrollment demographics, and centralized management console.
        </p>
        """,
        unsafe_allow_html=True,
    )

    students = fetch_all_students()

    if students is None:
        st.error("🚨 Unable to reach the FastAPI backend server at `http://127.0.0.1:8000`.")
        st.info("Tip: Start the backend server by running `python -m uvicorn backend.main:app --reload` in your terminal.")
    else:
        # Dynamic Metric Calculations
        total_students = len(students)
        avg_age = round(sum(s["age"] for s in students) / total_students, 1) if total_students > 0 else 0
        departments_active = len(set(s["department"] for s in students)) if total_students > 0 else 0

        # KPI Row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-title">Enrolled Students</div>
                    <div class="metric-val">{total_students}</div>
                    <div class="metric-desc"><span style="color: #34d399;">●</span> Live database records</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-title">Active Departments</div>
                    <div class="metric-val">{departments_active}</div>
                    <div class="metric-desc">Out of {len(DEPARTMENTS)} disciplines</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-title">Average Age</div>
                    <div class="metric-val">{avg_age} <span style="font-size: 1rem; color: #94a3b8; font-weight: 500;">yrs</span></div>
                    <div class="metric-desc">Cohort distribution</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi4:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-title">API Response</div>
                    <div class="metric-val">{backend_info.get('latency', 0) or 0} <span style="font-size: 1rem; color: #94a3b8; font-weight: 500;">ms</span></div>
                    <div class="metric-desc"><span style="color: #38bdf8;">⚡</span> Ultra-low latency</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

        # Department Chart & Quick Overview Split
        col_chart, col_recent = st.columns([1.2, 1])

        with col_chart:
            st.markdown("### 📈 Department Distribution")
            if total_students > 0:
                dept_counts = {}
                for s in students:
                    dept_counts[s["department"]] = dept_counts.get(s["department"], 0) + 1
                
                chart_df = pd.DataFrame(
                    list(dept_counts.items()),
                    columns=["Department", "Students"]
                ).set_index("Department").sort_values(by="Students", ascending=False)
                
                st.bar_chart(chart_df, height=310, color="#6366f1")
            else:
                st.info("No enrollment data available to chart yet. Register students to see live analytics!")

        with col_recent:
            st.markdown("### 🌟 Recent Enrollees")
            if total_students > 0:
                # Display the last 3-4 students as sleek profile cards
                recent_students = students[-3:][::-1]
                for s in recent_students:
                    initials = get_initials(s["name"])
                    badge_html = render_dept_badge(s["department"])
                    safe_name = html.escape(s["name"])
                    safe_email = html.escape(s["email"])
                    st.markdown(
                        f"""
                        <div class="student-card" style="margin-bottom: 12px; display: flex; align-items: center; gap: 14px;">
                            <div class="id-avatar" style="width: 48px; height: 48px; font-size: 1.1rem; border-radius: 12px; flex-shrink: 0;">
                                {initials}
                            </div>
                            <div style="flex-grow: 1; min-width: 0;">
                                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                                    <div style="font-weight: 700; color: #f8fafc; font-size: 0.98rem; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                                        {safe_name}
                                    </div>
                                    <span style="font-size: 0.72rem; color: #94a3b8; font-family: monospace;">ID #{s['id']}</span>
                                </div>
                                <div style="font-size: 0.78rem; color: #94a3b8; margin: 2px 0 4px 0;">{safe_email} • {s['age']} yrs</div>
                                <div>{badge_html}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No recent enrollees found.")

        # Quick Feature Highlights
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("### 🛠️ Interactive Feature Modules")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(
                """
                <div class="glass-panel" style="padding: 18px;">
                    <div style="font-size: 1.4rem; margin-bottom: 8px;">✨ Interactive Badge Preview</div>
                    <div style="font-size: 0.85rem; color: #94a3b8;">
                        Watch a digital hologram student ID card render dynamically in real-time as you register each candidate.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                """
                <div class="glass-panel" style="padding: 18px;">
                    <div style="font-size: 1.4rem; margin-bottom: 8px;">🔍 Dynamic Filters & Grid</div>
                    <div style="font-size: 0.85rem; color: #94a3b8;">
                        Instant instant text search, department multi-filtering, CSV export, and rich visual profile cards.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                """
                <div class="glass-panel" style="padding: 18px;">
                    <div style="font-size: 1.4rem; margin-bottom: 8px;">🛡️ Safe CRUD Pipeline</div>
                    <div style="font-size: 0.85rem; color: #94a3b8;">
                        Pre-populated smart updates and double-confirmation security toggles prevent accidental records deletion.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# 2. ADD STUDENT PAGE WITH LIVE BADGE PREVIEW
# ---------------------------------------------------------
elif choice == "✨ Add New Student":
    st.markdown(
        """
        <div class="hero-tag">REGISTRATION PIPELINE</div>
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(135deg, #ffffff 40%, #67e8f9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Register Student & Issue Digital ID
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px;">
            Fill in student credentials to automatically sync with the SQLite database and generate a student credential card.
        </p>
        """,
        unsafe_allow_html=True,
    )

    form_col, preview_col = st.columns([1.1, 1], gap="large")

    with form_col:
        st.markdown("#### 📝 Candidate Information")
        with st.container():
            name = st.text_input(
                "Full Legal Name",
                placeholder="e.g. Alex Morgan",
                help="Enter candidate's given and family name.",
            )
            
            c_age, c_dept = st.columns([1, 1.4])
            with c_age:
                age = st.number_input(
                    "Age",
                    min_value=15,
                    max_value=100,
                    value=20,
                    step=1,
                    help="Student age (between 15 and 100).",
                )
            with c_dept:
                department = st.selectbox("Department", DEPARTMENTS, index=0)
            
            email = st.text_input(
                "Academic / Personal Email",
                placeholder="alex.morgan@university.edu",
                help="Must be a valid email format.",
            )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            submit_btn = st.button("🚀 Register & Save Student", type="primary", use_container_width=True)

            if submit_btn:
                if not name.strip() or not email.strip():
                    st.error("⚠️ Please fill in all required fields (Name and Email).")
                elif "@" not in email or "." not in email:
                    st.warning("⚠️ Please provide a valid email address.")
                else:
                    payload = {
                        "name": name.strip(),
                        "age": int(age),
                        "department": department,
                        "email": email.strip(),
                    }
                    try:
                        with st.spinner("Writing to database..."):
                            response = requests.post(f"{API_URL}/students", json=payload, timeout=5)
                        
                        if response.status_code in (200, 201):
                            created_student = response.json()
                            st.balloons()
                            st.success(
                                f"🎉 Successfully enrolled **{created_student['name']}** (Assigned Student ID: `#{created_student['id']}`)!"
                            )
                        else:
                            st.error(f"❌ Error: {extract_error_message(response)}")
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Could not reach backend server at http://127.0.0.1:8000.")

    with preview_col:
        st.markdown("#### 🪪 Live Digital Credential Card")
        # Live reactive variables
        display_name = name.strip() if name.strip() else "Candidate Name"
        display_email = email.strip() if email.strip() else "candidate@institution.edu"
        display_initials = get_initials(display_name)
        dept_badge_html = render_dept_badge(department)
        now_date = datetime.datetime.now().strftime("%b %Y")

        safe_display_name = html.escape(display_name)
        safe_display_email = html.escape(display_email)

        st.markdown(
            f"""
            <div class="id-card">
                <div class="id-card-header">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">🏛️</span>
                        <div>
                            <div class="id-card-title">EDUSPHERE UNIVERSITY</div>
                            <div style="font-size: 0.65rem; color: #818cf8; letter-spacing: 0.05em;">STUDENT CREDENTIAL PASSPORT</div>
                        </div>
                    </div>
                    <div class="id-chip"></div>
                </div>

                <div style="display: flex; gap: 20px; align-items: center; margin: 18px 0;">
                    <div class="id-avatar">
                        {display_initials}
                    </div>
                    <div style="min-width: 0; flex-grow: 1;">
                        <div style="font-family: 'Outfit'; font-size: 1.35rem; font-weight: 700; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {safe_display_name}
                        </div>
                        <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 2px;">
                            {safe_display_email}
                        </div>
                        <div style="margin-top: 6px;">
                            {dept_badge_html}
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; background: rgba(15, 23, 42, 0.6); padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); margin-top: 16px;">
                    <div>
                        <div style="font-size: 0.65rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">STATUS</div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #34d399;">Active • Matriculated</div>
                    </div>
                    <div>
                        <div style="font-size: 0.65rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">AGE</div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc;">{age} yrs</div>
                    </div>
                    <div>
                        <div style="font-size: 0.65rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">ISSUED</div>
                        <div style="font-size: 0.85rem; font-weight: 700; color: #f8fafc;">{now_date}</div>
                    </div>
                </div>

                <div style="margin-top: 18px; display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 12px;">
                    <span style="font-family: monospace; font-size: 0.72rem; color: #94a3b8;">ID: AUTO-ASSIGNED • FASTAPI REST</span>
                    <span style="font-size: 0.9rem; opacity: 0.7;">📶 RFID VERIFIED</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("ℹ️ The live preview updates dynamically as you complete the registration form.")


# ---------------------------------------------------------
# 3. DIRECTORY & RECORDS
# ---------------------------------------------------------
elif choice == "📋 Directory & Records":
    st.markdown(
        """
        <div class="hero-tag">DATA REPOSITORY</div>
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(135deg, #ffffff 40%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Student Directory & Records
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px;">
            Filter, search, explore, and export student files across all faculties.
        </p>
        """,
        unsafe_allow_html=True,
    )

    students = fetch_all_students()

    if students is None:
        st.error("🚨 Could not connect to the FastAPI backend at http://127.0.0.1:8000.")
    elif not students:
        st.markdown(
            """
            <div class="glass-panel" style="text-align: center; padding: 48px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">📂</div>
                <h3 style="color: #f8fafc; margin-bottom: 8px;">No Student Records Found</h3>
                <p style="color: #94a3b8; max-width: 450px; margin: 0 auto 18px auto;">
                    The database is currently empty. Head over to <b>Add New Student</b> to record your first cohort entry!
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Search & Filter Toolbar
        t1, t2, t3, t4 = st.columns([1.5, 1.2, 0.8, 0.8])
        
        with t1:
            search_query = st.text_input("🔍 Quick Search", placeholder="Search by name, email, or ID...")
        with t2:
            dept_filter = st.selectbox("Filter Department", ["All Departments"] + DEPARTMENTS)
        with t3:
            view_mode = st.radio("Display View", ["Grid Cards", "Data Table"], horizontal=True)
        with t4:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            refresh = st.button("🔄 Refresh Data", use_container_width=True)

        # Apply Filters
        filtered = students
        if dept_filter != "All Departments":
            filtered = [s for s in filtered if s["department"] == dept_filter]
        
        if search_query.strip():
            sq = search_query.strip().lower()
            filtered = [
                s for s in filtered
                if sq in s["name"].lower() or sq in s["email"].lower() or sq == str(s["id"])
            ]

        # Results summary and CSV export
        c_count, c_csv = st.columns([1, 1])
        with c_count:
            st.markdown(
                f"<div style='font-size: 0.85rem; color: #94a3b8; margin: 8px 0;'>Showing <b>{len(filtered)}</b> of <b>{len(students)}</b> registered students</div>",
                unsafe_allow_html=True,
            )
        with c_csv:
            df_export = pd.DataFrame(filtered)
            csv_data = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name="students_export.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if not filtered:
            st.warning("No students matched your search criteria.")
        else:
            if view_mode == "Data Table":
                df = pd.DataFrame(filtered)
                # Reorder columns for optimal readability
                cols_order = ["id", "name", "age", "department", "email"]
                df = df[[c for c in cols_order if c in df.columns]]
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "id": st.column_config.NumberColumn("Student ID", format="#%d"),
                        "name": st.column_config.TextColumn("Full Name"),
                        "age": st.column_config.NumberColumn("Age", format="%d yrs"),
                        "department": st.column_config.TextColumn("Department"),
                        "email": st.column_config.TextColumn("Email Address"),
                    },
                )
            else:
                # Card Grid View: 3 columns layout
                cols = st.columns(3)
                for idx, student in enumerate(filtered):
                    col = cols[idx % 3]
                    initials = get_initials(student["name"])
                    badge_html = render_dept_badge(student["department"])
                    safe_name = html.escape(student["name"])
                    safe_email = html.escape(student["email"])
                    with col:
                        st.markdown(
                            f"""
                            <div class="student-card" style="margin-bottom: 20px;">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                                    <div class="id-avatar" style="width: 52px; height: 52px; font-size: 1.25rem;">
                                        {initials}
                                    </div>
                                    <span style="background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); font-size: 0.75rem; font-weight: 700; padding: 2px 8px; border-radius: 8px; font-family: monospace;">
                                        #{student['id']}
                                    </span>
                                </div>
                                <div style="font-family: 'Outfit'; font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin-bottom: 2px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                                    {safe_name}
                                </div>
                                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                                    ✉️ {safe_email}
                                </div>
                                <div style="font-size: 0.8rem; color: #cbd5e1; margin-bottom: 10px;">
                                    🎂 <b>{student['age']}</b> years old
                                </div>
                                <div style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                                    {badge_html}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


# ---------------------------------------------------------
# 4. SEARCH & LOOKUP PAGE
# ---------------------------------------------------------
elif choice == "🔍 Search & Lookup":
    st.markdown(
        """
        <div class="hero-tag">INSTANT LOOKUP</div>
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(135deg, #ffffff 40%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Student Record Inspection
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px;">
            Retrieve a specific student's record and view their verified credentials directly from SQLite.
        </p>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2 = st.columns([1, 1.2], gap="large")

    with sc1:
        st.markdown("#### 🎯 Query Parameters")
        student_id_input = st.number_input("Enter Student ID Number", min_value=1, value=1, step=1)
        search_pressed = st.button("🔎 Locate Student Record", type="primary", use_container_width=True)

    with sc2:
        st.markdown("#### 📋 Profile Dossier")
        if search_pressed or "last_search_id" in st.session_state:
            query_id = int(student_id_input)
            try:
                with st.spinner("Searching records..."):
                    res = requests.get(f"{API_URL}/students/{query_id}", timeout=4)
                
                if res.status_code == 200:
                    student = res.json()
                    st.success(f"Record successfully retrieved for ID #{student['id']}")
                    initials = get_initials(student["name"])
                    badge_html = render_dept_badge(student["department"])
                    safe_name = html.escape(student["name"])
                    safe_email = html.escape(student["email"])

                    st.markdown(
                        f"""
                        <div class="glass-panel" style="padding: 24px;">
                            <div style="display: flex; gap: 18px; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 16px;">
                                <div class="id-avatar" style="width: 64px; height: 64px; font-size: 1.6rem;">
                                    {initials}
                                </div>
                                <div>
                                    <div style="font-size: 0.75rem; text-transform: uppercase; color: #818cf8; font-weight: 700; letter-spacing: 0.05em;">STUDENT ID #{student['id']}</div>
                                    <div style="font-family: 'Outfit'; font-size: 1.5rem; font-weight: 700; color: #ffffff;">{safe_name}</div>
                                    <div>{badge_html}</div>
                                </div>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px;">
                                <div>
                                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Contact Email</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-top: 2px;">{safe_email}</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Age</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-top: 2px;">{student['age']} years old</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Department</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #f8fafc; margin-top: 2px;">{student['department']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase;">Database Status</div>
                                    <div style="font-size: 0.95rem; font-weight: 600; color: #34d399; margin-top: 2px;">● Synced & Verified</div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.error(f"❌ Student #{query_id} not found: {extract_error_message(res)}")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Could not reach backend server at http://127.0.0.1:8000.")
        else:
            st.info("Enter an ID number and press **Locate Student Record** to view details.")


# ---------------------------------------------------------
# 5. MODIFY RECORD PAGE (SMART AUTO-PREPOPULATION)
# ---------------------------------------------------------
elif choice == "✏️ Modify Record":
    st.markdown(
        """
        <div class="hero-tag">RECORD MAINTENANCE</div>
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(135deg, #ffffff 40%, #fbbf24 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Modify Student Profile
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px;">
            Fetch and adjust existing records with live auto-prepopulation and validation.
        </p>
        """,
        unsafe_allow_html=True,
    )

    fetch_col, edit_col = st.columns([1, 1.5], gap="large")

    with fetch_col:
        st.markdown("#### 1️⃣ Select Student")
        students = fetch_all_students()

        if students:
            # Dropdown with student names and IDs for instant selection
            student_options = {f"#{s['id']} — {s['name']} ({s['department']})": s["id"] for s in students}
            selected_label = st.selectbox("Choose student to edit", list(student_options.keys()))
            target_id = student_options[selected_label]
        else:
            target_id = st.number_input("Target Student ID", min_value=1, value=1, step=1)

        load_btn = st.button("📥 Load Student Profile", use_container_width=True)

        # Cache loaded student in session state for editing
        if load_btn or "edit_student_data" not in st.session_state:
            try:
                res = requests.get(f"{API_URL}/students/{int(target_id)}", timeout=4)
                if res.status_code == 200:
                    st.session_state["edit_student_data"] = res.json()
                    st.toast(f"Loaded student #{target_id} successfully!")
                else:
                    st.session_state["edit_student_data"] = None
                    st.error(f"Could not load ID #{target_id}: {extract_error_message(res)}")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Cannot connect to FastAPI backend.")

    with edit_col:
        st.markdown("#### 2️⃣ Update Fields")
        edit_data = st.session_state.get("edit_student_data")

        if edit_data:
            with st.container():
                edit_name = st.text_input("Full Name", value=edit_data.get("name", ""))
                
                col_age, col_dept = st.columns(2)
                with col_age:
                    edit_age = st.number_input(
                        "Age",
                        min_value=15,
                        max_value=100,
                        value=int(edit_data.get("age", 20)),
                        step=1,
                    )
                with col_dept:
                    current_dept = edit_data.get("department", DEPARTMENTS[0])
                    dept_index = DEPARTMENTS.index(current_dept) if current_dept in DEPARTMENTS else 0
                    edit_department = st.selectbox("Department", DEPARTMENTS, index=dept_index)
                
                edit_email = st.text_input("Email", value=edit_data.get("email", ""))

                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                save_btn = st.button("💾 Save Profile Changes", type="primary", use_container_width=True)

                if save_btn:
                    if not edit_name.strip() or not edit_email.strip():
                        st.error("Name and Email cannot be empty.")
                    else:
                        payload = {
                            "name": edit_name.strip(),
                            "age": int(edit_age),
                            "department": edit_department,
                            "email": edit_email.strip(),
                        }
                        try:
                            with st.spinner("Applying updates..."):
                                put_res = requests.put(
                                    f"{API_URL}/students/{edit_data['id']}",
                                    json=payload,
                                    timeout=5,
                                )
                            if put_res.status_code == 200:
                                updated = put_res.json()
                                st.session_state["edit_student_data"] = updated
                                st.success(f"✅ Student #{updated['id']} was successfully updated!")
                            else:
                                st.error(f"Update failed: {extract_error_message(put_res)}")
                        except requests.exceptions.ConnectionError:
                            st.error("🚨 Backend disconnected.")
        else:
            st.info("Select a student on the left and click **Load Student Profile** to begin editing.")


# ---------------------------------------------------------
# 6. DELETE STUDENT (SAFE CONFIRMATION PIPELINE)
# ---------------------------------------------------------
elif choice == "🗑️ Delete Student":
    st.markdown(
        """
        <div class="hero-tag" style="background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.3); color: #f87171;">
            DESTRUCTIVE ACTION
        </div>
        <h1 style="margin: 0; font-size: 2.2rem; background: linear-gradient(135deg, #ffffff 40%, #f87171 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Remove Student Record
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px;">
            Permanently delete a student file from the database. Protected with dual confirmation safeguard.
        </p>
        """,
        unsafe_allow_html=True,
    )

    del_c1, del_c2 = st.columns([1, 1.2], gap="large")

    students = fetch_all_students()

    with del_c1:
        st.markdown("#### 1️⃣ Select Record for Deletion")
        if students:
            del_options = {f"#{s['id']} — {s['name']} ({s['department']})": s["id"] for s in students}
            selected_del_label = st.selectbox("Select Candidate", list(del_options.keys()))
            del_id = del_options[selected_del_label]
        else:
            del_id = st.number_input("Target Student ID to Remove", min_value=1, value=1, step=1)

        # Inspect target student before deletion
        target_student = next((s for s in (students or []) if s["id"] == del_id), None)

    with del_c2:
        st.markdown("#### 2️⃣ Safety Confirmation")
        if target_student:
            initials = get_initials(target_student["name"])
            safe_name = html.escape(target_student["name"])
            safe_email = html.escape(target_student["email"])
            st.markdown(
                f"""
                <div class="glass-panel" style="border-color: rgba(239, 68, 68, 0.3); background: rgba(30, 41, 59, 0.7); margin-bottom: 16px;">
                    <div style="font-size: 0.75rem; text-transform: uppercase; color: #f87171; font-weight: 700;">Record Marked For Deletion</div>
                    <div style="font-family: 'Outfit'; font-size: 1.3rem; font-weight: 700; color: #ffffff; margin-top: 4px;">
                        {safe_name} <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 400;">(ID #{target_student['id']})</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #cbd5e1; margin-top: 4px;">
                        {safe_email} • {target_student['department']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        confirm_check = st.checkbox(
            "⚠️ I understand that this action is irreversible and permanently deletes the student record from SQLite.",
            value=False,
        )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        delete_btn = st.button("🗑️ Permanently Delete Record", type="primary", disabled=not confirm_check, use_container_width=True)

        if delete_btn:
            try:
                with st.spinner("Deleting record..."):
                    res = requests.delete(f"{API_URL}/students/{int(del_id)}", timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    st.success(data.get("message", f"Student #{del_id} deleted successfully!"))
                    # Trigger rerun to update cached student count
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Delete failed: {extract_error_message(res)}")
            except requests.exceptions.ConnectionError:
                st.error("🚨 Backend disconnected.")
