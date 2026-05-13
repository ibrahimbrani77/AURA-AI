import streamlit as st

st.set_page_config(page_title="Aura — Your Personal AI", page_icon="✦", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "Violet"

themes = {
    "Violet": {"accent": "#a78bfa", "glow": "rgba(167, 139, 250, 0.15)", "glow2": "rgba(167,139,250,0.06)"},
    "Rose":   {"accent": "#f472b6", "glow": "rgba(244, 114, 182, 0.15)", "glow2": "rgba(244,114,182,0.06)"},
    "Cyan":   {"accent": "#22d3ee", "glow": "rgba(34, 211, 238, 0.15)",  "glow2": "rgba(34,211,238,0.06)"},
}
active_color = themes[st.session_state.theme]["accent"]
glow_color   = themes[st.session_state.theme]["glow"]
glow2_color  = themes[st.session_state.theme]["glow2"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, h1, h2, h3, label {{
    font-family: 'Syne', sans-serif !important;
}}
.stApp {{ background: #050508 !important; color: #f0f0f8 !important; }}
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
    padding: 14px 36px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.08em !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    width: auto !important;
    box-shadow: 0 0 24px {glow_color} !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 32px {glow_color} !important;
    color: #050508 !important;
}}

/* ── HERO ── */
.hero-wrap {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 80px 24px 60px;
    position: relative;
    overflow: hidden;
}}
.hero-orb {{
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    filter: blur(80px);
    animation: orb-float 8s ease-in-out infinite;
}}
@keyframes orb-float {{
    0%, 100% {{ transform: translateY(0px) scale(1); opacity: 0.6; }}
    50%       {{ transform: translateY(-20px) scale(1.05); opacity: 0.9; }}
}}
.hero-logo {{
    width: 80px; height: 80px; border-radius: 22px;
    background: linear-gradient(135deg, {active_color}, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 36px; color: #050508;
    margin: 0 auto 36px;
    box-shadow: 0 0 60px {glow_color}, 0 0 120px {glow2_color};
    animation: logo-pulse 3s ease-in-out infinite;
}}
@keyframes logo-pulse {{
    0%, 100% {{ box-shadow: 0 0 40px {glow_color}, 0 0 80px {glow2_color}; }}
    50%       {{ box-shadow: 0 0 80px {glow_color}, 0 0 160px {glow2_color}; }}
}}
.hero-badge {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {glow_color}; border: 1px solid {active_color}44;
    border-radius: 24px; padding: 7px 18px; margin-bottom: 28px;
}}
.hero-badge-dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: {active_color};
    animation: badge-blink 2s ease-in-out infinite;
}}
@keyframes badge-blink {{
    0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }}
}}
.hero-h1 {{
    font-size: clamp(48px, 8vw, 96px);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.0;
    color: #f0f0f8;
    max-width: 960px;
    margin: 0 auto 28px;
}}
.hero-sub {{
    font-size: clamp(15px, 2vw, 19px);
    color: #9090a8;
    max-width: 580px;
    line-height: 1.7;
    margin: 0 auto 56px;
    font-weight: 400;
}}

/* ── STATS BAR ── */
.stats-bar {{
    display: flex;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
    padding: 28px 40px;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: rgba(12,12,18,0.6);
    backdrop-filter: blur(12px);
    margin-top: 16px;
}}
.stat-item {{ text-align: center; }}
.stat-value {{
    font-size: 32px; font-weight: 800;
    color: {active_color}; letter-spacing: -0.03em; line-height: 1;
}}
.stat-label {{
    font-size: 10px; color: #6b6b80;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-top: 4px;
}}

/* ── HOW IT WORKS ── */
.steps-section {{
    padding: 100px 40px;
    max-width: 1100px;
    margin: 0 auto;
}}
.section-eyebrow {{
    font-size: 10px; font-weight: 600;
    letter-spacing: 0.22em; color: #6b6b80;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase; margin-bottom: 14px;
    text-align: center;
}}
.section-headline {{
    font-size: clamp(30px, 4vw, 44px);
    font-weight: 800; letter-spacing: -0.025em;
    color: #f0f0f8; text-align: center;
    margin-bottom: 64px;
}}
.steps-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    position: relative;
}}
.step-card {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 36px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s;
}}
.step-card:hover {{
    border-color: {active_color}55;
    transform: translateY(-4px);
}}
.step-number {{
    font-size: 11px; font-weight: 700;
    color: {active_color}; letter-spacing: 0.14em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 20px; display: block;
}}
.step-icon {{ font-size: 40px; margin-bottom: 18px; display: block; }}
.step-title {{
    font-size: 18px; font-weight: 700;
    color: #f0f0f8; margin-bottom: 10px;
}}
.step-desc {{
    font-size: 13px; color: #9090a8; line-height: 1.75;
}}

