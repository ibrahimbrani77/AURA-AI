import streamlit as st
import time
import datetime

from modules.reminders import create_reminder, get_reminders, complete_reminder, delete_reminder, get_overdue_reminders
from modules.personalization import save_preference, get_preferences, build_user_context
from modules.auth import (
    register_user, login_user, decode_token,
    get_user_by_email, login_user_biometric
)
from modules.tasks import create_task, get_tasks, complete_task, delete_task
from modules.notes import create_note, get_notes, delete_note
from modules.ai_engine import get_ai_response
from modules.vision import capture_face_embedding, verify_face

# =========================
# CONFIG & THEME ENGINE
# =========================
st.set_page_config(page_title="Nexus AI", page_icon="🧬", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "Cyan"

themes = {
    "Cyan":    {"accent": "#00f2ff", "glow": "rgba(0, 242, 255, 0.15)"},
    "Emerald": {"accent": "#10b981", "glow": "rgba(16, 185, 129, 0.15)"},
    "Violet":  {"accent": "#8b5cf6", "glow": "rgba(139, 92, 246, 0.15)"}
}
active_color = themes[st.session_state.theme]["accent"]
glow_color   = themes[st.session_state.theme]["glow"]

# =========================
# NAVIGATION & REDIRECTS
# =========================
if "nav" not in st.session_state:
    st.session_state.nav = "Login"

def redirect(page):
    st.session_state.nav = page
    st.rerun()

# Decode uid early so sidebar can use it
uid = None
if "token" in st.session_state:
    try:
        payload = decode_token(st.session_state.token)
        uid = payload["user_id"]
    except:
        pass

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, h1, h2, h3, label {{
    font-family: 'Syne', sans-serif !important;
}}
.stApp {{
    background: #050508 !important;
    color: #f0f0f8 !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 4rem !important; }}
.streamlit-expanderHeader p {{
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #f0f0f8 !important;
}}
.streamlit-expanderHeader svg {{ display: none !important; }}
details summary span[data-testid="stExpanderToggleIcon"] {{ display: none !important; }}
details {{
    background: #0c0c12 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    margin-bottom: 10px !important;
}}
details summary {{
    padding: 12px 16px !important;
    color: #f0f0f8 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    list-style: none !important;
}}
details summary::-webkit-details-marker {{ display: none !important; }}
section[data-testid="stSidebar"] {{
    background: #0c0c12 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}}
section[data-testid="stSidebar"] * {{
    font-family: 'Syne', sans-serif !important;
}}
.stSelectbox > div > div {{
    background: #12121a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f0f0f8 !important;
    border-radius: 8px !important;
}}
.stRadio label {{
    color: #9090a8 !important;
    font-size: 13px !important;
}}
.stRadio label:hover {{ color: #f0f0f8 !important; }}
input, textarea, input[type="text"], input[type="password"] {{
    background: #12121a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f0f0f8 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
}}
input:focus, textarea:focus {{
    border-color: {active_color} !important;
    box-shadow: 0 0 0 2px {glow_color} !important;
}}
label[data-testid="stWidgetLabel"] p {{
    color: #9090a8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}}
.stButton > button {{
    width: 100% !important;
    background: {active_color} !important;
    color: #050508 !important;
    border: none !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 0.08em !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    text-transform: uppercase !important;
    transition: opacity 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.85 !important;
    color: #050508 !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    background: #0c0c12 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: #6b6b80 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    font-family: 'Syne', sans-serif !important;
    padding: 6px 16px !important;
}}
.stTabs [aria-selected="true"] {{
    background: {active_color}22 !important;
    color: {active_color} !important;
}}
.stChatInput textarea {{
    background: #0c0c12 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #f0f0f8 !important;
    font-family: 'Syne', sans-serif !important;
}}
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 4px; }}
.nexus-metric {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    margin-bottom: 8px;
}}
.nexus-metric-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; }}
.nexus-metric-label {{
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #6b6b80; margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
}}
.nexus-metric-value {{
    font-size: 30px; font-weight: 800;
    letter-spacing: -0.02em; line-height: 1;
    margin-bottom: 8px; font-family: 'Syne', sans-serif;
}}
.nexus-metric-sub {{ font-size: 11px; color: #6b6b80; font-family: 'JetBrains Mono', monospace; }}
.nexus-panel-header {{
    padding: 12px 0;
    font-size: 13px; font-weight: 600;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 14px; color: #f0f0f8;
}}
.nexus-task {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
}}
.nexus-task-title {{ font-size: 13px; font-weight: 600; color: #f0f0f8; }}
.nexus-task-desc {{
    font-size: 11px; color: #6b6b80;
    font-family: 'JetBrains Mono', monospace; margin-top: 3px;
}}
.nexus-bubble-ai {{
    background: #12121a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; border-top-left-radius: 3px;
    padding: 10px 14px; font-size: 13px; line-height: 1.6;
    color: #f0f0f8; max-width: 85%; margin-bottom: 10px; display: inline-block;
}}
.nexus-bubble-user {{
    background: {glow_color};
    border: 1px solid {active_color}44;
    border-radius: 12px; border-top-right-radius: 3px;
    padding: 10px 14px; font-size: 13px; line-height: 1.6;
    color: #f0f0f8; max-width: 85%; margin-bottom: 10px; display: inline-block;
}}
.nexus-chat-ai {{ display: flex; align-items: flex-start; gap: 10px; margin-bottom: 6px; }}
.nexus-chat-user {{ display: flex; flex-direction: row-reverse; align-items: flex-start; gap: 10px; margin-bottom: 6px; }}
.nexus-av {{
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 800; flex-shrink: 0;
    background: linear-gradient(135deg, {active_color}, #9b59ff);
    color: #050508; font-family: 'Syne', sans-serif;
}}
.nexus-note {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
}}
.nexus-note-title {{ font-size: 12px; font-weight: 700; color: #f0f0f8; margin-bottom: 4px; }}
.nexus-note-body {{ font-size: 11px; color: #9090a8; line-height: 1.6; }}
.nexus-auth-card {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 2.5rem 2rem;
}}
.nexus-status-bar {{
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 28px; background: #0c0c12;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center;
    padding: 0 28px; gap: 24px; z-index: 9999;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; color: #6b6b80;
}}
.nexus-tag {{
    font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace; display: inline-block;
}}
.streamlit-expanderHeader p::before {{ content: none !important; }}
[data-testid="stExpanderToggleIcon"] {{ display: none !important; width: 0 !important; }}
summary > div > p {{ font-size: 13px !important; font-weight: 600 !important; color: #f0f0f8 !important; }}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"""
    <div style='padding:12px 0 20px;'>
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:20px;'>
            <div style='width:32px;height:32px;border-radius:8px;
                background:linear-gradient(135deg,{active_color},#9b59ff);
                display:flex;align-items:center;justify-content:center;
                font-weight:900;font-size:14px;color:#050508;
                font-family:Syne,sans-serif;flex-shrink:0;'>N</div>
            <span style='font-size:13px;font-weight:800;letter-spacing:0.1em;
                color:{active_color};font-family:Syne,sans-serif;'>NEXUS AI</span>
        </div>
        <div style='font-size:9px;color:#6b6b80;letter-spacing:0.14em;
            font-family:JetBrains Mono,monospace;margin-bottom:8px;'>WORKSPACE THEME</div>
    </div>
    """, unsafe_allow_html=True)

    theme_choice = st.selectbox("Theme", list(themes.keys()), label_visibility="collapsed")
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)

    if "token" in st.session_state and uid:
        st.markdown("""
        <div style='font-size:9px;color:#6b6b80;letter-spacing:0.14em;
            font-family:JetBrains Mono,monospace;margin-bottom:8px;'>MY PROFILE</div>
        """, unsafe_allow_html=True)

        if "show_prefs" not in st.session_state:
            st.session_state.show_prefs = False

        if st.button("Edit Profile", key="toggle_prefs"):
            st.session_state.show_prefs = not st.session_state.show_prefs

        if st.session_state.show_prefs:
            prefs = get_preferences(uid)
            p_name  = st.text_input("Your Name",        value=prefs.get("name", ""),        key="p_name")
            p_role  = st.text_input("Your Role",        value=prefs.get("role", ""),        key="p_role")
            p_goals = st.text_input("Your Goals",       value=prefs.get("goals", ""),       key="p_goals")
            p_prefs = st.text_input("Your Preferences", value=prefs.get("preferences", ""), key="p_prefs")
            p_tz    = st.text_input("Your Timezone",    value=prefs.get("timezone", ""),    key="p_tz")
            if st.button("Save Profile", key="save_prefs"):
                if p_name:  save_preference(uid, "name",        p_name)
                if p_role:  save_preference(uid, "role",        p_role)
                if p_goals: save_preference(uid, "goals",       p_goals)
                if p_prefs: save_preference(uid, "preferences", p_prefs)
                if p_tz:    save_preference(uid, "timezone",    p_tz)
                st.success("Profile saved!")
                st.session_state.show_prefs = False
                st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)

        if st.button("Secure Logout"):
            st.session_state.clear()
            redirect("Login")
    else:
        nav_choice = st.radio("Navigation", ["Login", "Register"],
                              index=0 if st.session_state.nav == "Login" else 1,
                              label_visibility="collapsed")
        if nav_choice != st.session_state.nav:
            redirect(nav_choice)

# =========================
# AUTH
# =========================
if st.session_state.nav in ["Login", "Register"]:
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='nexus-auth-card'>", unsafe_allow_html=True)

        if st.session_state.nav == "Register":
            st.markdown(f"<h2 style='color:{active_color};margin-bottom:20px;font-family:Syne,sans-serif;'>Create Nexus ID</h2>", unsafe_allow_html=True)
            reg_name  = st.text_input("Identity Name", placeholder="John Doe")
            reg_email = st.text_input("Neural Email",  placeholder="name@nexus.ai")
            reg_pass  = st.text_input("Security Key",  type="password", placeholder="••••••••")

            import os
            is_cloud = os.getenv("IS_CLOUD", "false").lower() == "true"

            if is_cloud:
                st.markdown(f"""
                <div style='background:#ffb02012;border:1px solid #ffb02044;
                    border-radius:10px;padding:12px;margin-bottom:12px;'>
                    <div style='font-size:11px;color:#ffb020;'>
                        Face ID unavailable on web — account will be created without biometrics.
                        You can add face login when running locally.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Create Account"):
                    if reg_name and reg_email and reg_pass:
                        register_user(reg_name, reg_email, reg_pass, None)
                        st.success("Identity created. Redirecting...")
                        time.sleep(1.5)
                        redirect("Login")
                    else:
                        st.warning("All fields are mandatory.")
            else:
                st.info("Biometric scan required for account finalization.")
                if st.button("Initialize Face Scan & Create"):
                    if reg_name and reg_email and reg_pass:
                        with st.spinner("Analyzing facial geometry..."):
                            face_data = capture_face_embedding()
                            if face_data:
                                register_user(reg_name, reg_email, reg_pass, face_data)
                                st.success("Identity created. Redirecting...")
                                time.sleep(1.5)
                                redirect("Login")
                            else:
                                st.error("Face capture failed. Check lighting.")
                    else:
                        st.warning("All fields are mandatory.")
        else:
            st.markdown(f"<h2 style='color:{active_color};margin-bottom:20px;font-family:Syne,sans-serif;'>System Access</h2>", unsafe_allow_html=True)
            login_tab, face_tab = st.tabs(["Password Login", "Face Login"])

            with login_tab:
                l_email = st.text_input("Email", key="l_email")
                l_pass  = st.text_input("Password", type="password", key="l_pass")
                if st.button("Verify Identity"):
                    token = login_user(l_email, l_pass)
                    if token:
                        st.session_state.token = token
                        redirect("Dashboard")
                    else:
                        st.error("Access Denied: Invalid credentials.")

            with face_tab:
                import os
                if os.getenv("IS_CLOUD", "false").lower() == "true":
                    st.markdown(f"""
                    <div style='background:#ffb02012;border:1px solid #ffb02044;
                        border-radius:10px;padding:16px;text-align:center;'>
                        <div style='font-size:13px;font-weight:700;color:#ffb020;
                            margin-bottom:6px;'>Face ID — Local Only</div>
                        <div style='font-size:11px;color:#9090a8;'>
                            Biometric login requires running the app locally.<br>
                            Use password login on the web version.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    f_email = st.text_input("Email", key="f_email")
                    if st.button("Scan Face"):
                        user = get_user_by_email(f_email)
                        if user:
                            with st.spinner("Matching biometric signature..."):
                                if verify_face(user.face_embedding):
                                    st.session_state.token = login_user_biometric(f_email)
                                    redirect("Dashboard")
                                else:
                                    st.error("Biometric mismatch.")
                        else:
                            st.error("Identity not found.")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
elif st.session_state.nav == "Dashboard":
    if "token" not in st.session_state:
        redirect("Login")

    tasks     = get_tasks(uid)
    notes     = get_notes(uid)
    reminders = get_reminders(uid)
    overdue   = get_overdue_reminders(uid)

    # HEADER
    st.markdown(f"""
    <div style='margin-bottom:24px;'>
        <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
            letter-spacing:0.12em;margin-bottom:8px;'>MASTER CONTROL · NEXUS AI</div>
        <h1 style='font-size:26px;font-weight:800;letter-spacing:-0.02em;
            line-height:1;margin:0;color:#f0f0f8;font-family:Syne,sans-serif;'>
            Good evening, <span style='color:{active_color};'>Commander.</span>
        </h1>
        <p style='color:#9090a8;font-size:13px;margin-top:8px;margin-bottom:0;'>
            {len(tasks)} tasks pending &nbsp;·&nbsp; AI ready &nbsp;·&nbsp; System active
        </p>
    </div>
    """, unsafe_allow_html=True)

    # METRICS
    m1, m2, m3, m4 = st.columns(4)
    metric_data = [
        (m1, "ACTIVE TASKS", str(len(tasks)),     "tasks deployed",    active_color),
        (m2, "NOTES SAVED",  str(len(notes)),     "in memory bank",    "#9b59ff"),
        (m3, "AI STATUS",    "ONLINE",            "neural engine ready","#00d68f"),
        (m4, "REMINDERS",    str(len(reminders)), "upcoming alerts",   "#ffb020"),
    ]
    for col, label, value, sub, color in metric_data:
        with col:
            st.markdown(f"""
            <div class='nexus-metric'>
                <div class='nexus-metric-bar'
                    style='background:linear-gradient(90deg,{color},transparent);'></div>
                <div class='nexus-metric-label'>{label}</div>
                <div class='nexus-metric-value' style='color:{color};'>{value}</div>
                <div class='nexus-metric-sub'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # WORKSPACE
    col_left, col_right = st.columns([1.3, 1])

    with col_left:

        # ── TASKS ──
        st.markdown(f"""
        <div class='nexus-panel-header'>
            <div style='width:6px;height:6px;border-radius:50%;
                background:{active_color};flex-shrink:0;'></div>
            Task Engine
            <span style='margin-left:auto;font-size:10px;color:#6b6b80;
                font-family:JetBrains Mono,monospace;'>{len(tasks)} PENDING</span>
        </div>
        """, unsafe_allow_html=True)

        if "show_add_task" not in st.session_state:
            st.session_state.show_add_task = False
        if st.button("Deploy New Task", key="toggle_task"):
            st.session_state.show_add_task = not st.session_state.show_add_task
        if st.session_state.show_add_task:
            st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;'>", unsafe_allow_html=True)
            t_title = st.text_input("Task Identifier", placeholder="e.g. Fix vision.py threshold")
            t_desc  = st.text_area("Objective Details", placeholder="Describe the task...")
            if st.button("Confirm Deployment"):
                if t_title:
                    create_task(t_title, t_desc, uid)
                    st.session_state.show_add_task = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        for t in tasks:
            tag_color = "#ff4560" if t.status != "completed" else "#00d68f"
            tag_label = "PENDING" if t.status != "completed" else "DONE"
            st.markdown(f"""
            <div class='nexus-task'>
                <div style='display:flex;align-items:center;justify-content:space-between;'>
                    <div>
                        <div class='nexus-task-title'>{t.title}</div>
                        <div class='nexus-task-desc'>{t.description or "No description"}</div>
                    </div>
                    <span class='nexus-tag'
                        style='background:{tag_color}22;color:{tag_color};'>{tag_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, _ = st.columns([0.15, 0.15, 0.7])
            if t.status != "completed":
                if c1.button("✔", key=f"done_{t.id}"):
                    complete_task(t.id)
                    st.rerun()
            if c2.button("✕", key=f"del_{t.id}"):
                delete_task(t.id)
                st.rerun()

        # ── NOTES ──
        st.markdown("""
        <div style='margin-top:24px;margin-bottom:10px;font-size:10px;font-weight:600;
            letter-spacing:0.14em;color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;'>Quick Notes</div>
        """, unsafe_allow_html=True)

        if notes:
            for n in notes:
                st.markdown(f"""
                <div class='nexus-note'>
                    <div class='nexus-note-title'>{n.title}</div>
                    <div class='nexus-note-body'>{n.content or ""}</div>
                </div>
                """, unsafe_allow_html=True)
                nd1, nd2, _ = st.columns([0.15, 0.15, 0.7])
                if nd2.button("✕", key=f"del_note_{n.id}"):
                    delete_note(n.id)
                    st.rerun()
        else:
            st.markdown("<div style='color:#6b6b80;font-size:12px;margin-bottom:10px;'>No notes yet.</div>", unsafe_allow_html=True)

        if "show_add_note" not in st.session_state:
            st.session_state.show_add_note = False
        if st.button("New Note", key="toggle_note"):
            st.session_state.show_add_note = not st.session_state.show_add_note
        if st.session_state.show_add_note:
            st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;'>", unsafe_allow_html=True)
            n_title = st.text_input("Note Title", placeholder="e.g. Debug findings")
            n_body  = st.text_area("Content", placeholder="Write anything...")
            if st.button("Save Note"):
                if n_title:
                    create_note(n_title, n_body, uid)
                    st.session_state.show_add_note = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ── REMINDERS ──
        st.markdown("""
        <div style='margin-top:24px;margin-bottom:10px;font-size:10px;font-weight:600;
            letter-spacing:0.14em;color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;'>Reminders</div>
        """, unsafe_allow_html=True)

        if overdue:
            for r in overdue:
                st.markdown(f"""
                <div style='background:#ff456012;border:1px solid #ff456044;
                    border-radius:10px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:12px;font-weight:700;color:#ff4560;'>
                        OVERDUE — {r.title}</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date"}</div>
                </div>
                """, unsafe_allow_html=True)

        if reminders:
            for r in reminders:
                st.markdown(f"""
                <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:13px;font-weight:600;color:#f0f0f8;'>{r.title}</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date set"}</div>
                </div>
                """, unsafe_allow_html=True)
                r1, r2, _ = st.columns([0.15, 0.15, 0.7])
                if r1.button("✔", key=f"rem_done_{r.id}"):
                    complete_reminder(r.id)
                    st.rerun()
                if r2.button("✕", key=f"rem_del_{r.id}"):
                    delete_reminder(r.id)
                    st.rerun()
        else:
            st.markdown("<div style='color:#6b6b80;font-size:12px;margin-bottom:10px;'>No reminders set.</div>", unsafe_allow_html=True)

        if "show_add_reminder" not in st.session_state:
            st.session_state.show_add_reminder = False
        if st.button("New Reminder", key="toggle_reminder"):
            st.session_state.show_add_reminder = not st.session_state.show_add_reminder
        if st.session_state.show_add_reminder:
            st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;'>", unsafe_allow_html=True)
            rem_title = st.text_input("Reminder", placeholder="e.g. Take medication")
            rem_date  = st.date_input("Due Date")
            rem_time  = st.time_input("Due Time")
            if st.button("Save Reminder"):
                if rem_title:
                    due_dt = datetime.datetime.combine(rem_date, rem_time)
                    create_reminder(rem_title, due_dt, uid)
                    st.session_state.show_add_reminder = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── CHAT ──
    with col_right:
        st.markdown(f"""
        <div class='nexus-panel-header'>
            <div style='width:6px;height:6px;border-radius:50%;
                background:#9b59ff;flex-shrink:0;'></div>
            Neural Chat
            <span style='margin-left:auto;font-size:10px;color:{active_color};
                font-family:JetBrains Mono,monospace;'>AI ONLINE</span>
        </div>
        """, unsafe_allow_html=True)

        if "chat" not in st.session_state:
            st.session_state.chat = [{
                "role": "assistant",
                "content": "System initialized. Identity confirmed. How can I assist you, Commander?"
            }]

        chat_container = st.container(height=420)
        with chat_container:
            for msg in st.session_state.chat:
                if msg["role"] == "assistant":
                    st.markdown(f"""
                    <div class='nexus-chat-ai'>
                        <div class='nexus-av'>N</div>
                        <div class='nexus-bubble-ai'>{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='nexus-chat-user'>
                        <div class='nexus-av'
                            style='background:linear-gradient(135deg,#9b59ff,{active_color});'>U</div>
                        <div class='nexus-bubble-user'>{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        prompt = st.chat_input("Command the AI...", key="main_chat")
        if prompt:
            st.session_state.chat.append({"role": "user", "content": prompt})
            user_context = build_user_context(uid)
            response = get_ai_response(
                prompt,
                chat_history=st.session_state.chat[:-1],
                user_context=user_context,
                tasks=tasks,
                notes=notes,
                reminders=reminders
            )
            st.session_state.chat.append({"role": "assistant", "content": response})
            st.rerun()

    # STATUS BAR
    st.markdown(f"""
    <div class='nexus-status-bar'>
        <span><span style='color:{active_color};'>●</span>&nbsp; AI ENGINE ONLINE</span>
        <span><span style='color:#00d68f;'>●</span>&nbsp; PBKDF2 AUTH</span>
        <span><span style='color:#9b59ff;'>●</span>&nbsp; SFACE VERIFIED</span>
        <span style='margin-left:auto;'>NEXUS AI v2.0 &nbsp;·&nbsp; localhost:8501</span>
    </div>
    """, unsafe_allow_html=True)