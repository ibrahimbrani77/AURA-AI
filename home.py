import streamlit as st

st.set_page_config(page_title="Aura — Your Personal AI", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

# Theme Setup
theme = {"accent": "#a78bfa", "glow": "rgba(167, 139, 250, 0.15)", "bg": "#050508", "card_bg": "#0c0c12"}
active_color = theme["accent"]
glow_color = theme["glow"]

# --- GLOBAL CSS ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, h1, h2, h3, h4, h5, h6, label {{
    font-family: 'Syne', sans-serif !important;
}}

.stApp {{
    background-color: {theme['bg']} !important;
    color: #f0f0f8 !important;
}}

/* Hide default Streamlit headers and footers */
header, footer {{ visibility: hidden; }}
.block-container {{
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1300px !important;
}}

/* Custom Button Styling */
.stButton > button {{
    background: {active_color} !important;
    color: #050508 !important;
    border: none !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}}
.stButton > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px {glow_color} !important;
}}

/* Secondary Button */
.btn-secondary > button {{
    background: transparent !important;
    color: #f0f0f8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}}
.btn-secondary > button:hover {{
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.2) !important;
}}

/* Glassmorphism Dashboard Preview */
.glass-panel {{
    background: linear-gradient(145deg, rgba(12,12,18,0.9), rgba(12,12,18,0.4));
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}}

.glass-panel::before {{
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at center, {glow_color} 0%, transparent 50%);
    opacity: 0.5;
    pointer-events: none;
    z-index: 0;
}}

/* Bento Box Grid */
.bento-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    margin-top: 20px;
}}

.bento-card {{
    background: {theme['card_bg']};
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 32px;
    transition: transform 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}}

.bento-card:hover {{
    transform: translateY(-4px);
    border-color: rgba(167, 139, 250, 0.3);
}}

.icon-wrapper {{
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px;
    margin-bottom: 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
}}

