"""Premium CSS injection for the ChurnGuard AI dashboard."""
import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Google Font ────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide defaults ─────────────────────────────────── */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ── Main container ────────────────────────────────── */
    .main .block-container {
        padding: 2rem 3rem 3rem 3rem;
        max-width: 1300px;
    }

    /* ── Sidebar ───────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080b1f 0%, #0f1338 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 1.3rem;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* ── Glass Card ─────────────────────────────────────── */
    .glass-card {
        background: linear-gradient(135deg, rgba(17,22,51,0.8), rgba(10,14,39,0.9));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent, #00d4ff), transparent);
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 212, 255, 0.2);
        box-shadow: 0 12px 40px rgba(0, 212, 255, 0.08);
    }
    .glass-card:hover::before { opacity: 1; }

    /* ── Metric Cards ──────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, rgba(17,22,51,0.9), rgba(10,14,39,0.95));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0, 212, 255, 0.1);
        border-color: rgba(0, 212, 255, 0.25);
    }
    .metric-card .metric-icon {
        font-size: 2rem;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 8px rgba(0,212,255,0.3));
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 6px;
        font-weight: 500;
    }
    .metric-card .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* ── Color accent variants ─────────────────────────── */
    .metric-card.blue .metric-value { color: #00d4ff; }
    .metric-card.blue:hover { border-color: rgba(0,212,255,0.3); box-shadow: 0 12px 40px rgba(0,212,255,0.12); }
    .metric-card.purple .metric-value { color: #a78bfa; }
    .metric-card.purple:hover { border-color: rgba(124,58,237,0.3); box-shadow: 0 12px 40px rgba(124,58,237,0.12); }
    .metric-card.green .metric-value { color: #10b981; }
    .metric-card.green:hover { border-color: rgba(16,185,129,0.3); box-shadow: 0 12px 40px rgba(16,185,129,0.12); }
    .metric-card.amber .metric-value { color: #f59e0b; }
    .metric-card.amber:hover { border-color: rgba(245,158,11,0.3); box-shadow: 0 12px 40px rgba(245,158,11,0.12); }
    .metric-card.red .metric-value { color: #ef4444; }
    .metric-card.red:hover { border-color: rgba(239,68,68,0.3); box-shadow: 0 12px 40px rgba(239,68,68,0.12); }

    /* ── Page Header ───────────────────────────────────── */
    .page-header {
        padding: 12px 0 28px 0;
    }
    .page-header h1 {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px !important;
    }
    .page-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }

    /* ── Section Headers ───────────────────────────────── */
    .section-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #e2e8f0;
        padding: 16px 0 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }

    /* ── Risk Badges ───────────────────────────────────── */
    .risk-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .risk-critical { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
    .risk-high { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); }
    .risk-moderate { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
    .risk-low { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }

    /* ── Customer Card ─────────────────────────────────── */
    .customer-card {
        background: linear-gradient(135deg, rgba(17,22,51,0.8), rgba(10,14,39,0.9));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 12px;
    }
    .customer-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0,212,255,0.2);
        box-shadow: 0 8px 32px rgba(0,212,255,0.06);
    }
    .customer-card .avatar {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
        margin-right: 16px;
        flex-shrink: 0;
    }
    .customer-card .card-row {
        display: flex;
        align-items: center;
    }
    .customer-card .card-info h4 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: #e2e8f0;
    }
    .customer-card .card-info p {
        margin: 2px 0 0 0;
        font-size: 0.8rem;
        color: #64748b;
    }
    .sim-score {
        font-size: 1.5rem;
        font-weight: 800;
        color: #00d4ff;
    }

    /* ── Gauge Container ───────────────────────────────── */
    .gauge-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 24px;
    }

    /* ── Strategy Box ──────────────────────────────────── */
    .strategy-box {
        background: linear-gradient(135deg, rgba(0,212,255,0.05), rgba(124,58,237,0.05));
        border: 1px solid rgba(0,212,255,0.15);
        border-radius: 12px;
        padding: 20px;
        margin-top: 12px;
    }
    .strategy-box h4 {
        color: #00d4ff;
        margin: 0 0 8px 0;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .strategy-box p {
        color: #94a3b8;
        margin: 0;
        line-height: 1.6;
        font-size: 0.9rem;
    }

    /* ── Tech Badge ────────────────────────────────────── */
    .tech-badge {
        display: inline-block;
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.2);
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #00d4ff;
        margin: 4px;
        transition: all 0.25s ease;
    }
    .tech-badge:hover {
        background: rgba(0,212,255,0.15);
        transform: translateY(-1px);
    }

    /* ── Timeline ──────────────────────────────────────── */
    .timeline-item {
        position: relative;
        padding-left: 36px;
        padding-bottom: 28px;
        border-left: 2px solid rgba(255,255,255,0.08);
        margin-left: 12px;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -7px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #00d4ff;
        box-shadow: 0 0 12px rgba(0,212,255,0.4);
    }
    .timeline-item h4 {
        margin: 0;
        color: #e2e8f0;
        font-size: 1rem;
        font-weight: 600;
    }
    .timeline-item p {
        margin: 4px 0 0 0;
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ── Divider ───────────────────────────────────────── */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
        margin: 24px 0;
        border: none;
    }

    /* ── Plotly chart overrides ─────────────────────────── */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Dataframe styling ─────────────────────────────── */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Tabs ──────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* ── Selectbox / inputs ────────────────────────────── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: rgba(17,22,51,0.8) !important;
        border-color: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }

    /* ── Buttons ───────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        padding: 0.5rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,212,255,0.25) !important;
    }

    /* ── Download button ───────────────────────────────── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(124,58,237,0.1)) !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        color: #00d4ff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(124,58,237,0.2)) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Spinner ───────────────────────────────────────── */
    .stSpinner > div {
        border-color: #00d4ff transparent transparent !important;
    }

    /* ── Expander ──────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(17,22,51,0.5) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def metric_card(icon, value, label, color="blue", sub=""):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="metric-card {color}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {sub_html}
    </div>"""


def page_header(title, subtitle=""):
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    return f"""
    <div class="page-header">
        <h1>{title}</h1>
        {sub_html}
    </div>"""


def risk_badge(label):
    cls_map = {"Critical Risk": "risk-critical", "High Risk": "risk-high",
               "Moderate Risk": "risk-moderate", "Low Risk": "risk-low"}
    return f'<span class="risk-badge {cls_map.get(label, "risk-low")}">{label}</span>'


def section_header(text):
    return f'<div class="section-header">{text}</div>'


def glow_divider():
    return '<div class="glow-divider"></div>'
