import streamlit as st

st.set_page_config(page_title="Aura — Your Personal AI", page_icon="✦", layout="wide")

# Read active color from session if available
if "theme" not in st.session_state:
    st.session_state.theme = "Violet"

themes = {
    "Violet": {"accent": "#a78bfa", "glow": "rgba(167, 139, 250, 0.15)"},
    "Rose":   {"accent": "#f472b6", "glow": "rgba(244, 114, 182, 0.15)"},
    "Cyan":   {"accent": "#22d3ee", "glow": "rgba(34, 211, 238, 0.15)"},
}
active_color = themes[st.session_state.theme]["accent"]
glow_color   = themes[st.session_state.theme]["glow"]

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
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}}
.stButton > button {{
    background: {active_color} !important;
    color: #050508 !important;
    border: none !important;
    padding: 14px 32px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.08em !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    text-transform: uppercase !important;
    transition: opacity 0.2s !important;
    width: auto !important;
}}
.stButton > button:hover {{
    opacity: 0.85 !important;
    color: #050508 !important;
}}
</style>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown(f"""
<div style='min-height:100vh;display:flex;flex-direction:column;align-items:center;
    justify-content:center;text-align:center;padding:60px 20px;position:relative;overflow:hidden;'>

    <!-- Background glow -->
    <div style='position:absolute;top:20%;left:50%;transform:translateX(-50%);
        width:600px;height:600px;border-radius:50%;
        background:radial-gradient(circle, {glow_color} 0%, transparent 70%);
        pointer-events:none;'></div>

    <!-- Logo -->
    <div style='width:72px;height:72px;border-radius:18px;
        background:linear-gradient(135deg,{active_color},#9b59ff);
        display:flex;align-items:center;justify-content:center;
        font-weight:900;font-size:32px;color:#050508;
        margin-bottom:32px;box-shadow:0 0 40px {glow_color};'>A</div>

    <!-- Badge -->
    <div style='display:inline-flex;align-items:center;gap:8px;
        background:{glow_color};border:1px solid {active_color}44;
        border-radius:20px;padding:6px 16px;margin-bottom:24px;'>
        <div style='width:6px;height:6px;border-radius:50%;background:{active_color};'></div>
        <span style='font-size:11px;font-weight:600;color:{active_color};
            letter-spacing:0.12em;font-family:JetBrains Mono,monospace;'>
            AI-POWERED PERSONAL ASSISTANT
        </span>
    </div>

    <!-- Headline -->
    <h1 style='font-size:clamp(40px,7vw,88px);font-weight:800;letter-spacing:-0.03em;
        line-height:1;margin:0 0 24px;color:#f0f0f8;max-width:900px;'>
        Your AI,<br>
        <span style='color:{active_color};'>perfectly tuned</span><br>
        to you.
    </h1>

    <!-- Subheadline -->
    <p style='font-size:18px;color:#9090a8;max-width:560px;line-height:1.6;
        margin:0 0 48px;font-weight:400;'>
        Aura manages your tasks, notes, and reminders — and adapts its personality
        to match how you think and work.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA buttons
c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if st.button("Get Started →", key="cta_main"):
        st.switch_page("app.py")

st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# ── FEATURES ──
st.markdown(f"""
<div style='padding:80px 40px;max-width:1100px;margin:0 auto;'>
    <div style='text-align:center;margin-bottom:60px;'>
        <div style='font-size:10px;font-weight:600;letter-spacing:0.2em;color:#6b6b80;
            font-family:JetBrains Mono,monospace;margin-bottom:12px;'>WHAT AURA DOES</div>
        <h2 style='font-size:40px;font-weight:800;letter-spacing:-0.02em;color:#f0f0f8;margin:0;'>
            Everything you need,<br>nothing you don't.
        </h2>
    </div>

    <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:24px;'>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,{active_color},transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>📌</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Task Engine</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                Deploy tasks with priority levels. Track what's pending, what's done,
                and what needs your attention first.
            </p>
        </div>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#9b59ff,transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>🧠</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Neural Chat</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                Talk to an AI that knows your tasks, notes, and goals.
                Switch personalities — from professional to hype coach.
            </p>
        </div>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#00d68f,transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>⏰</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Smart Reminders</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                Set reminders and get alerted when they're overdue.
                Never miss what matters.
            </p>
        </div>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#ffb020,transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>📝</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Quick Notes</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                Capture ideas instantly. Your notes are always searchable
                and available to your AI.
            </p>
        </div>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#f472b6,transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>🎭</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>AI Personalities</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                Choose from Professional, Friendly, Mentor, Sarcastic,
                Minimalist, Hype Coach — or define your own.
            </p>
        </div>

        <div style='background:#0c0c12;border:1px solid rgba(255,255,255,0.06);
            border-radius:20px;padding:32px;position:relative;overflow:hidden;'>
            <div style='position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#22d3ee,transparent);'></div>
            <div style='font-size:32px;margin-bottom:16px;'>🔒</div>
            <h3 style='font-size:18px;font-weight:700;color:#f0f0f8;margin:0 0 10px;'>Secure by Default</h3>
            <p style='font-size:13px;color:#9090a8;line-height:1.6;margin:0;'>
                PBKDF2 password hashing and JWT tokens keep your
                data private and secure.
            </p>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# ── CTA BOTTOM ──
st.markdown(f"""
<div style='padding:80px 40px;text-align:center;'>
    <h2 style='font-size:40px;font-weight:800;letter-spacing:-0.02em;
        color:#f0f0f8;margin:0 0 16px;'>
        Ready to meet your Aura?
    </h2>
    <p style='font-size:16px;color:#9090a8;margin:0 0 40px;'>
        Free to use. No credit card required.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if st.button("Launch Aura →", key="cta_bottom"):
        st.switch_page("app.py")

# ── FOOTER ──
st.markdown(f"""
<div style='padding:40px;text-align:center;border-top:1px solid rgba(255,255,255,0.06);
    margin-top:40px;'>
    <div style='display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:12px;'>
        <div style='width:24px;height:24px;border-radius:6px;
            background:linear-gradient(135deg,{active_color},#9b59ff);
            display:flex;align-items:center;justify-content:center;
            font-weight:900;font-size:11px;color:#050508;'>A</div>
        <span style='font-size:13px;font-weight:800;letter-spacing:0.1em;color:{active_color};'>AURA</span>
    </div>
    <p style='font-size:11px;color:#6b6b80;margin:0;font-family:JetBrains Mono,monospace;'>
        AURA v1.0 · Personal AI Assistant · Built with ❤️
    </p>
</div>
""", unsafe_allow_html=True)