/* ── FEATURE CARDS ── */
.features-section {{
    padding: 80px 40px;
    max-width: 1100px;
    margin: 0 auto;
    border-top: 1px solid rgba(255,255,255,0.05);
}}
.feat-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}}
.feat-card {{
    background: #0c0c12;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 30px 28px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
    cursor: default;
}}
.feat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}}
.feat-card-bar {{
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--card-color), transparent);
}}
.feat-icon {{ font-size: 34px; margin-bottom: 16px; display: block; }}
.feat-title {{
    font-size: 17px; font-weight: 700;
    color: #f0f0f8; margin-bottom: 10px;
}}
.feat-desc {{
    font-size: 13px; color: #9090a8; line-height: 1.7;
}}

/* ── BOTTOM CTA ── */
.cta-section {{
    padding: 100px 40px;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
}}
.cta-glow {{
    position: absolute;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, {glow_color} 0%, transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
}}
.cta-h2 {{
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800; letter-spacing: -0.025em;
    color: #f0f0f8; margin-bottom: 18px;
    position: relative; z-index: 1;
}}
.cta-sub {{
    font-size: 16px; color: #9090a8;
    margin-bottom: 48px;
    position: relative; z-index: 1;
}}

/* ── FOOTER ── */
.footer {{
    padding: 40px;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.06);
}}
.footer-logo {{
    display: flex; align-items: center; justify-content: center;
    gap: 10px; margin-bottom: 14px;
}}
.footer-logo-icon {{
    width: 26px; height: 26px; border-radius: 7px;
    background: linear-gradient(135deg, {active_color}, #9b59ff);
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 12px; color: #050508;
}}
.footer-wordmark {{
    font-size: 13px; font-weight: 800;
    letter-spacing: 0.1em; color: {active_color};
}}
.footer-copy {{
    font-size: 11px; color: #6b6b80;
    font-family: 'JetBrains Mono', monospace;
}}

/* ── RESPONSIVE ── */
@media (max-width: 900px) {{
    .steps-grid, .feat-grid {{ grid-template-columns: 1fr 1fr !important; }}
}}
@media (max-width: 600px) {{
    .steps-grid, .feat-grid {{ grid-template-columns: 1fr !important; }}
    .stats-bar {{ gap: 28px; }}
    .hero-wrap {{ padding: 80px 16px 40px; }}
}}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <!-- Animated background orbs -->
    <div class="hero-orb" style="width:500px;height:500px;top:10%;left:50%;
        transform:translateX(-50%);
        background:radial-gradient(circle,{glow_color} 0%,transparent 70%);"></div>
    <div class="hero-orb" style="width:300px;height:300px;top:20%;left:15%;
        background:radial-gradient(circle,rgba(124,58,237,0.12) 0%,transparent 70%);
        animation-delay:2s;animation-duration:10s;"></div>
    <div class="hero-orb" style="width:240px;height:240px;bottom:15%;right:12%;
        background:radial-gradient(circle,rgba(244,114,182,0.08) 0%,transparent 70%);
        animation-delay:4s;animation-duration:12s;"></div>

    <!-- Logo -->
    <div class="hero-logo">✦</div>

    <!-- Badge -->
    <div class="hero-badge">
        <div class="hero-badge-dot"></div>
        <span style="font-size:11px;font-weight:600;color:{active_color};
            letter-spacing:0.12em;font-family:'JetBrains Mono',monospace;">
            AI-POWERED PERSONAL ASSISTANT
        </span>
    </div>

    <!-- Headline -->
    <h1 class="hero-h1">
        Your AI,<br>
        <span style="color:{active_color};">perfectly tuned</span><br>
        to you.
    </h1>

    <!-- Subheadline -->
    <p class="hero-sub">
        Aura manages your tasks, notes, and reminders — and adapts its personality
        to match how <em>you</em> think and work.
    </p>
</div>
""", unsafe_allow_html=True)

# CTA button
c1, c2, c3 = st.columns([2.5, 1, 2.5])
with c2:
    if st.button("Get Started →", key="cta_main"):
        st.switch_page("app.py")

# Stats bar
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-value">6</div>
        <div class="stat-label">AI Personalities</div>
    </div>
    <div class="stat-item" style="border-left:1px solid rgba(255,255,255,0.07);border-right:1px solid rgba(255,255,255,0.07);padding:0 48px;">
        <div class="stat-value">∞</div>
        <div class="stat-label">Tasks & Notes</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">1-Click</div>
        <div class="stat-label">Data Export</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="steps-section">
    <div class="section-eyebrow">How It Works</div>
    <h2 class="section-headline">Up and running in seconds.</h2>

    <div class="steps-grid">
        <div class="step-card">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,{active_color},transparent);"></div>
            <span class="step-number">STEP 01</span>
            <span class="step-icon">👤</span>
            <div class="step-title">Create your account</div>
            <p class="step-desc">Sign up in seconds with your name, email, and password.
                Optionally register your face for biometric login.</p>
        </div>
        <div class="step-card">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#9b59ff,transparent);"></div>
            <span class="step-number">STEP 02</span>
            <span class="step-icon">🎭</span>
            <div class="step-title">Pick a personality</div>
            <p class="step-desc">Choose how Aura talks to you — Professional, Friendly,
                Mentor, Sarcastic, Minimalist, Hype Coach, or write your own.</p>
        </div>
        <div class="step-card">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
                background:linear-gradient(90deg,#00d68f,transparent);"></div>
            <span class="step-number">STEP 03</span>
            <span class="step-icon">⚡</span>
            <div class="step-title">Start working</div>
            <p class="step-desc">Add tasks, set reminders, jot notes, and chat with an AI
                that knows your full context and adapts to your workflow.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="features-section">
    <div class="section-eyebrow">What Aura Does</div>
    <h2 class="section-headline">Everything you need,<br>nothing you don't.</h2>

    <div class="feat-grid">
        <div class="feat-card" style="--card-color:{active_color};">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">📌</span>
            <div class="feat-title">Task Engine</div>
            <p class="feat-desc">Deploy tasks with High, Medium, or Low priority.
                I'll help you figure out what to tackle first.</p>
        </div>
        <div class="feat-card" style="--card-color:#9b59ff;">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">🧠</span>
            <div class="feat-title">Neural Chat</div>
            <p class="feat-desc">Talk to an AI that knows your tasks, notes, and goals.
                My answers are actually useful — not generic.</p>
        </div>
        <div class="feat-card" style="--card-color:#f472b6;">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">🎭</span>
            <div class="feat-title">AI Personalities</div>
            <p class="feat-desc">Professional, Friendly, Mentor, Sarcastic,
                Minimalist, or Hype Coach — or define your own.</p>
        </div>
        <div class="feat-card" style="--card-color:#ffb020;">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">⏰</span>
            <div class="feat-title">Smart Reminders</div>
            <p class="feat-desc">Set reminders and get alerted when they're overdue.
                Never miss what matters.</p>
        </div>
        <div class="feat-card" style="--card-color:#00d68f;">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">📝</span>
            <div class="feat-title">Quick Notes</div>
            <p class="feat-desc">Capture ideas instantly. Your notes are always
                searchable and available to your AI.</p>
        </div>
        <div class="feat-card" style="--card-color:#22d3ee;">
            <div class="feat-card-bar"></div>
            <span class="feat-icon">🔒</span>
            <div class="feat-title">Secure by Default</div>
            <p class="feat-desc">PBKDF2 password hashing and JWT tokens keep your
                data private and yours.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BOTTOM CTA ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cta-section">
    <div class="cta-glow"></div>
    <h2 class="cta-h2">Ready to meet your Aura?</h2>
    <p class="cta-sub">Free to use. No credit card. Takes 30 seconds to set up.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([2.5, 1, 2.5])
with c2:
    if st.button("Launch Aura →", key="cta_bottom"):
        st.switch_page("app.py")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <div class="footer-logo">
        <div class="footer-logo-icon">A</div>
        <span class="footer-wordmark">AURA</span>
    </div>
    <p class="footer-copy">AURA v1.0 · Personal AI Assistant · Built with ❤️</p>
</div>
""", unsafe_allow_html=True)
