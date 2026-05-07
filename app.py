import streamlit as st
import time
from modules.voice import text_to_speech
from datetime import datetime
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

from modules.database import engine, Base
import modules.models
from sqlalchemy import text

try:
    Base.metadata.create_all(bind=engine, checkfirst=True)
except Exception:
    pass

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE tasks ADD COLUMN priority VARCHAR DEFAULT 'Medium'"))
        conn.commit()
    except Exception:
        pass
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN preferences TEXT DEFAULT ''"))
        conn.commit()
    except Exception:
        pass

st.set_page_config(page_title="Aura — Your Personal AI", page_icon="✦", layout="wide")

themes = {
    "Violet": {"accent": "#a78bfa", "glow": "rgba(167, 139, 250, 0.15)"},
    "Rose":   {"accent": "#f472b6", "glow": "rgba(244, 114, 182, 0.15)"},
    "Cyan":   {"accent": "#22d3ee", "glow": "rgba(34, 211, 238, 0.15)"},
}
if "theme" not in st.session_state:
    st.session_state.theme = "Violet"
active_color = themes[st.session_state.theme]["accent"]
glow_color   = themes[st.session_state.theme]["glow"]

if "nav" not in st.session_state:
    st.session_state.nav = "Home"

def redirect(page):
    st.session_state.nav = page
    st.rerun()

