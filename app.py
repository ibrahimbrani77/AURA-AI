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
.stButton > button:hover {{ opacity: 0.85 !important; color: #050508 !important; }}
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
        saved_personality = _prefs_sidebar.get("personality", "🎩 Professional")
        selected_personality = st.selectbox(
            "Personality", personality_options,
            index=personality_options.index(saved_personality) if saved_personality in personality_options else 0,
            key="personality_select", label_visibility="collapsed"
        )
        personality_defaults = {
            "🎩 Professional": "Formal, precise, and concise. No casual language.",
            "😊 Friendly":     "Warm, encouraging, and conversational.",
            "🧙 Mentor":       "Wise, patient, and guiding with thoughtful advice.",
            "😏 Sarcastic":    "Witty and sarcastic with dry humor, but still helpful.",
            "⚡ Minimalist":   "Ultra-concise. Short answers, bullet points, no fluff.",
            "🔥 Hype Coach":   "Energetic, motivating, and enthusiastic about everything!",
            "✨ Custom":       ""
        }
        custom_desc = st.text_area(
            "Personality Description",
            value=_prefs_sidebar.get("custom_personality", personality_defaults.get(selected_personality, "")),
            placeholder="Describe how Aura should behave...",
            height=80, key="custom_personality_input", label_visibility="collapsed"
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

    _hour = datetime.now().hour
    _greeting = "Good morning" if _hour < 12 else "Good afternoon" if _hour < 17 else "Good evening"
    _prefs        = get_preferences(uid)
    _name         = _prefs.get("name", "Commander")
    _pending_count = len([t for t in tasks if t.status != "completed"])

    st.markdown(f"""
    <div style='margin-bottom:16px;'>
        <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
            letter-spacing:0.12em;margin-bottom:8px;'>
            AURA · PERSONAL AI · {datetime.now().strftime("%A, %b %d · %H:%M")}
        </div>
        <h1 style='font-size:26px;font-weight:800;letter-spacing:-0.02em;
            line-height:1;margin:0;color:#f0f0f8;font-family:Syne,sans-serif;'>
            {_greeting}, <span style='color:{active_color};'>{_name}.</span>
        </h1>
        <p style='color:#9090a8;font-size:13px;margin-top:8px;margin-bottom:0;'>
            {_pending_count} tasks pending &nbsp;·&nbsp;
            {len(notes)} notes &nbsp;·&nbsp;
            {len(reminders)} reminders &nbsp;·&nbsp;
            AI ready
        </p>
    </div>
    """, unsafe_allow_html=True)

    if overdue:
        overdue_names = ", ".join([r.title for r in overdue[:3]])
        extra = f" +{len(overdue)-3} more" if len(overdue) > 3 else ""
        st.markdown(f"""
        <div style='background:#ff456012;border:1px solid #ff456044;border-radius:12px;
            padding:12px 18px;margin-bottom:16px;display:flex;align-items:center;gap:12px;'>
            <span style='font-size:20px;'>⚠️</span>
            <div>
                <div style='font-size:12px;font-weight:700;color:#ff4560;'>
                    {len(overdue)} OVERDUE REMINDER{"S" if len(overdue) > 1 else ""}
                </div>
                <div style='font-size:11px;color:#9090a8;'>{overdue_names}{extra}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    for col, label, value, sub, color in [
        (m1, "ACTIVE TASKS", str(len(tasks)),     "tasks deployed",     active_color),
        (m2, "NOTES SAVED",  str(len(notes)),     "in memory bank",     "#9b59ff"),
        (m3, "AI STATUS",    "ONLINE",            "neural engine ready", "#00d68f"),
        (m4, "REMINDERS",    str(len(reminders)), "upcoming alerts",    "#ffb020"),
    ]:
        with col:
            st.markdown(f"""
            <div class='aura-metric'>
                <div class='aura-metric-bar' style='background:linear-gradient(90deg,{color},transparent);'></div>
                <div class='aura-metric-label'>{label}</div>
                <div class='aura-metric-value' style='color:{color};'>{value}</div>
                <div class='aura-metric-sub'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    search_query = st.text_input("Search", placeholder="Search tasks, notes, reminders...",
                                  key="global_search", label_visibility="collapsed")
    if search_query:
        q = search_query.lower()
        matched_tasks     = [t for t in tasks     if q in t.title.lower() or q in (t.description or "").lower()]
        matched_notes     = [n for n in notes     if q in (n.title or "").lower() or q in (n.content or "").lower()]
        matched_reminders = [r for r in reminders if q in r.title.lower()]
        st.markdown(f"""
        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);
            border-radius:12px;padding:16px;margin-bottom:16px;'>
            <div style='font-size:10px;font-weight:600;letter-spacing:0.14em;
                color:#6b6b80;font-family:JetBrains Mono,monospace;margin-bottom:12px;'>
                SEARCH RESULTS FOR "{search_query.upper()}"
            </div>
        """, unsafe_allow_html=True)
        if matched_tasks:
            st.markdown(f"<div style='font-size:11px;color:{active_color};font-weight:700;margin-bottom:6px;'>TASKS ({len(matched_tasks)})</div>", unsafe_allow_html=True)
            for t in matched_tasks:
                tag_color = "#ff4560" if t.status != "completed" else "#00d68f"
                st.markdown(f"""<div style='background:#12121a;border-radius:8px;padding:10px 14px;margin-bottom:6px;'>
                    <span style='font-size:12px;font-weight:600;color:#f0f0f8;'>{t.title}</span>
                    <span style='font-size:10px;color:{tag_color};margin-left:8px;'>{t.status.upper()}</span>
                    <div style='font-size:11px;color:#6b6b80;margin-top:2px;'>{t.description or ""}</div>
                </div>""", unsafe_allow_html=True)
        if matched_notes:
            st.markdown(f"<div style='font-size:11px;color:#9b59ff;font-weight:700;margin-bottom:6px;margin-top:10px;'>NOTES ({len(matched_notes)})</div>", unsafe_allow_html=True)
            for n in matched_notes:
                st.markdown(f"""<div style='background:#12121a;border-radius:8px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:12px;font-weight:600;color:#f0f0f8;'>{n.title or "Untitled"}</div>
                    <div style='font-size:11px;color:#6b6b80;margin-top:2px;'>{n.content or ""}</div>
                </div>""", unsafe_allow_html=True)
        if matched_reminders:
            st.markdown(f"<div style='font-size:11px;color:#ffb020;font-weight:700;margin-bottom:6px;margin-top:10px;'>REMINDERS ({len(matched_reminders)})</div>", unsafe_allow_html=True)
            for r in matched_reminders:
                st.markdown(f"""<div style='background:#12121a;border-radius:8px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:12px;font-weight:600;color:#f0f0f8;'>{r.title}</div>
                    <div style='font-size:11px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date"}</div>
                </div>""", unsafe_allow_html=True)
        if not matched_tasks and not matched_notes and not matched_reminders:
            st.markdown("<div style='color:#6b6b80;font-size:12px;'>No results found.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        st.markdown(f"""
        <div class='aura-panel-header'>
            <div style='width:6px;height:6px;border-radius:50%;background:{active_color};flex-shrink:0;'></div>
            Task Engine
            <span style='margin-left:auto;font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>{len(tasks)} PENDING</span>
        </div>
        """, unsafe_allow_html=True)

        if "show_add_task" not in st.session_state:
            st.session_state.show_add_task = False
        if st.button("Deploy New Task", key="toggle_task"):
            st.session_state.show_add_task = not st.session_state.show_add_task
        if st.session_state.show_add_task:
            st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;'>", unsafe_allow_html=True)
            t_title    = st.text_input("Task Title",  placeholder="e.g. Fix login bug")
            t_desc     = st.text_area("Description",  placeholder="Describe the task...")
            t_priority = st.select_slider("Priority", options=["Low", "Medium", "High"], value="Medium")
            if st.button("Confirm Deployment"):
                if t_title:
                    create_task(t_title, t_desc, uid, t_priority)
                    st.session_state.show_add_task = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        for t in tasks:
            tag_color = "#ff4560" if t.status != "completed" else "#00d68f"
            tag_label = "PENDING" if t.status != "completed" else "DONE"
            priority  = getattr(t, "priority", "Medium") or "Medium"
            p_color   = {"High": "#ff4560", "Medium": "#ffb020", "Low": "#00d68f"}.get(priority, "#ffb020")
            st.markdown(f"""
            <div class='aura-task'>
                <div style='display:flex;align-items:center;justify-content:space-between;'>
                    <div>
                        <div class='aura-task-title'>{t.title}</div>
                        <div class='aura-task-desc'>{t.description or "No description"}</div>
                    </div>
                    <div style='display:flex;gap:6px;align-items:center;'>
                        <span class='aura-tag' style='background:{p_color}22;color:{p_color};'>{priority.upper()}</span>
                        <span class='aura-tag' style='background:{tag_color}22;color:{tag_color};'>{tag_label}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, _ = st.columns([0.15, 0.15, 0.7])
            if t.status != "completed":
                if c1.button("✔", key=f"done_{t.id}"):
                    complete_task(t.id); st.rerun()
            if c2.button("✕", key=f"del_{t.id}"):
                delete_task(t.id); st.rerun()

        st.markdown("""<div style='margin-top:24px;margin-bottom:10px;font-size:10px;font-weight:600;
            letter-spacing:0.14em;color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;'>Quick Notes</div>""", unsafe_allow_html=True)

        if notes:
            for n in notes:
                st.markdown(f"""<div class='aura-note'>
                    <div class='aura-note-title'>{n.title}</div>
                    <div class='aura-note-body'>{n.content or ""}</div>
                </div>""", unsafe_allow_html=True)
                nd1, nd2, _ = st.columns([0.15, 0.15, 0.7])
                if nd2.button("✕", key=f"del_note_{n.id}"):
                    delete_note(n.id); st.rerun()
        else:
            st.markdown("<div style='color:#6b6b80;font-size:12px;margin-bottom:10px;'>No notes yet.</div>", unsafe_allow_html=True)

        if "show_add_note" not in st.session_state:
            st.session_state.show_add_note = False
        if st.button("New Note", key="toggle_note"):
            st.session_state.show_add_note = not st.session_state.show_add_note
        if st.session_state.show_add_note:
            st.markdown("<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:16px;margin-bottom:12px;'>", unsafe_allow_html=True)
            n_title = st.text_input("Note Title", placeholder="e.g. Ideas")
            n_body  = st.text_area("Content",     placeholder="Write anything...")
            if st.button("Save Note"):
                if n_title:
                    create_note(n_title, n_body, uid)
                    st.session_state.show_add_note = False; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div style='margin-top:24px;margin-bottom:10px;font-size:10px;font-weight:600;
            letter-spacing:0.14em;color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;'>Reminders</div>""", unsafe_allow_html=True)

        if overdue:
            for r in overdue:
                st.markdown(f"""<div style='background:#ff456012;border:1px solid #ff456044;
                    border-radius:10px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:12px;font-weight:700;color:#ff4560;'>OVERDUE — {r.title}</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date"}</div>
                </div>""", unsafe_allow_html=True)

        if reminders:
            for r in reminders:
                st.markdown(f"""<div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
                    border-radius:10px;padding:10px 14px;margin-bottom:6px;'>
                    <div style='font-size:13px;font-weight:600;color:#f0f0f8;'>{r.title}</div>
                    <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;'>
                        {r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date set"}</div>
                </div>""", unsafe_allow_html=True)
                r1, r2, _ = st.columns([0.15, 0.15, 0.7])
                if r1.button("✔", key=f"rem_done_{r.id}"):
                    complete_reminder(r.id); st.rerun()
                if r2.button("✕", key=f"rem_del_{r.id}"):
                    delete_reminder(r.id); st.rerun()
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
                    due_dt = datetime.combine(rem_date, rem_time)
                    create_reminder(rem_title, due_dt, uid)
                    st.session_state.show_add_reminder = False; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div style='margin-top:24px;margin-bottom:10px;font-size:10px;font-weight:600;
            letter-spacing:0.14em;color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;'>Export Data</div>""", unsafe_allow_html=True)

        if st.button("Export All Data", key="export_btn"):
            lines = ["="*50, "AURA — WORKSPACE EXPORT",
                     f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "="*50, "\n📌 TASKS", "-"*30]
            if tasks:
                for t in tasks:
                    priority = getattr(t, "priority", "Medium") or "Medium"
                    status = "✔ Done" if t.status == "completed" else "○ Pending"
                    lines.append(f"[{priority.upper()}] {t.title} — {status}")
                    if t.description: lines.append(f"    {t.description}")
            else:
                lines.append("No tasks.")
            lines += ["\n📝 NOTES", "-"*30]
            if notes:
                for n in notes:
                    lines.append(f"• {n.title or 'Untitled'}")
                    if n.content: lines.append(f"  {n.content}")
            else:
                lines.append("No notes.")
            lines += ["\n⏰ REMINDERS", "-"*30]
            if reminders:
                for r in reminders:
                    date_str = r.due_date.strftime("%b %d, %Y %H:%M") if r.due_date else "No date"
                    lines.append(f"• {r.title} — {date_str}")
            else:
                lines.append("No reminders.")
            lines.append("\n" + "="*50)
            st.download_button(label="Download .txt", data="\n".join(lines),
                file_name=f"aura_export_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain", key="download_export")

    with col_right:
        st.markdown(f"""
        <div class='aura-panel-header'>
            <div style='width:6px;height:6px;border-radius:50%;background:#9b59ff;flex-shrink:0;'></div>
            Neural Chat
            <span style='margin-left:auto;font-size:10px;color:{active_color};
                font-family:JetBrains Mono,monospace;'>AI ONLINE</span>
        </div>
        """, unsafe_allow_html=True)

        if "chat" not in st.session_state:
            st.session_state.chat = [{"role": "assistant", "content": "Aura online. How can I help you today?"}]

        chat_container = st.container(height=380)
        with chat_container:
            for msg in st.session_state.chat:
                if msg["role"] == "assistant":
                    st.markdown(f"""<div class='aura-chat-ai'>
                        <div class='aura-av'>A</div>
                        <div class='aura-bubble-ai'>{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class='aura-chat-user'>
                        <div class='aura-av' style='background:linear-gradient(135deg,#9b59ff,{active_color});'>U</div>
                        <div class='aura-bubble-user'>{msg['content']}</div>
                    </div>""", unsafe_allow_html=True)

        # ── VOICE OUTPUT ──
        vc1, vc2 = st.columns([1, 3])
        with vc1:
            voice_on = st.toggle("🔊 Voice", value=st.session_state.get("voice_enabled", False), key="voice_toggle")
            st.session_state["voice_enabled"] = voice_on

        if "last_audio" in st.session_state and st.session_state["voice_enabled"]:
            audio_b64 = st.session_state["last_audio"]
            st.markdown(f"""
            <audio autoplay style='width:100%;margin-bottom:4px;'>
                <source src='data:audio/mp3;base64,{audio_b64}' type='audio/mp3'>
            </audio>
            """, unsafe_allow_html=True)

        # ── VOICE INPUT (coming soon) ──
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
            <button disabled style='
                flex:1;padding:10px;border-radius:10px;
                background:#12121a;border:2px solid #3a3a4a;
                color:#6b6b80;font-weight:700;font-size:12px;
                cursor:not-allowed;letter-spacing:0.08em;'>
                🎤 SPEAK TO AURA
            </button>
            <span style='
                font-size:9px;font-weight:700;letter-spacing:0.1em;
                background:#ffb02022;border:1px solid #ffb02066;
                color:#ffb020;border-radius:6px;padding:4px 8px;
                font-family:JetBrains Mono,monospace;white-space:nowrap;'>
                CLOUD SOON
            </span>
        </div>
        <div style='font-size:10px;color:#6b6b80;font-family:JetBrains Mono,monospace;
            margin-bottom:8px;'>
            Voice input available on desktop · 🔊 Voice output active
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style='font-size:10px;font-weight:600;letter-spacing:0.14em;
            color:#6b6b80;text-transform:uppercase;
            font-family:JetBrains Mono,monospace;margin-bottom:8px;margin-top:8px;'>
            Quick Commands</div>""", unsafe_allow_html=True)

        qc1, qc2, qc3, qc4 = st.columns(4)
        quick_prompt = None
        if qc1.button("My Tasks",   key="qc1"): quick_prompt = "Summarize my current tasks and tell me what I should focus on first."
        if qc2.button("Overdue?",   key="qc2"): quick_prompt = "Do I have any overdue reminders? If so, list them and suggest what to do."
        if qc3.button("My Notes",   key="qc3"): quick_prompt = "Summarize all my notes and highlight the most important points."
        if qc4.button("Prioritize", key="qc4"): quick_prompt = "Based on my tasks and reminders, help me prioritize what to do today."

        prompt = st.chat_input("Message Aura...", key="main_chat")
        final_prompt = prompt or quick_prompt
        if final_prompt:
            st.session_state.chat.append({"role": "user", "content": final_prompt})
            user_context = build_user_context(uid)
            _personality_prefs = get_preferences(uid)
            response = get_ai_response(
                final_prompt,
                chat_history=st.session_state.chat[:-1],
                user_context=user_context,
                tasks=tasks, notes=notes, reminders=reminders,
                personality=_personality_prefs.get("personality", "🎩 Professional"),
                custom_personality=_personality_prefs.get("custom_personality", "")
            )
            st.session_state.chat.append({"role": "assistant", "content": response})
            if st.session_state.get("voice_enabled", False):
                audio_b64 = text_to_speech(response)
                if audio_b64:
                    st.session_state["last_audio"] = audio_b64
            st.rerun()

    st.markdown(f"""
    <div class='aura-status-bar'>
        <span><span style='color:{active_color};'>●</span>&nbsp; AI ONLINE</span>
        <span><span style='color:#00d68f;'>●</span>&nbsp; AUTH</span>
        <span><span style='color:#9b59ff;'>●</span>&nbsp; SECURE</span>
        <span style='margin-left:auto;'>AURA v1.0 &nbsp;·&nbsp; aura-ai.streamlit.app</span>
    </div>
    """, unsafe_allow_html=True)