import streamlit as st

st.set_page_config(page_title="AURA — Your Personal AI Sanctuary", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp, .stMarkdown, p, div, span, h1, h2, h3, label {
    font-family: 'Inter', sans-serif !important;
}
.stApp { background: #15121b !important; color: #e8dfed !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}
.stButton > button {
    background: linear-gradient(to right, #7830db, #aa74ff) !important;
    color: #ffffff !important;
    border: none !important;
    padding: 14px 32px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    border-radius: 9999px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(214,186,255,0.4) !important;
    width: auto !important;
}
.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 30px rgba(214,186,255,0.6) !important;
    color: #ffffff !important;
}

/* ambient background */
.bg-ambient {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 0;
    background:
        radial-gradient(circle at 15% 50%, rgba(66,0,138,0.15) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(201,129,26,0.1) 0%, transparent 50%);
}
.ambient-orb-tl {
    position: fixed; top: -10%; left: -10%;
    width: 40%; height: 40%; border-radius: 50%;
    background: rgba(214,186,255,0.1); filter: blur(120px);
    pointer-events: none; z-index: 0;
}
.ambient-orb-br {
    position: fixed; bottom: -10%; right: -10%;
    width: 30%; height: 30%; border-radius: 50%;
    background: rgba(255,184,101,0.1); filter: blur(100px);
    pointer-events: none; z-index: 0;
}

/* navbar */
.aura-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 40px;
    background: rgba(21,18,27,0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    position: sticky; top: 0; z-index: 100;
}
.aura-nav-logo {
    font-size: 24px; font-weight: 700;
    background: linear-gradient(to right, #d6baff, #c9811a);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 15px rgba(214,186,255,0.5));
}
.aura-nav-links { display: flex; gap: 32px; }
.aura-nav-link {
    font-size: 14px; color: #cdc2d7;
    text-decoration: none; transition: color 0.2s;
}
.aura-nav-link:hover { color: #d6baff; }

/* hero */
.hero-section {
    min-height: 870px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
    padding: 96px 40px 64px;
    position: relative; z-index: 1;
}
.hero-title {
    font-size: clamp(36px, 6vw, 56px);
    font-weight: 700; letter-spacing: -0.02em;
    line-height: 1.1; color: #e8dfed;
    max-width: 900px; margin: 0 auto 24px;
}
.hero-title-gradient {
    background: linear-gradient(to right, #d6baff, #aa74ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 18px; color: #cdc2d7;
    max-width: 640px; margin: 0 auto 48px;
    line-height: 1.6;
}
.hero-mockup-wrap {
    margin-top: 96px; width: 100%; max-width: 900px;
    margin-left: auto; margin-right: auto;
    position: relative;
}
.hero-mockup-wrap::before {
    content: ''; position: absolute; inset: 0;
    background: rgba(214,186,255,0.2); filter: blur(100px);
    border-radius: 24px; transition: all 0.7s ease;
}
.hero-mockup-wrap:hover::before {
    background: rgba(214,186,255,0.3);
}
.hero-mockup-inner {
    position: relative;
    background: rgba(18,18,22,0.7);
    backdrop-filter: blur(32px);
    border: 1px solid rgba(255,255,255,0.1);
    border-top: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px; padding: 8px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.hero-mockup-screen {
    width: 100%; border-radius: 10px;
    background: linear-gradient(135deg, #1e1a23 0%, #15121b 50%, #221e28 100%);
    height: 420px; display: flex; align-items: center; justify-content: center;
    border: 1px solid rgba(255,255,255,0.05);
    position: relative; overflow: hidden;
}
.mockup-kpi {
    position: absolute; background: #100c16;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px; padding: 16px 20px;
}
.mockup-label {
    font-size: 9px; color: #968da0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em; margin-bottom: 6px;
}
.mockup-value { font-size: 22px; font-weight: 700; }

/* features section */
.features-section {
    padding: 96px 40px;
    background: rgba(16,12,22,0.5);
    border-top: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: relative; z-index: 1;
}
.features-inner { max-width: 1200px; margin: 0 auto; }
.section-eyebrow {
    font-size: 12px; font-weight: 500;
    letter-spacing: 0.1em; color: #968da0;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase; margin-bottom: 12px;
    text-align: center;
}
.section-headline {
    font-size: clamp(24px, 3vw, 32px);
    font-weight: 600; color: #e8dfed;
    text-align: center; margin-bottom: 16px;
}
.section-sub {
    font-size: 16px; color: #cdc2d7;
    text-align: center; margin-bottom: 64px;
}
.feat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
}
.feat-card {
    background: rgba(18,18,22,0.7);
    backdrop-filter: blur(32px);
    border: 1px solid rgba(255,255,255,0.1);
    border-top: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px; padding: 32px;
    transition: background 0.3s ease;
    cursor: default;
    display: flex; flex-direction: column;
    align-items: flex-start; gap: 16px;
}
.feat-card:hover {
    background: rgba(30,26,35,0.7);
}
.feat-icon-wrap {
    width: 48px; height: 48px; border-radius: 12px;
    background: rgba(214,186,255,0.1);
    display: flex; align-items: center; justify-content: center;
}
.feat-icon-wrap .material-symbols-outlined {
    font-size: 28px; color: #d6baff;
}
.feat-title { font-size: 20px; font-weight: 600; color: #e8dfed; }
.feat-desc { font-size: 14px; color: #cdc2d7; line-height: 1.6; }

/* social proof */
.proof-section {
    padding: 80px 40px;
    text-align: center;
    position: relative; z-index: 1;
}
.proof-badge {
    display: inline-flex; align-items: center; gap: 12px;
    background: rgba(18,18,22,0.7);
    backdrop-filter: blur(32px);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 12px 24px; border-radius: 9999px;
    margin-bottom: 32px;
}
.proof-badge .material-symbols-outlined { color: #d6baff; font-size: 20px; }
.proof-badge-text {
    font-size: 12px; font-weight: 500;
    letter-spacing: 0.1em; color: #e8dfed;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
}
.proof-stars { display: flex; justify-content: center; gap: 4px; margin-bottom: 16px; }
.proof-stars .material-symbols-outlined { color: #ffb865; font-size: 22px; }
.proof-quote {
    font-size: 16px; color: #cdc2d7;
    max-width: 480px; margin: 0 auto;
    font-style: italic; line-height: 1.6;
}

/* footer */
.aura-footer {
    background: #100c16;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding: 48px 40px;
    display: flex; justify-content: space-between; align-items: center;
    flex-wrap: wrap; gap: 24px;
    position: relative; z-index: 1;
}
.footer-logo {
    font-size: 13px; font-weight: 700;
    letter-spacing: 0.1em; color: #d6baff;
    font-family: 'JetBrains Mono', monospace;
}
.footer-copy { font-size: 14px; color: #cdc2d7; }
.footer-links { display: flex; gap: 24px; }
.footer-link {
    font-size: 14px; color: #cdc2d7;
    text-decoration: none; opacity: 0.8;
    transition: color 0.2s, opacity 0.2s;
}
.footer-link:hover { color: #d6baff; opacity: 1; }

@media (max-width: 900px) {
    .feat-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .aura-nav-links { display: none !important; }
}
@media (max-width: 600px) {
    .feat-grid { grid-template-columns: 1fr !important; }
    .hero-section { padding: 80px 20px 40px; }
    .aura-footer { flex-direction: column; align-items: flex-start; }
}
</style>
""", unsafe_allow_html=True)

# ── AMBIENT ──
st.markdown("""
<div class="ambient-orb-tl"></div>
<div class="ambient-orb-br"></div>
""", unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="aura-nav">
    <div class="aura-nav-logo">AURA</div>
    <div class="aura-nav-links">
        <a class="aura-nav-link" href="#">Features</a>
        <a class="aura-nav-link" href="#">How It Works</a>
        <a class="aura-nav-link" href="#">Personalities</a>
        <a class="aura-nav-link" href="#">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">
        Your Personal<br>
        <span class="hero-title-gradient">AI Sanctuary</span>
    </h1>
    <p class="hero-sub">
        A high-performance digital environment designed for ultimate focus and silent efficiency.
        Experience the future of personal intelligence.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([3, 1.2, 3])
with c2:
    if st.button("Get Started →", key="cta_main"):
        st.switch_page("app.py")

# Hero mockup
st.markdown("""
<div style="padding: 0 40px 40px; position: relative; z-index: 1;">
<div class="hero-mockup-wrap">
    <div class="hero-mockup-inner">
        <div class="hero-mockup-screen">
            <!-- Glow orb -->
            <div style="position:absolute;width:300px;height:300px;border-radius:50%;
                background:rgba(120,48,219,0.2);filter:blur(80px);top:50%;left:50%;
                transform:translate(-50%,-50%);pointer-events:none;"></div>
            <!-- AURA orb -->
            <div style="width:160px;height:160px;border-radius:50%;
                background:radial-gradient(circle at 35% 35%, #c4b5fd, #7c3aed 50%, #4c1d95);
                display:flex;align-items:center;justify-content:center;
                box-shadow:0 0 60px rgba(214,186,255,0.3);position:relative;z-index:2;">
                <span style="font-size:56px;color:rgba(255,255,255,0.9);">✦</span>
            </div>
            <!-- KPI cards -->
            <div class="mockup-kpi" style="top:40px;right:40px;">
                <div class="mockup-label">TASKS PENDING</div>
                <div class="mockup-value" style="color:#d6baff;">8</div>
            </div>
            <div class="mockup-kpi" style="bottom:60px;left:40px;">
                <div class="mockup-label">AI STATUS</div>
                <div class="mockup-value" style="color:#00d68f;font-size:16px;">ONLINE</div>
            </div>
            <div class="mockup-kpi" style="top:120px;left:40px;">
                <div class="mockup-label">OVERDUE</div>
                <div class="mockup-value" style="color:#ffb865;">2</div>
            </div>
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# ── FEATURES SECTION ──
st.markdown("""
<div class="features-section">
<div class="features-inner">
    <div class="section-eyebrow">Engineered for Excellence</div>
    <h2 class="section-headline">Everything you need, nothing you don't</h2>
    <p class="section-sub">Intelligent features wrapped in a seamless, distraction-free interface.</p>
    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon-wrap">
                <span class="material-symbols-outlined">face</span>
            </div>
            <div class="feat-title">Face ID Login</div>
            <p class="feat-desc">Frictionless, secure access powered by advanced biometric recognition. Your sanctuary opens only for you.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap">
                <span class="material-symbols-outlined">task_alt</span>
            </div>
            <div class="feat-title">Smart Task Management</div>
            <p class="feat-desc">AI-driven prioritization organizes your workload silently, ensuring you focus on what truly matters.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap">
                <span class="material-symbols-outlined">psychology</span>
            </div>
            <div class="feat-title">Dynamic AI Personalities</div>
            <p class="feat-desc">Adapt your assistant's tone and analytical depth to match your current workflow and cognitive needs.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon-wrap">
                <span class="material-symbols-outlined">picture_as_pdf</span>
            </div>
            <div class="feat-title">Instant Export (PDF/CSV)</div>
            <p class="feat-desc">Transform complex insights into presentation-ready documents with a single click. Seamless integration.</p>
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# ── SOCIAL PROOF ──
st.markdown("""
<div class="proof-section">
    <div class="proof-badge">
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">verified</span>
        <span class="proof-badge-text">Trusted by 50,000+ power users</span>
    </div>
    <div class="proof-stars">
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">star</span>
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">star</span>
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">star</span>
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">star</span>
        <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">star</span>
    </div>
    <p class="proof-quote">
        "AURA hasn't just improved my productivity; it has fundamentally elevated the aesthetic of my digital life."
    </p>
</div>
""", unsafe_allow_html=True)

# Bottom CTA
c1, c2, c3 = st.columns([3, 1.2, 3])
with c2:
    if st.button("Launch AURA →", key="cta_bottom"):
        st.switch_page("app.py")

# ── FOOTER ──
st.markdown("""
<div class="aura-footer">
    <div class="footer-logo">AURA</div>
    <div class="footer-copy">© 2024 AURA AI Digital Sanctuary.</div>
    <div class="footer-links">
        <a class="footer-link" href="#">Privacy Policy</a>
        <a class="footer-link" href="#">Terms of Service</a>
        <a class="footer-link" href="#">API Documentation</a>
        <a class="footer-link" href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