uid = None
if "token" in st.session_state:
    try:
        payload = decode_token(st.session_state.token)
        uid = payload["user_id"]
    except:
        pass

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');
html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, h1, h2, h3, label {{
    font-family: 'Syne', sans-serif !important;
}}
.stApp {{ background: #050508 !important; color: #f0f0f8 !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 4rem !important; }}
section[data-testid="stSidebar"] {{
    background: #0c0c12 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}}
section[data-testid="stSidebar"] * {{ font-family: 'Syne', sans-serif !important; }}
.stSelectbox > div > div {{
    background: #12121a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #f0f0f8 !important;
    border-radius: 8px !important;
}}
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
    color: #9090a8 !important; font-size: 12px !important;
    font-weight: 600 !important; letter-spacing: 0.04em !important;
}}
.stButton > button {{
    background: {active_color} !important;
    color: #050508 !important;
    border: none !important;
    padding: 8px 16px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    text-transform: uppercase !important;
    transition: opacity 0.2s !important;
    width: auto !important;
    min-width: unset !important;
}}
.stButton > button:hover {{ opacity: 0.85 !important; color: #050508 !important; }}
.btn-sm .stButton > button {{
    background: transparent !important;
    color: #9090a8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    padding: 3px 8px !important;
    font-size: 10px !important;
    border-radius: 5px !important;
}}
.btn-sm .stButton > button:hover {{
    background: rgba(255,255,255,0.06) !important;
    color: #f0f0f8 !important;
    opacity: 1 !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    background: #0c0c12 !important; border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important; color: #6b6b80 !important;
    border-radius: 8px !important; font-size: 12px !important;
    font-weight: 600 !important; font-family: 'Syne', sans-serif !important;
    padding: 6px 16px !important;
}}
.stTabs [aria-selected="true"] {{ background: {active_color}22 !important; color: {active_color} !important; }}
.stChatInput textarea {{
    background: #0c0c12 !important; border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important; color: #f0f0f8 !important; font-family: 'Syne', sans-serif !important;
}}
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.1); border-radius: 4px; }}
.aura-metric {{
    background: #0c0c12; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 20px; position: relative; overflow: hidden; margin-bottom: 8px;
}}
.aura-metric-bar {{ position: absolute; top: 0; left: 0; right: 0; height: 2px; }}
.aura-metric-label {{
    font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase;
    color: #6b6b80; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace;
}}
.aura-metric-value {{
    font-size: 30px; font-weight: 800; letter-spacing: -0.02em; line-height: 1;
    margin-bottom: 8px; font-family: 'Syne', sans-serif;
}}
.aura-metric-sub {{ font-size: 11px; color: #6b6b80; font-family: 'JetBrains Mono', monospace; }}
.aura-panel-header {{
    padding: 12px 0; font-size: 13px; font-weight: 600;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 14px; color: #f0f0f8;
}}
.aura-task {{
    background: #0c0c12; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
}}
.aura-task-title {{ font-size: 13px; font-weight: 600; color: #f0f0f8; }}
.aura-task-desc {{ font-size: 11px; color: #6b6b80; font-family: 'JetBrains Mono', monospace; margin-top: 3px; }}
.aura-bubble-ai {{
    background: #12121a; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; border-top-left-radius: 3px;
    padding: 10px 14px; font-size: 13px; line-height: 1.6;
    color: #f0f0f8; max-width: 85%; margin-bottom: 10px; display: inline-block;
}}
.aura-bubble-user {{
    background: {glow_color}; border: 1px solid {active_color}44;
    border-radius: 12px; border-top-right-radius: 3px;
    padding: 10px 14px; font-size: 13px; line-height: 1.6;
    color: #f0f0f8; max-width: 85%; margin-bottom: 10px; display: inline-block;
}}
.aura-chat-ai {{ display: flex; align-items: flex-start; gap: 10px; margin-bottom: 6px; }}
.aura-chat-user {{ display: flex; flex-direction: row-reverse; align-items: flex-start; gap: 10px; margin-bottom: 6px; }}
.aura-av {{
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 800; flex-shrink: 0;
    background: linear-gradient(135deg, {active_color}, #9b59ff);
    color: #050508; font-family: 'Syne', sans-serif;
}}
.aura-note {{
    background: #0c0c12; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;
}}
.aura-note-title {{ font-size: 12px; font-weight: 700; color: #f0f0f8; margin-bottom: 4px; }}
.aura-note-body {{ font-size: 11px; color: #9090a8; line-height: 1.6; }}
.aura-auth-card {{
    background: #0c0c12; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 2.5rem 2rem;
}}
.aura-status-bar {{
    position: fixed; bottom: 0; left: 0; right: 0;
    height: 28px; background: #0c0c12;
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center;
    padding: 0 28px; gap: 24px; z-index: 9999;
    font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #6b6b80;
}}
.aura-tag {{
    font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 20px;
    font-family: 'JetBrains Mono', monospace; display: inline-block;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR — only on dashboard
# =========================
if st.session_state.nav == "Dashboard" and uid:
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:12px 0 20px;'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:20px;'>
                <div style='width:32px;height:32px;border-radius:8px;
                    background:linear-gradient(135deg,{active_color},#9b59ff);
                    display:flex;align-items:center;justify-content:center;
                    font-weight:900;font-size:14px;color:#050508;flex-shrink:0;'>A</div>
                <span style='font-size:13px;font-weight:800;letter-spacing:0.1em;
                    color:{active_color};'>AURA</span>
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
            p_goals = st.text_input("Your Goals",       value=prefs.get("goals", ""),       key="p_goals")
            p_prefs = st.text_input("Your Preferences", value=prefs.get("preferences", ""), key="p_prefs")
            p_tz    = st.text_input("Your Timezone",    value=prefs.get("timezone", ""),    key="p_tz")
            if st.button("Save Profile", key="save_prefs"):
                if p_name:  save_preference(uid, "name",        p_name)
                if p_goals: save_preference(uid, "goals",       p_goals)
                if p_prefs: save_preference(uid, "preferences", p_prefs)
                if p_tz:    save_preference(uid, "timezone",    p_tz)
                st.success("Profile saved!")
                st.session_state.show_prefs = False
                st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:12px 0;'>", unsafe_allow_html=True)

        st.markdown("""
        <div style='font-size:9px;color:#6b6b80;letter-spacing:0.14em;
            font-family:JetBrains Mono,monospace;margin-bottom:8px;'>AURA PERSONALITY</div>
        """, unsafe_allow_html=True)

        try:
            _prefs_sidebar = get_preferences(uid) if uid else {}
        except Exception:
            _prefs_sidebar = {}

        personality_options = ["🎩 Professional", "😊 Friendly", "🧙 Mentor", "😏 Sarcastic", "⚡ Minimalist", "🔥 Hype Coach", "✨ Custom"]
        personality_defaults = {
            "🎩 Professional": "Formal, precise, and concise. No casual language.",
            "😊 Friendly":     "Warm, encouraging, and conversational.",
            "🧙 Mentor":       "Wise, patient, and guiding with thoughtful advice.",
            "😏 Sarcastic":    "Witty and sarcastic with dry humor, but still helpful.",
            "⚡ Minimalist":   "Ultra-concise. Short answers, bullet points, no fluff.",
            "🔥 Hype Coach":   "Energetic, motivating, and enthusiastic about everything!",
            "✨ Custom":       ""
        }

        def on_personality_change():
            new = st.session_state.personality_select
            st.session_state.custom_personality_input = personality_defaults.get(new, "")

        saved_personality = _prefs_sidebar.get("personality", "🎩 Professional")

        # Initialise text area state only once (don't overwrite if user is mid-edit)
        if "custom_personality_input" not in st.session_state:
            st.session_state.custom_personality_input = _prefs_sidebar.get(
                "custom_personality",
                personality_defaults.get(saved_personality, "")
            )

        selected_personality = st.selectbox(
            "Personality", personality_options,
            index=personality_options.index(saved_personality) if saved_personality in personality_options else 0,
            key="personality_select",
            on_change=on_personality_change,
            label_visibility="collapsed"
        )

        custom_desc = st.text_area(
            "Personality Description",
            placeholder="Describe how Aura should behave...",
            height=80,
            key="custom_personality_input",
            label_visibility="collapsed"
        )
        if st.button("Save Personality", key="save_personality"):
            save_preference(uid, "personality", selected_personality)
            save_preference(uid, "custom_personality", custom_desc)
            st.success("Personality saved!")
            st.rerun()

        st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)
        if st.button("Secure Logout"):
            st.session_state.clear()
            redirect("Home")

# =========================
# HOME PAGE
# =========================
if st.session_state.nav == "Home":

    # ── NAVBAR ──
    st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:space-between;
        padding:18px 48px;border-bottom:1px solid rgba(255,255,255,0.06);
        position:sticky;top:0;background:rgba(5,5,8,0.95);
        backdrop-filter:blur(12px);z-index:100;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:32px;height:32px;border-radius:8px;
                background:linear-gradient(135deg,{active_color},#7c3aed);
                display:flex;align-items:center;justify-content:center;
                font-weight:900;font-size:14px;color:#050508;'>A</div>
            <span style='font-size:15px;font-weight:800;letter-spacing:0.1em;color:{active_color};'>AURA</span>
        </div>
        <div style='display:flex;gap:32px;'>
            <span style='font-size:13px;color:#9090a8;font-weight:500;cursor:pointer;'>Features</span>
            <span style='font-size:13px;color:#9090a8;font-weight:500;cursor:pointer;'>How It Works</span>
            <span style='font-size:13px;color:#9090a8;font-weight:500;cursor:pointer;'>Personalities</span>
            <span style='font-size:13px;color:#9090a8;font-weight:500;cursor:pointer;'>About</span>
        </div>
        <div style='display:flex;gap:12px;align-items:center;'>
            <span id='nav-login-placeholder'></span>
            <span id='nav-signup-placeholder'></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_col1, nav_col2, nav_col3 = st.columns([6, 1, 1])
    with nav_col2:
        if st.button("Log in", key="nav_login"):
            redirect("Login")
    with nav_col3:
        if st.button("Get Started", key="nav_register"):
            redirect("Register")

    # ── HERO ──
    hero_left, hero_right = st.columns([1, 1], gap="large")

    with hero_left:
        st.markdown(f"""
        <div style='padding:60px 0 40px 48px;'>
            <div style='display:inline-flex;align-items:center;gap:8px;
                background:{glow_color};border:1px solid {active_color}44;
                border-radius:20px;padding:6px 14px;margin-bottom:24px;'>
                <div style='width:6px;height:6px;border-radius:50%;background:{active_color};'></div>
                <span style='font-size:11px;font-weight:600;color:{active_color};
                    letter-spacing:0.12em;font-family:JetBrains Mono,monospace;'>
                    AI-POWERED · PERSONAL · ADAPTIVE
                </span>
            </div>
            <h1 style='font-size:clamp(40px,5vw,64px);font-weight:800;letter-spacing:-0.03em;
                line-height:1.05;margin:0 0 20px;color:#f0f0f8;'>
                Hi, I'm <span style='color:{active_color};'>Aura.</span><br>
                Your AI, built<br>around <span style='color:{active_color};'>you.</span>
            </h1>
            <p style='font-size:16px;color:#9090a8;line-height:1.7;margin:0 0 40px;max-width:460px;'>
                I manage your tasks, take notes, set reminders, and chat with you —
                all while adapting my personality to match how <em>you</em> like to work.
            </p>
            <div style='display:flex;gap:32px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);'>
                <div>
                    <div style='font-size:28px;font-weight:800;color:#f0f0f8;'>6</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;'>AI PERSONALITIES</div>
                </div>
                <div style='width:1px;background:rgba(255,255,255,0.08);'></div>
                <div>
                    <div style='font-size:28px;font-weight:800;color:#f0f0f8;'>∞</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;'>TASKS & NOTES</div>
                </div>
                <div style='width:1px;background:rgba(255,255,255,0.08);'></div>
                <div>
                    <div style='font-size:28px;font-weight:800;color:#f0f0f8;'>1</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;letter-spacing:0.1em;'>CLICK EXPORT</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn1, btn2, btn3 = st.columns([1, 1, 2])
        with btn1:
            if st.button("✦ Get Started Free", key="hero_cta"):
                redirect("Register")
        with btn2:
            if st.button("Sign In →", key="hero_login"):
                redirect("Login")

    with hero_right:
        st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:center;
            padding:40px 48px 40px 0;position:relative;height:420px;'>
            <div style='position:absolute;width:340px;height:340px;border-radius:50%;
                border:1px solid {active_color}22;top:50%;left:50%;
                transform:translate(-50%,-50%);'></div>
            <div style='position:absolute;width:420px;height:420px;border-radius:50%;
                border:1px solid {active_color}11;top:50%;left:50%;
                transform:translate(-50%,-50%);'></div>
            <div style='width:220px;height:220px;border-radius:50%;
                background:radial-gradient(circle at 35% 35%, #c4b5fd, #7c3aed 50%, #4c1d95);
                display:flex;align-items:center;justify-content:center;
                box-shadow:0 0 60px {active_color}33;position:relative;z-index:2;'>
                <span style='font-size:72px;color:rgba(255,255,255,0.9);'>✦</span>
            </div>
            <div style='position:absolute;top:60px;right:40px;
                background:#0c0c12;border:1px solid rgba(255,255,255,0.08);
                border-radius:14px;padding:14px 18px;z-index:3;'>
                <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                    letter-spacing:0.1em;margin-bottom:4px;'>TASKS PENDING</div>
                <div style='font-size:22px;font-weight:800;color:{active_color};'>8</div>
            </div>
            <div style='position:absolute;bottom:80px;left:30px;
                background:#0c0c12;border:1px solid rgba(255,255,255,0.08);
                border-radius:14px;padding:14px 18px;z-index:3;'>
                <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                    letter-spacing:0.1em;margin-bottom:4px;'>AI STATUS</div>
                <div style='font-size:16px;font-weight:800;color:#00d68f;'>ONLINE</div>
            </div>
            <div style='position:absolute;top:140px;left:20px;
                background:#0c0c12;border:1px solid rgba(255,255,255,0.08);
                border-radius:14px;padding:14px 18px;z-index:3;'>
                <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                    letter-spacing:0.1em;margin-bottom:4px;'>OVERDUE</div>
                <div style='font-size:22px;font-weight:800;color:#ffb020;'>2</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── FEATURES STRIP ──
    st.markdown(f"""
    <div style='display:flex;justify-content:center;gap:48px;padding:24px 48px;
        border-top:1px solid rgba(255,255,255,0.06);
        border-bottom:1px solid rgba(255,255,255,0.06);
        background:rgba(12,12,18,0.5);flex-wrap:wrap;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>📌</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>Task Engine</span>
        </div>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>🧠</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>Neural Chat</span>
        </div>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>🎭</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>6 Personalities</span>
        </div>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>⏰</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>Smart Reminders</span>
        </div>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>🔊</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>Voice Output</span>
        </div>
        <div style='display:flex;align-items:center;gap:10px;'>
            <span style='font-size:18px;'>🔒</span>
            <span style='font-size:13px;font-weight:600;color:#9090a8;'>Secure & Private</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FEATURE CARDS ──
    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:40px;padding:0 48px;'>
        <div style='font-size:10px;font-weight:600;letter-spacing:0.2em;color:#6b6b80;
            font-family:JetBrains Mono,monospace;margin-bottom:12px;'>WHAT I CAN DO FOR YOU</div>
        <h2 style='font-size:36px;font-weight:800;letter-spacing:-0.02em;color:#f0f0f8;margin:0;'>
            Everything in one place.
        </h2>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    for col, icon, title, color, desc in [
        (f1, "📌", "Task Engine", active_color, "Deploy tasks with High, Medium, or Low priority. I'll help you figure out what to tackle first."),
        (f2, "🧠", "Neural Chat", "#9b59ff", "Talk to me about anything. I know your tasks, notes, and goals — so my answers are actually useful."),
        (f3, "🎭", "6 Personalities", "#f472b6", "Pick Professional, Friendly, Mentor, Sarcastic, Minimalist, or Hype Coach. Or write your own."),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                border-radius:20px;padding:32px;position:relative;overflow:hidden;margin-bottom:20px;'>
                <div style='position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,{color},transparent);'></div>
                <div style='font-size:36px;margin-bottom:16px;'>{icon}</div>
                <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>{title}</h3>
                <p style='font-size:13px;color:#9090a8;line-height:1.7;margin:0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3)
    for col, icon, title, color, desc in [
        (f4, "⏰", "Smart Reminders", "#ffb020", "Set reminders with dates and times. I'll flag what's overdue the moment you open the app."),
        (f5, "📝", "Quick Notes", "#00d68f", "Capture ideas instantly. Your notes are always searchable and available to me."),
        (f6, "🔒", "Secure & Private", "#22d3ee", "PBKDF2 password hashing and JWT tokens. Your data stays yours."),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                border-radius:20px;padding:32px;position:relative;overflow:hidden;margin-bottom:20px;'>
                <div style='position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,{color},transparent);'></div>
                <div style='font-size:36px;margin-bottom:16px;'>{icon}</div>
                <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>{title}</h3>
                <p style='font-size:13px;color:#9090a8;line-height:1.7;margin:0;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    f7c, f8c, f9c = st.columns(3)
    with f7c:
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;margin-bottom:20px;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#a78bfa,transparent);'></div>
            <div style='font-size:36px;margin-bottom:16px;'>🔊</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Voice Output</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.7;margin:0;'>
                Toggle voice mode and Aura reads her responses back to you using natural text-to-speech.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with f8c:
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;margin-bottom:20px;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#ffb020,transparent);'></div>
            <div style='position:absolute;top:16px;right:16px;font-size:9px;font-weight:700;
                letter-spacing:0.1em;background:#ffb02022;border:1px solid #ffb02066;
                color:#ffb020;border-radius:6px;padding:3px 8px;
                font-family:JetBrains Mono,monospace;'>COMING SOON</div>
            <div style='font-size:36px;margin-bottom:16px;'>🎤</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Voice Input</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.7;margin:0;'>
                Speak to Aura instead of typing. Full Whisper speech-to-text pipeline built and ready.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with f9c:
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;margin-bottom:20px;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#00d68f,transparent);'></div>
            <div style='font-size:36px;margin-bottom:16px;'>📊</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Smart Export</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.7;margin:0;'>
                Export all your tasks, notes, and reminders as a clean .txt file with one click.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── DASHBOARD MOCKUP ──
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:32px;'>
        <div style='font-size:10px;font-weight:600;letter-spacing:0.2em;color:#6b6b80;
            font-family:JetBrains Mono,monospace;margin-bottom:12px;'>SEE IT IN ACTION</div>
        <h2 style='font-size:36px;font-weight:800;letter-spacing:-0.02em;color:#f0f0f8;margin:0;'>
            Your workspace, your way.
        </h2>
    </div>
    <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;overflow:hidden;margin-bottom:60px;'>
        <div style='background:#080810;border-bottom:1px solid rgba(255,255,255,0.06);
            padding:14px 24px;display:flex;align-items:center;gap:8px;'>
            <div style='width:10px;height:10px;border-radius:50%;background:#ff4560;'></div>
            <div style='width:10px;height:10px;border-radius:50%;background:#ffb020;'></div>
            <div style='width:10px;height:10px;border-radius:50%;background:#00d68f;'></div>
            <span style='font-size:11px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                margin-left:12px;'>AURA · PERSONAL AI · aura-ai-1.streamlit.app</span>
        </div>
        <div style='display:grid;grid-template-columns:180px 1fr 260px;min-height:300px;'>
            <div style='border-right:1px solid rgba(255,255,255,0.06);padding:20px;'>
                <div style='display:flex;align-items:center;gap:8px;margin-bottom:20px;'>
                    <div style='width:24px;height:24px;border-radius:6px;
                        background:linear-gradient(135deg,{active_color},#7c3aed);
                        display:flex;align-items:center;justify-content:center;
                        font-size:11px;font-weight:900;color:#050508;'>A</div>
                    <span style='font-size:11px;font-weight:800;color:{active_color};
                        letter-spacing:0.08em;'>AURA</span>
                </div>
                <div style='display:flex;align-items:center;gap:8px;padding:8px 10px;
                    border-radius:8px;background:{glow_color};margin-bottom:4px;'>
                    <span style='font-size:13px;'>⚡</span>
                    <span style='font-size:11px;color:{active_color};font-weight:600;'>Dashboard</span>
                </div>
                <div style='display:flex;align-items:center;gap:8px;padding:8px 10px;
                    border-radius:8px;margin-bottom:4px;'>
                    <span style='font-size:13px;'>📌</span>
                    <span style='font-size:11px;color:#6b6b80;'>Tasks</span>
                </div>
                <div style='display:flex;align-items:center;gap:8px;padding:8px 10px;
                    border-radius:8px;margin-bottom:4px;'>
                    <span style='font-size:13px;'>📝</span>
                    <span style='font-size:11px;color:#6b6b80;'>Notes</span>
                </div>
                <div style='display:flex;align-items:center;gap:8px;padding:8px 10px;
                    border-radius:8px;margin-bottom:4px;'>
                    <span style='font-size:13px;'>⏰</span>
                    <span style='font-size:11px;color:#6b6b80;'>Reminders</span>
                </div>
                <div style='display:flex;align-items:center;gap:8px;padding:8px 10px;
                    border-radius:8px;'>
                    <span style='font-size:13px;'>🧠</span>
                    <span style='font-size:11px;color:#6b6b80;'>AI Chat</span>
                </div>
                <div style='margin-top:16px;padding-top:16px;
                    border-top:1px solid rgba(255,255,255,0.06);'>
                    <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                        letter-spacing:0.12em;margin-bottom:8px;'>PERSONALITY</div>
                    <div style='font-size:11px;color:{active_color};
                        background:{glow_color};padding:6px 10px;border-radius:6px;'>
                        🎩 Professional
                    </div>
                </div>
            </div>
            <div style='padding:20px;'>
                <div style='font-size:18px;font-weight:700;color:#f0f0f8;margin-bottom:4px;'>
                    Good morning, <span style='color:{active_color};'>Ibrahim.</span>
                </div>
                <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                    margin-bottom:16px;'>AURA · PERSONAL AI · TUESDAY, MAY 06 · 09:15</div>
                <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px;'>
                    <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;padding:12px;'>
                        <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                            margin-bottom:6px;'>ACTIVE TASKS</div>
                        <div style='font-size:22px;font-weight:800;color:{active_color};'>8</div>
                    </div>
                    <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;padding:12px;'>
                        <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                            margin-bottom:6px;'>NOTES SAVED</div>
                        <div style='font-size:22px;font-weight:800;color:#9b59ff;'>12</div>
                    </div>
                    <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;padding:12px;'>
                        <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                            margin-bottom:6px;'>AI STATUS</div>
                        <div style='font-size:14px;font-weight:800;color:#00d68f;margin-top:4px;'>ONLINE</div>
                    </div>
                    <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;padding:12px;'>
                        <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                            margin-bottom:6px;'>REMINDERS</div>
                        <div style='font-size:22px;font-weight:800;color:#ffb020;'>3</div>
                    </div>
                </div>
                <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:14px;'>
                    <div style='display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:12px;'>
                        <span style='font-size:12px;font-weight:600;color:#f0f0f8;'>Task Engine</span>
                        <span style='font-size:10px;color:{active_color};
                            background:{glow_color};padding:3px 8px;border-radius:6px;'>+ New Task</span>
                    </div>
                    <div style='display:flex;align-items:center;gap:8px;padding:6px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);'>
                        <div style='width:14px;height:14px;border-radius:3px;
                            background:#00d68f;flex-shrink:0;'></div>
                        <span style='font-size:11px;color:#6b6b80;flex:1;
                            text-decoration:line-through;'>Setup database schema</span>
                        <span style='font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;
                            background:rgba(255,69,96,0.15);color:#ff4560;'>HIGH</span>
                    </div>
                    <div style='display:flex;align-items:center;gap:8px;padding:6px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);'>
                        <div style='width:14px;height:14px;border-radius:3px;
                            border:1px solid rgba(255,255,255,0.2);flex-shrink:0;'></div>
                        <span style='font-size:11px;color:#9090a8;flex:1;'>Build homepage redesign</span>
                        <span style='font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;
                            background:rgba(255,69,96,0.15);color:#ff4560;'>HIGH</span>
                    </div>
                    <div style='display:flex;align-items:center;gap:8px;padding:6px 0;'>
                        <div style='width:14px;height:14px;border-radius:3px;
                            border:1px solid rgba(255,255,255,0.2);flex-shrink:0;'></div>
                        <span style='font-size:11px;color:#9090a8;flex:1;'>Prepare poster presentation</span>
                        <span style='font-size:9px;font-weight:700;padding:2px 6px;border-radius:4px;
                            background:rgba(0,214,143,0.15);color:#00d68f;'>LOW</span>
                    </div>
                </div>
            </div>
            <div style='border-left:1px solid rgba(255,255,255,0.06);padding:20px;'>
                <div style='display:flex;align-items:center;gap:6px;margin-bottom:14px;'>
                    <span style='font-size:12px;font-weight:600;color:#f0f0f8;'>Neural Chat</span>
                    <span style='font-size:9px;background:{glow_color};color:{active_color};
                        padding:2px 6px;border-radius:4px;font-family:JetBrains Mono,monospace;'>AI ONLINE</span>
                </div>
                <div style='width:32px;height:32px;border-radius:50%;
                    background:linear-gradient(135deg,{active_color},#7c3aed);
                    display:flex;align-items:center;justify-content:center;
                    font-size:14px;margin-bottom:10px;'>A</div>
                <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;border-top-left-radius:3px;
                    padding:10px 12px;font-size:11px;color:#9090a8;line-height:1.6;margin-bottom:12px;'>
                    Aura online. You have 2 high priority tasks today. Want me to help you plan your morning?
                </div>
                <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;'>Quick Commands</div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:12px;'>
                    <div style='font-size:10px;color:{active_color};
                        background:{glow_color};border:1px solid {active_color}33;
                        padding:6px;border-radius:6px;text-align:center;'>My Tasks</div>
                    <div style='font-size:10px;color:{active_color};
                        background:{glow_color};border:1px solid {active_color}33;
                        padding:6px;border-radius:6px;text-align:center;'>Overdue?</div>
                    <div style='font-size:10px;color:{active_color};
                        background:{glow_color};border:1px solid {active_color}33;
                        padding:6px;border-radius:6px;text-align:center;'>My Notes</div>
                    <div style='font-size:10px;color:{active_color};
                        background:{glow_color};border:1px solid {active_color}33;
                        padding:6px;border-radius:6px;text-align:center;'>Prioritize</div>
                </div>
                <div style='background:#080810;border:1px solid rgba(255,255,255,0.06);
                    border-radius:8px;padding:8px 12px;font-size:10px;color:#6b6b80;'>
                    Message Aura...
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA ──
    st.markdown(f"""
    <div style='text-align:center;padding:60px 20px;
        border-top:1px solid rgba(255,255,255,0.06);'>
        <h2 style='font-size:44px;font-weight:800;letter-spacing:-0.02em;color:#f0f0f8;margin:0 0 16px;'>
            Ready to meet your Aura?
        </h2>
        <p style='font-size:16px;color:#9090a8;margin:0 0 40px;'>
            Free to use. Takes 30 seconds to set up.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Create My Aura →", key="bottom_cta"):
            redirect("Register")

    st.markdown(f"""
    <div style='text-align:center;padding:32px;border-top:1px solid rgba(255,255,255,0.06);'>
        <p style='font-size:11px;color:#6b6b80;margin:0;font-family:JetBrains Mono,monospace;'>
            AURA v1.0 · Personal AI Assistant · OSTİM Technical University
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# AUTH
# =========================
elif st.session_state.nav in ["Login", "Register"]:

    n1, n2, n3 = st.columns([1, 4, 1])
    with n1:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;padding:16px 0;'>
            <div style='width:28px;height:28px;border-radius:7px;
                background:linear-gradient(135deg,{active_color},#9b59ff);
                display:flex;align-items:center;justify-content:center;
                font-weight:900;font-size:12px;color:#050508;'>A</div>
            <span style='font-size:13px;font-weight:800;letter-spacing:0.1em;color:{active_color};'>AURA</span>
        </div>
        """, unsafe_allow_html=True)
    with n3:
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        if st.button("← Home", key="auth_back"):
            redirect("Home")

    st.markdown(f"<hr style='border-color:rgba(255,255,255,0.06);margin:0 0 40px;'>", unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='aura-auth-card'>", unsafe_allow_html=True)

        if st.session_state.nav == "Register":
            st.markdown(f"<h2 style='color:{active_color};margin-bottom:8px;font-family:Syne,sans-serif;'>Create Your Aura</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#9090a8;font-size:13px;margin-bottom:24px;'>Set up your account in seconds.</p>", unsafe_allow_html=True)
            reg_name  = st.text_input("Your Name", placeholder="John Doe")
            reg_email = st.text_input("Email",     placeholder="name@email.com")
            reg_pass  = st.text_input("Password",  type="password", placeholder="••••••••")

            import os
            if os.getenv("IS_CLOUD", "false").lower() == "true":
                st.markdown(f"""
                <div style='background:#ffb02012;border:1px solid #ffb02044;
                    border-radius:10px;padding:12px;margin-bottom:12px;'>
                    <div style='font-size:11px;color:#ffb020;'>
                        Face ID unavailable on web — account will be created without biometrics.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Create Account"):
                    if reg_name and reg_email and reg_pass:
                        register_user(reg_name, reg_email, reg_pass, None)
                        st.success("Account created! Redirecting...")
                        time.sleep(1.5)
                        redirect("Login")
                    else:
                        st.warning("All fields are required.")
            else:
                if st.button("Initialize Face Scan & Create"):
                    if reg_name and reg_email and reg_pass:
                        with st.spinner("Scanning face..."):
                            face_data = capture_face_embedding()
                            if face_data:
                                register_user(reg_name, reg_email, reg_pass, face_data)
                                st.success("Account created!")
                                time.sleep(1.5)
                                redirect("Login")
                            else:
                                st.error("Face capture failed.")
                    else:
                        st.warning("All fields are required.")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            if st.button("Already have an account? Sign in", key="go_login"):
                redirect("Login")

        else:
            st.markdown(f"<h2 style='color:{active_color};margin-bottom:8px;font-family:Syne,sans-serif;'>Welcome back.</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color:#9090a8;font-size:13px;margin-bottom:24px;'>Sign in to your Aura workspace.</p>", unsafe_allow_html=True)

            login_tab, face_tab = st.tabs(["Password Login", "Face Login"])
            with login_tab:
                l_email = st.text_input("Email",    key="l_email")
                l_pass  = st.text_input("Password", type="password", key="l_pass")
                if st.button("Sign In"):
                    token = login_user(l_email, l_pass)
                    if token:
                        st.session_state.token = token
                        redirect("Dashboard")
                    else:
                        st.error("Invalid credentials.")

            with face_tab:
                import os
                if os.getenv("IS_CLOUD", "false").lower() == "true":
                    st.markdown(f"""
                    <div style='background:#ffb02012;border:1px solid #ffb02044;
                        border-radius:10px;padding:16px;text-align:center;'>
                        <div style='font-size:13px;font-weight:700;color:#ffb020;margin-bottom:6px;'>
                            Face ID — Local Only</div>
                        <div style='font-size:11px;color:#9090a8;'>Use password login on the web.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    f_email = st.text_input("Email", key="f_email")
                    if st.button("Scan Face"):
                        user = get_user_by_email(f_email)
                        if user:
                            with st.spinner("Verifying face..."):
                                if verify_face(user.face_embedding):
                                    st.session_state.token = login_user_biometric(f_email)
                                    redirect("Dashboard")
                                else:
                                    st.error("Face not recognized.")
                        else:
                            st.error("User not found.")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            if st.button("Don't have an account? Sign up", key="go_register"):
                redirect("Register")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
elif st.session_state.nav == "Dashboard":
    if "token" not in st.session_state:
        redirect("Home")

    tasks     = get_tasks(uid)
    notes     = get_notes(uid)
    reminders = get_reminders(uid)
    overdue   = get_overdue_reminders(uid)

    _hour          = datetime.now().hour
    _greeting      = "Good morning" if _hour < 12 else "Good afternoon" if _hour < 17 else "Good evening"
    _prefs         = get_preferences(uid)
    _name          = _prefs.get("name", "Commander")
    _pending_count = len([t for t in tasks if t.status != "completed"])
    _done_count    = len([t for t in tasks if t.status == "completed"])

    # ── DASHBOARD CSS ──
    st.markdown("""
    <style>
    /* Constrain max width */
    .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    /* All buttons: compact inline */
    .stButton > button {
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        padding: 7px 14px !important;
        font-size: 11px !important;
        border-radius: 8px !important;
        margin: 0 !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        font-family: 'Syne', sans-serif !important;
        transition: opacity 0.2s !important;
        cursor: pointer !important;
    }
    [data-testid="stButton"] {
        margin-bottom: 0 !important;
        display: inline-block !important;
    }
    /* Task action buttons: tiny ghost */
    .task-actions [data-testid="stButton"] button {
        background: transparent !important;
        color: #6b6b80 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        padding: 2px 8px !important;
        font-size: 11px !important;
        border-radius: 5px !important;
        height: 24px !important;
        font-weight: 500 !important;
        letter-spacing: 0 !important;
        text-transform: none !important;
    }
    .task-actions [data-testid="stButton"] button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: #f0f0f8 !important;
        opacity: 1 !important;
    }
    /* Add / primary buttons */
    .add-btn [data-testid="stButton"] button {
        background: rgba(167,139,250,0.12) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(167,139,250,0.25) !important;
        font-weight: 700 !important;
    }
    .add-btn [data-testid="stButton"] button:hover {
        background: rgba(167,139,250,0.2) !important;
        opacity: 1 !important;
    }
    /* Quick command buttons */
    .qc-btn [data-testid="stButton"] button {
        background: rgba(167,139,250,0.1) !important;
        color: #a78bfa !important;
        border: 1px solid rgba(167,139,250,0.2) !important;
        width: 100% !important;
        justify-content: center !important;
        font-size: 10px !important;
        padding: 6px 8px !important;
    }
    /* Export button */
    .export-btn [data-testid="stButton"] button {
        background: transparent !important;
        color: #6b6b80 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .export-btn [data-testid="stButton"] button:hover {
        color: #f0f0f8 !important;
        opacity: 1 !important;
    }
    /* Strip Streamlit column gaps */
    [data-testid="stHorizontalBlock"] {
        gap: 12px !important;
        align-items: flex-start !important;
    }
    /* Chat container */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
        background: #080812 !important;
    }
    /* Search input */
    .dash-search [data-testid="stTextInput"] {
        margin-top: 12px !important;
    }
    .dash-search [data-testid="stTextInput"] input {
        background: #0c0c12 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #f0f0f8 !important;
        font-size: 13px !important;
    }
    /* Remove bottom margin from form elements inside panels */
    .dash-panel [data-testid="stVerticalBlock"] > div {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── HEADER + SEARCH ──
    hdr_col, srch_col = st.columns([3, 1])
    with hdr_col:
        st.markdown(f"""
        <div style='padding:4px 0 8px;'>
            <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                letter-spacing:0.12em;margin-bottom:6px;'>
                AURA · PERSONAL AI · {datetime.now().strftime("%A, %b %d · %H:%M")}
            </div>
            <h1 style='font-size:26px;font-weight:800;letter-spacing:-0.02em;
                line-height:1.2;margin:0 0 4px;color:#f0f0f8;font-family:Syne,sans-serif;'>
                {_greeting}, <span style='color:{active_color};font-style:italic;'>{_name}.</span>
            </h1>
            <p style='color:#9090a8;font-size:13px;margin:0;'>Here\'s your overview for today.</p>
        </div>
        """, unsafe_allow_html=True)
    with srch_col:
        st.markdown("<div class='dash-search'>", unsafe_allow_html=True)
        search_query = st.text_input("s", placeholder="Search anything...",
                                      key="global_search", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    if search_query:
        q = search_query.lower()
        matched_tasks     = [t for t in tasks     if q in t.title.lower() or q in (t.description or "").lower()]
        matched_notes     = [n for n in notes     if q in (n.title or "").lower() or q in (n.content or "").lower()]
        matched_reminders = [r for r in reminders if q in r.title.lower()]
        html = f"<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:18px;margin:10px 0;'><div style='font-size:10px;font-weight:600;letter-spacing:0.14em;color:#6b6b80;font-family:JetBrains Mono,monospace;margin-bottom:10px;'>RESULTS FOR \"{search_query.upper()}\"</div>"
        for t in matched_tasks:
            c = "#ff4560" if t.status != "completed" else "#00d68f"
            html += f"<div style='background:#12121a;border-radius:8px;padding:8px 12px;margin-bottom:5px;font-size:12px;font-weight:600;color:#f0f0f8;'>{t.title} <span style='color:{c};font-size:10px;'>{t.status.upper()}</span></div>"
        for n in matched_notes:
            html += f"<div style='background:#12121a;border-radius:8px;padding:8px 12px;margin-bottom:5px;font-size:12px;color:#9090a8;'>{n.title or 'Untitled'}</div>"
        for r in matched_reminders:
            html += f"<div style='background:#12121a;border-radius:8px;padding:8px 12px;margin-bottom:5px;font-size:12px;color:#ffb020;'>{r.title}</div>"
        if not matched_tasks and not matched_notes and not matched_reminders:
            html += "<div style='color:#6b6b80;font-size:12px;'>No results found.</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    # ── OVERDUE BANNER ──
    if overdue:
        names = ", ".join([r.title for r in overdue[:3]])
        extra = f" +{len(overdue)-3} more" if len(overdue) > 3 else ""
        st.markdown(f"""
        <div style='background:#ff456010;border:1px solid #ff456040;border-radius:12px;
            padding:12px 18px;margin:8px 0;display:flex;align-items:center;gap:12px;'>
            <span style='font-size:16px;'>⚠️</span>
            <div>
                <div style='font-size:12px;font-weight:700;color:#ff4560;'>
                    {len(overdue)} Overdue Reminder{"s" if len(overdue) > 1 else ""}</div>
                <div style='font-size:11px;color:#9090a8;'>{names}{extra}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI ROW — pure HTML grid ──

    kpi_items = [
        ("Tasks",     str(len(tasks)),      "Total tasks",    active_color),
        ("Completed", str(_done_count),     "Tasks done",     "#00d68f"),
        ("AI Status", "ONLINE",             "Neural engine",  "#00d68f"),
        ("Overdue",   str(len(overdue)),    "Need attention", "#ff4560" if overdue else "#6b6b80"),
        ("Notes",     str(len(notes)),      "In memory bank", "#9b59ff"),
    ]
    kpi_html = "<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:14px 0;'>"
    for label, value, sub, color in kpi_items:
        kpi_html += f"""<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:14px;padding:18px 20px;position:relative;overflow:hidden;min-height:110px;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,{color},transparent);'></div>
            <div style='font-size:9px;font-weight:600;letter-spacing:0.12em;color:#6b6b80;
                font-family:JetBrains Mono,monospace;margin-bottom:10px;text-transform:uppercase;'>{label}</div>
            <div style='font-size:32px;font-weight:800;color:{color};
                letter-spacing:-0.02em;line-height:1;margin-bottom:6px;'>{value}</div>
            <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>{sub}</div>
        </div>"""
    kpi_html += "</div>"
    st.markdown(kpi_html, unsafe_allow_html=True)

    # ── MAIN 2-COLUMN SPLIT ──
    col_left, col_right = st.columns([1.5, 1], gap="medium")

    # ════════════════════════
    # LEFT COLUMN
    # ════════════════════════
    with col_left:

        # MY TASKS header card
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:14px;padding:14px 18px;margin-bottom:10px;
            display:flex;justify-content:space-between;align-items:center;'>
            <div style='display:flex;align-items:center;gap:8px;'>
                <div style='width:6px;height:6px;border-radius:50%;background:{active_color};'></div>
                <span style='font-size:14px;font-weight:700;color:#f0f0f8;font-family:Syne,sans-serif;'>My Tasks</span>
            </div>
            <span style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>{_pending_count} PENDING</span>
        </div>
        """, unsafe_allow_html=True)

        if "show_add_task" not in st.session_state:
            st.session_state.show_add_task = False
        st.markdown("<div class='add-btn'>", unsafe_allow_html=True)
        if st.button("+ Add Task", key="toggle_task"):
            st.session_state.show_add_task = not st.session_state.show_add_task
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.show_add_task:
            with st.container():
                st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px;margin:8px 0;'>", unsafe_allow_html=True)
                t_title    = st.text_input("Task Title",  placeholder="e.g. Fix login bug",   key="t_title_inp")
                t_desc     = st.text_area("Description",  placeholder="Describe the task...", key="t_desc_inp", height=60)
                t_priority = st.select_slider("Priority", options=["Low","Medium","High"],    value="Medium", key="t_pri_inp")
                st.markdown("<div class='add-btn'>", unsafe_allow_html=True)
                if st.button("Confirm", key="confirm_task"):
                    if t_title:
                        create_task(t_title, t_desc, uid, t_priority)
                        st.session_state.show_add_task = False
                        st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

        # Task items
        for t in tasks:
            is_done  = t.status == "completed"
            priority = getattr(t, "priority", "Medium") or "Medium"
            p_color  = {"High":"#ff4560","Medium":"#ffb020","Low":"#00d68f"}.get(priority,"#ffb020")
            title_s  = "text-decoration:line-through;color:#6b6b80;" if is_done else "color:#f0f0f8;"
            check_s  = f"background:{p_color};" if is_done else f"border:2px solid {p_color}44;"
            tick     = "<span style='color:#050508;font-size:10px;font-weight:900;'>✓</span>" if is_done else ""
            st.markdown(f"""
            <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                border-radius:12px;padding:12px 16px;margin-bottom:4px;
                display:flex;align-items:center;gap:12px;'>
                <div style='width:18px;height:18px;border-radius:5px;{check_s}flex-shrink:0;
                    display:flex;align-items:center;justify-content:center;'>{tick}</div>
                <div style='flex:1;min-width:0;'>
                    <div style='font-size:13px;font-weight:600;{title_s}
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{t.title}</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
                        margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{t.description or "No description"}</div>
                </div>
                <span style='font-size:9px;font-weight:700;padding:3px 8px;border-radius:5px;
                    background:{p_color}18;color:{p_color};font-family:JetBrains Mono,monospace;
                    flex-shrink:0;'>{priority.upper()}</span>
            </div>
            """, unsafe_allow_html=True)
            ta1, ta2, _ = st.columns([0.07, 0.07, 0.86])
            with ta1:
                st.markdown("<div class='task-actions'>", unsafe_allow_html=True)
                if not is_done:
                    if st.button("✔", key=f"done_{t.id}"): complete_task(t.id); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with ta2:
                st.markdown("<div class='task-actions'>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{t.id}"): delete_task(t.id); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        # UPCOMING REMINDERS header
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:14px;padding:14px 18px;margin:16px 0 10px;
            display:flex;justify-content:space-between;align-items:center;'>
            <div style='display:flex;align-items:center;gap:8px;'>
                <div style='width:6px;height:6px;border-radius:50%;background:#ffb020;'></div>
                <span style='font-size:14px;font-weight:700;color:#f0f0f8;font-family:Syne,sans-serif;'>Upcoming</span>
            </div>
            <span style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>{len(reminders)} SET</span>
        </div>
        """, unsafe_allow_html=True)

        if "show_add_reminder" not in st.session_state:
            st.session_state.show_add_reminder = False
        st.markdown("<div class='add-btn'>", unsafe_allow_html=True)
        if st.button("+ Add Reminder", key="toggle_reminder"):
            st.session_state.show_add_reminder = not st.session_state.show_add_reminder
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.show_add_reminder:
            with st.container():
                st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px;margin:8px 0;'>", unsafe_allow_html=True)
                rem_title = st.text_input("Reminder", placeholder="e.g. Team standup", key="rem_title_inp")
                rem_date  = st.date_input("Due Date", key="rem_date_inp")
                rem_time  = st.time_input("Due Time", key="rem_time_inp")
                st.markdown("<div class='add-btn'>", unsafe_allow_html=True)
                if st.button("Save Reminder", key="save_rem"):
                    if rem_title:
                        due_dt = datetime.combine(rem_date, rem_time)
                        create_reminder(rem_title, due_dt, uid)
                        st.session_state.show_add_reminder = False
                        st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

        for r in overdue:
            st.markdown(f"""
            <div style='background:#ff456010;border:1px solid #ff456040;border-radius:10px;
                padding:10px 14px;margin-bottom:5px;display:flex;align-items:center;gap:10px;'>
                <div style='width:7px;height:7px;border-radius:50%;background:#ff4560;flex-shrink:0;'></div>
                <div style='flex:1;'>
                    <div style='font-size:12px;font-weight:600;color:#ff4560;'>{r.title}</div>
                    <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d · %H:%M") if r.due_date else "No date"} · OVERDUE</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        for r in reminders:
            st.markdown(f"""
            <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);border-radius:10px;
                padding:10px 14px;margin-bottom:5px;display:flex;align-items:center;gap:10px;'>
                <div style='width:7px;height:7px;border-radius:50%;background:{active_color};flex-shrink:0;'></div>
                <div style='flex:1;'>
                    <div style='font-size:12px;font-weight:600;color:#f0f0f8;'>{r.title}</div>
                    <div style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d · %H:%M") if r.due_date else "No date"}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            rb1, rb2, _ = st.columns([0.07, 0.07, 0.86])
            with rb1:
                st.markdown("<div class='task-actions'>", unsafe_allow_html=True)
                if st.button("✔", key=f"rem_done_{r.id}"): complete_reminder(r.id); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with rb2:
                st.markdown("<div class='task-actions'>", unsafe_allow_html=True)
                if st.button("✕", key=f"rem_del_{r.id}"): delete_reminder(r.id); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        if not reminders and not overdue:
            st.markdown("<div style='color:#6b6b80;font-size:12px;padding:6px 0;'>No reminders set.</div>", unsafe_allow_html=True)

        st.markdown("<div class=\'export-btn\' style=\'margin-top:16px;\'>", unsafe_allow_html=True)
        if st.button("Export All Data", key="export_btn"):
            export_lines = ["="*50, "AURA WORKSPACE EXPORT",
                f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "="*50]
            export_lines += ["TASKS", "-"*30]
            for t in tasks:
                pr = getattr(t, "priority", "Medium") or "Medium"
                st_s = "Done" if t.status == "completed" else "Pending"
                export_lines.append(f"[{pr.upper()}] {t.title} - {st_s}")
                if t.description:
                    export_lines.append(f"    {t.description}")
            export_lines += ["NOTES", "-"*30]
            for n in notes:
                export_lines.append(f"* {n.title or 'Untitled'}")
                if n.content:
                    export_lines.append(f"  {n.content}")
            export_lines += ["REMINDERS", "-"*30]
            for r in reminders:
                ds = r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date"
                export_lines.append(f"* {r.title} - {ds}")
            export_lines.append("="*50)
            st.download_button(label="Download .txt", data="\n".join(export_lines),
                file_name=f"aura_export_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain", key="download_export")
        st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════
    # RIGHT COLUMN
    # ════════════════════════
    with col_right:

        # AI ASSISTANT HEADER
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:14px;padding:14px 18px;margin-bottom:10px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div style='display:flex;align-items:center;gap:8px;'>
                    <span style='font-size:14px;font-weight:700;color:#f0f0f8;font-family:Syne,sans-serif;'>AI Assistant</span>
                    <span style='font-size:9px;font-weight:700;background:{glow_color};
                        color:{active_color};padding:2px 7px;border-radius:4px;
                        font-family:JetBrains Mono,monospace;'>NEW</span>
                </div>
                <span style='font-size:9px;color:#00d68f;font-family:JetBrains Mono,monospace;font-weight:600;'>● ONLINE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # VOICE TOGGLE
        vc1, vc2 = st.columns([1, 3])
        with vc1:
            voice_on = st.toggle("🔊", value=st.session_state.get("voice_enabled", False), key="voice_toggle")
            st.session_state["voice_enabled"] = voice_on
        with vc2:
            st.markdown(f"""
            <div style='padding-top:8px;font-size:12px;color:#9090a8;'>
                Voice Output &nbsp;
                <span style='font-size:9px;color:{"#00d68f" if voice_on else "#6b6b80"};
                    font-family:JetBrains Mono,monospace;'>{"● ACTIVE" if voice_on else "○ OFF"}</span>
            </div>
            """, unsafe_allow_html=True)

        if "last_audio" in st.session_state and voice_on:
            st.markdown(f"""
            <audio autoplay style='width:100%;height:28px;margin:4px 0;'>
                <source src='data:audio/mp3;base64,{st.session_state["last_audio"]}' type='audio/mp3'>
            </audio>
            """, unsafe_allow_html=True)

        # CHAT HISTORY as pure HTML
        if "chat" not in st.session_state:
            init_msg = f"Aura online. You have {_pending_count} pending tasks and {len(overdue)} overdue reminders. What should we focus on?"
            st.session_state.chat = [{"role": "assistant", "content": init_msg}]

        chat_html = """<div style='background:#080812;border:1px solid rgba(255,255,255,0.07);
            border-radius:12px;padding:14px;margin:8px 0;
            max-height:300px;overflow-y:auto;min-height:140px;'>"""
        for msg in st.session_state.chat:
            if msg["role"] == "assistant":
                chat_html += f"""
                <div style='display:flex;align-items:flex-start;gap:8px;margin-bottom:10px;'>
                    <div style='width:24px;height:24px;border-radius:50%;flex-shrink:0;
                        background:linear-gradient(135deg,{active_color},#7c3aed);
                        display:flex;align-items:center;justify-content:center;
                        font-size:9px;font-weight:900;color:#050508;'>A</div>
                    <div style='background:#12121a;border:1px solid rgba(255,255,255,0.06);
                        border-radius:10px;border-top-left-radius:3px;
                        padding:8px 12px;font-size:12px;line-height:1.6;
                        color:#f0f0f8;max-width:88%;'>{msg["content"]}</div>
                </div>"""
            else:
                chat_html += f"""
                <div style='display:flex;flex-direction:row-reverse;align-items:flex-start;gap:8px;margin-bottom:10px;'>
                    <div style='width:24px;height:24px;border-radius:50%;flex-shrink:0;
                        background:linear-gradient(135deg,#9b59ff,{active_color});
                        display:flex;align-items:center;justify-content:center;
                        font-size:9px;font-weight:900;color:#050508;'>U</div>
                    <div style='background:{glow_color};border:1px solid {active_color}33;
                        border-radius:10px;border-top-right-radius:3px;
                        padding:8px 12px;font-size:12px;line-height:1.6;
                        color:#f0f0f8;max-width:88%;'>{msg["content"]}</div>
                </div>"""
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        # VOICE INPUT coming soon
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:8px;margin:6px 0;'>
            <button disabled style='flex:1;padding:7px;border-radius:8px;background:#0c0c12;
                border:1px solid #2a2a3a;color:#6b6b80;font-weight:600;font-size:11px;
                cursor:not-allowed;letter-spacing:0.05em;font-family:Syne,sans-serif;'>
                🎤 SPEAK TO AURA
            </button>
            <span style='font-size:8px;font-weight:700;letter-spacing:0.08em;
                background:#ffb02015;border:1px solid #ffb02040;color:#ffb020;
                border-radius:4px;padding:3px 6px;font-family:JetBrains Mono,monospace;
                white-space:nowrap;'>SOON</span>
        </div>
        """, unsafe_allow_html=True)

        # QUICK COMMANDS 2x2
        st.markdown("""<div style='font-size:9px;font-weight:600;letter-spacing:0.12em;color:#6b6b80;
            text-transform:uppercase;font-family:JetBrains Mono,monospace;margin:8px 0 5px;'>
            Quick Commands</div>""", unsafe_allow_html=True)

        quick_prompt = None
        qr1, qr2 = st.columns(2)
        qr3, qr4 = st.columns(2)
        with qr1:
            st.markdown("<div class='qc-btn'>", unsafe_allow_html=True)
            if st.button("My Tasks",   key="qc1"): quick_prompt = "Summarize my current tasks and tell me what I should focus on first."
            st.markdown("</div>", unsafe_allow_html=True)
        with qr2:
            st.markdown("<div class='qc-btn'>", unsafe_allow_html=True)
            if st.button("Overdue?",   key="qc2"): quick_prompt = "Do I have any overdue reminders? If so, list them and suggest what to do."
            st.markdown("</div>", unsafe_allow_html=True)
        with qr3:
            st.markdown("<div class='qc-btn'>", unsafe_allow_html=True)
            if st.button("My Notes",   key="qc3"): quick_prompt = "Summarize all my notes and highlight the most important points."
            st.markdown("</div>", unsafe_allow_html=True)
        with qr4:
            st.markdown("<div class='qc-btn'>", unsafe_allow_html=True)
            if st.button("Prioritize", key="qc4"): quick_prompt = "Based on my tasks and reminders, help me prioritize what to do today."
            st.markdown("</div>", unsafe_allow_html=True)

        # CHAT INPUT
        prompt = st.chat_input("Message Aura...", key="main_chat")
        final_prompt = prompt or quick_prompt
        if final_prompt:
            st.session_state.chat.append({"role": "user", "content": final_prompt})
            user_context = build_user_context(uid)
            _pp = get_preferences(uid)
            response = get_ai_response(
                final_prompt,
                chat_history=st.session_state.chat[:-1],
                user_context=user_context,
                tasks=tasks, notes=notes, reminders=reminders,
                personality=_pp.get("personality", "🎩 Professional"),
                custom_personality=_pp.get("custom_personality", "")
            )
            st.session_state.chat.append({"role": "assistant", "content": response})
            if voice_on:
                ab = text_to_speech(response)
                if ab:
                    st.session_state["last_audio"] = ab
            st.rerun()

        # QUICK NOTES PANEL
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:14px;padding:14px 18px;margin-top:16px;
            display:flex;justify-content:space-between;align-items:center;'>
            <div style='display:flex;align-items:center;gap:8px;'>
                <div style='width:6px;height:6px;border-radius:50%;background:#9b59ff;'></div>
                <span style='font-size:14px;font-weight:700;color:#f0f0f8;font-family:Syne,sans-serif;'>Quick Notes</span>
            </div>
            <span style='font-size:9px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>{len(notes)} SAVED</span>
        </div>
        """, unsafe_allow_html=True)

        if "show_add_note" not in st.session_state:
            st.session_state.show_add_note = False
        st.markdown("<div class='add-btn' style='margin:8px 0 4px;'>", unsafe_allow_html=True)
        if st.button("+ New Note", key="toggle_note"):
            st.session_state.show_add_note = not st.session_state.show_add_note
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.show_add_note:
            with st.container():
                st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px;margin-bottom:8px;'>", unsafe_allow_html=True)
                n_title = st.text_input("Note Title", placeholder="e.g. Ideas",          key="note_title_inp")
                n_body  = st.text_area("Content",     placeholder="Write anything...",   key="note_body_inp",  height=60)
                st.markdown("<div class='add-btn'>", unsafe_allow_html=True)
                if st.button("Save Note", key="save_note"):
                    if n_title:
                        create_note(n_title, n_body, uid)
                        st.session_state.show_add_note = False
                        st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

        if notes:
            for n in notes:
                st.markdown(f"""
                <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:10px 14px;margin-bottom:5px;'>
                    <div style='font-size:12px;font-weight:700;color:#f0f0f8;margin-bottom:2px;'>{n.title}</div>
                    <div style='font-size:11px;color:#9090a8;line-height:1.5;overflow:hidden;
                        display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;'>{n.content or ""}</div>
                </div>
                """, unsafe_allow_html=True)
                nd1, _ = st.columns([0.12, 0.88])
                with nd1:
                    st.markdown("<div class='task-actions'>", unsafe_allow_html=True)
                    if st.button("✕", key=f"del_note_{n.id}"): delete_note(n.id); st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#6b6b80;font-size:12px;padding:6px 0;'>No notes yet.</div>", unsafe_allow_html=True)

    # STATUS BAR
    st.markdown(f"""
    <div class='aura-status-bar'>
        <span><span style='color:{active_color};'>●</span>&nbsp; AI ONLINE</span>
        <span><span style='color:#00d68f;'>●</span>&nbsp; AUTH</span>
        <span><span style='color:#9b59ff;'>●</span>&nbsp; SECURE</span>
        <span style='margin-left:auto;'>AURA v1.0 &nbsp;·&nbsp; aura-ai-1.streamlit.app</span>
    </div>
    """, unsafe_allow_html=True)