/* Utility text classes */
.tag {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {glow_color}; border: 1px solid {active_color}44;
    border-radius: 20px; padding: 6px 16px; margin-bottom: 24px;
    font-size: 11px; font-weight: 700; color: {active_color};
    letter-spacing: 0.12em; font-family: 'JetBrains Mono', monospace;
}}
</style>
""", unsafe_allow_html=True)

# --- TOP NAVIGATION ---
nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
with nav_col1:
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:12px;padding:8px 0;'>
        <div style='width:36px;height:36px;border-radius:10px;
            background:linear-gradient(135deg,{active_color},#9b59ff);
            display:flex;align-items:center;justify-content:center;
            font-weight:800;font-size:18px;color:#050508;'>A</div>
        <span style='font-size:18px;font-weight:800;letter-spacing:0.05em;'>AURA</span>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        st.button("Log In", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.button("Get Started", use_container_width=True)

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

# --- HERO SECTION ---
hero_left, hero_right = st.columns([1.1, 1], gap="large")

with hero_left:
    st.markdown(f"""
    <div style="padding-top: 40px;">
        <div class="tag">
            <div style='width:6px;height:6px;border-radius:50%;background:{active_color};'></div>
            AI-POWERED PERSONAL ASSISTANT
        </div>
        <h1 style='font-size:clamp(48px, 6vw, 72px); font-weight:800; letter-spacing:-0.03em; line-height:1.1; margin:0 0 24px;'>
            Your AI, <br>
            <span style='color:{active_color};'>perfectly tuned</span><br>
            to you.
        </h1>
        <p style='font-size:18px; color:#9090a8; max-width:500px; line-height:1.6; margin:0 0 40px; font-weight:400;'>
            Plan tasks, set reminders, take notes, and let Aura prioritize what matters most — adapting its personality to match how you work.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 2])
    with btn_col1:
        st.button("Get Started for Free", use_container_width=True)
    with btn_col2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        st.button("▶ Watch Demo", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with hero_right:
    # App Dashboard Mockup built with HTML/CSS
    st.markdown(f"""
    <div class="glass-panel">
        <div style="position:relative; z-index:1;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 30px;">
                <div>
                    <div style="font-size:12px; color:#9090a8; font-family:'JetBrains Mono', monospace;">TODAY's OVERVIEW</div>
                    <div style="font-size:24px; font-weight:700;">Good morning, <span style="color:{active_color}">Commander</span></div>
                </div>
                <div style="width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg, {active_color}, #9b59ff); display:flex; align-items:center; justify-content:center; color:#050508; font-weight:bold;">C</div>
            </div>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:20px;">
                    <div style="font-size:11px; color:#9090a8; margin-bottom:8px; font-family:'JetBrains Mono', monospace;">TASKS ORGANIZED</div>
                    <div style="font-size:32px; font-weight:800; color:{active_color}">35</div>
                </div>
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:20px;">
                    <div style="font-size:11px; color:#9090a8; margin-bottom:8px; font-family:'JetBrains Mono', monospace;">AI STATUS</div>
                    <div style="font-size:24px; font-weight:800; color:#00d68f; margin-top:6px;">ONLINE</div>
                </div>
            </div>

            <div style="background:rgba(0,0,0,0.2); border-radius:16px; padding:16px; border:1px solid rgba(255,255,255,0.03);">
                <div style="font-size:12px; font-weight:600; margin-bottom:12px; display:flex; justify-content:space-between;">
                    <span>Priority Tasks</span>
                    <span style="color:{active_color}">View All</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                    <div style="width:16px; height:16px; border-radius:4px; border:2px solid {active_color};"></div>
                    <span style="font-size:14px;">Review project proposal</span>
                    <span style="margin-left:auto; font-size:11px; background:rgba(255,69,96,0.15); color:#ff4560; padding:2px 8px; border-radius:10px;">HIGH</span>
                </div>
                <div style="display:flex; align-items:center; gap:12px; padding:10px 0;">
                    <div style="width:16px; height:16px; border-radius:4px; border:2px solid #6b6b80;"></div>
                    <span style="font-size:14px; color:#9090a8;">Team stand-up meeting</span>
                    <span style="margin-left:auto; font-size:11px; background:rgba(255,176,32,0.15); color:#ffb020; padding:2px 8px; border-radius:10px;">MED</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# --- BENTO BOX FEATURES ---
st.markdown(f"""
<div style='text-align:center; margin-bottom: 40px;'>
    <h2 style='font-size:36px; font-weight:800; letter-spacing:-0.02em;'>Everything you need to stay on top of your day.</h2>
</div>

<div class="bento-grid">
    <div class="bento-card">
        <div class="icon-wrapper" style="color: {active_color};">📌</div>
        <h3 style="font-size:18px; font-weight:700; margin:0 0 12px;">Task Engine</h3>
        <p style="font-size:14px; color:#9090a8; line-height:1.6; margin:0;">Deploy tasks with priority levels. Track what's pending, done, and what needs attention first.</p>
    </div>
    <div class="bento-card">
        <div class="icon-wrapper" style="color: #9b59ff;">🧠</div>
        <h3 style="font-size:18px; font-weight:700; margin:0 0 12px;">Neural Chat</h3>
        <p style="font-size:14px; color:#9090a8; line-height:1.6; margin:0;">Talk to an AI that knows your tasks, notes, and goals. Switch personalities on the fly.</p>
    </div>
    <div class="bento-card">
        <div class="icon-wrapper" style="color: #00d68f;">📝</div>
        <h3 style="font-size:18px; font-weight:700; margin:0 0 12px;">Quick Notes</h3>
        <p style="font-size:14px; color:#9090a8; line-height:1.6; margin:0;">Capture ideas instantly. Your notes are always searchable and available to your AI.</p>
    </div>
    <div class="bento-card">
        <div class="icon-wrapper" style="color: #ffb020;">⏰</div>
        <h3 style="font-size:18px; font-weight:700; margin:0 0 12px;">Smart Reminders</h3>
        <p style="font-size:14px; color:#9090a8; line-height:1.6; margin:0;">Set reminders and get alerted when they're overdue. Never miss what matters.</p>
    </div>
</div>
""", unsafe_allow_html=True)