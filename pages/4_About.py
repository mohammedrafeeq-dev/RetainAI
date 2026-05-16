"""About - Project overview and developer portfolio page."""
import streamlit as st

st.set_page_config(page_title="About | RetainAI", page_icon="ℹ️", layout="wide")

from utils.styles import inject_css, page_header, section_header, glow_divider

inject_css()
st.markdown(page_header("About RetainAI",
    "An advanced customer retention platform built with Applied Machine Learning"),
    unsafe_allow_html=True)

# ── Project Overview ─────────────────────────────────────────
st.markdown(section_header("🎯 Project Overview"), unsafe_allow_html=True)
st.markdown("""
<div class="glass-card">
    <p style="color:#94a3b8;line-height:1.8;font-size:0.95rem;">
    <b style="color:#00d4ff;">RetainAI</b> is an end-to-end Applied Machine Learning project
    that predicts customer churn and generates personalised retention strategies.
    The platform combines predictive modelling, customer segmentation, and similarity-based
    recommendations to help businesses reduce churn and maximise customer lifetime value.
    </p>
    <div style="display:flex;gap:16px;margin-top:16px;flex-wrap:wrap;">
        <div style="flex:1;min-width:200px;background:rgba(0,212,255,0.05);border-radius:10px;padding:16px;border:1px solid rgba(0,212,255,0.1);">
            <div style="font-size:1.5rem;">🎯</div>
            <div style="color:#e2e8f0;font-weight:600;margin-top:6px;">Predict</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">Identify at-risk customers before they leave</div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(124,58,237,0.05);border-radius:10px;padding:16px;border:1px solid rgba(124,58,237,0.1);">
            <div style="font-size:1.5rem;">🔍</div>
            <div style="color:#e2e8f0;font-weight:600;margin-top:6px;">Segment</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">Group customers into actionable risk tiers</div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(16,185,129,0.05);border-radius:10px;padding:16px;border:1px solid rgba(16,185,129,0.1);">
            <div style="font-size:1.5rem;">💡</div>
            <div style="color:#e2e8f0;font-weight:600;margin-top:6px;">Recommend</div>
            <div style="color:#64748b;font-size:0.8rem;margin-top:4px;">Generate personalised retention strategies</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── ML Pipeline ──────────────────────────────────────────────
st.markdown(section_header("🔧 ML Pipeline Architecture"), unsafe_allow_html=True)

steps = [
    ("📥 Data Ingestion", "Load raw customer dataset with 30 features covering demographics, behaviour, and engagement"),
    ("🧹 Preprocessing", "Handle missing values (mode/median imputation), flag unrealistic ages, clean categorical labels"),
    ("⚙️ Feature Engineering", "Create derived features: spend_per_visit, total_time_spent to capture engagement patterns"),
    ("📊 Exploratory Analysis", "Distribution analysis, correlation heatmap, class imbalance assessment (85/15 split)"),
    ("🔧 Outlier Treatment", "IQR-based detection and capping for all numerical features"),
    ("🔄 Encoding & Scaling", "One-Hot Encoding for categoricals, StandardScaler for normalisation"),
    ("⚖️ Imbalance Handling", "SMOTE oversampling on training data only to prevent data leakage"),
    ("🤖 Model Training", "Train Logistic Regression, Random Forest, and XGBoost with class-weight balancing"),
    ("📈 Model Selection", "Combined Score + Stability Gap framework with 5-Fold Stratified Cross-Validation"),
    ("🎛️ Hyperparameter Tuning", "GridSearchCV on XGBoost for optimal learning_rate, max_depth, scale_pos_weight"),
    ("🤝 Recommendation Engine", "Cosine similarity + K-Means clustering (k=4) for segment-based retention strategies"),
]

timeline_html = ""
for title, desc in steps:
    timeline_html += f"""
    <div class="timeline-item">
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>"""

st.markdown(f'<div style="margin-top:8px;">{timeline_html}</div>', unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Tech Stack ───────────────────────────────────────────────
st.markdown(section_header("🛠️ Technology Stack"), unsafe_allow_html=True)

techs = {
    "Core": ["Python 3.10+", "NumPy", "Pandas"],
    "ML": ["scikit-learn", "XGBoost", "imbalanced-learn"],
    "Visualization": ["Plotly", "Matplotlib", "Seaborn"],
    "Dashboard": ["Streamlit", "Custom CSS"],
    "Techniques": ["SMOTE", "GridSearchCV", "K-Means", "Cosine Similarity"],
}

cols = st.columns(len(techs))
for col, (category, items) in zip(cols, techs.items()):
    with col:
        badges = ''.join(f'<span class="tech-badge">{item}</span>' for item in items)
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;min-height:180px;">
            <div style="color:#94a3b8;font-size:0.75rem;text-transform:uppercase;
                        letter-spacing:1.5px;margin-bottom:12px;font-weight:600;">{category}</div>
            {badges}
        </div>""", unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Dataset ──────────────────────────────────────────────────
st.markdown(section_header("📊 Dataset Description"), unsafe_allow_html=True)

col_d1, col_d2 = st.columns([1, 1])
with col_d1:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#e2e8f0;margin-top:0;">Sales & Marketing Customer Dataset</h4>
        <table style="width:100%;margin-top:12px;">
            <tr><td style="color:#64748b;padding:6px 0;">Records</td>
                <td style="color:#e2e8f0;font-weight:600;">~10,000 customers</td></tr>
            <tr><td style="color:#64748b;padding:6px 0;">Features</td>
                <td style="color:#e2e8f0;font-weight:600;">30 columns</td></tr>
            <tr><td style="color:#64748b;padding:6px 0;">Target</td>
                <td style="color:#e2e8f0;font-weight:600;">Binary (churn: 0/1)</td></tr>
            <tr><td style="color:#64748b;padding:6px 0;">Class Split</td>
                <td style="color:#f59e0b;font-weight:600;">~85% / 15% (imbalanced)</td></tr>
        </table>
    </div>""", unsafe_allow_html=True)

with col_d2:
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#e2e8f0;margin-top:0;">Feature Categories</h4>
        <div style="margin-top:12px;">
            <div style="padding:6px 0;"><span style="color:#00d4ff;">●</span>
                <span style="color:#94a3b8;"> Demographics:</span>
                <span style="color:#e2e8f0;"> gender, age, city</span></div>
            <div style="padding:6px 0;"><span style="color:#7c3aed;">●</span>
                <span style="color:#94a3b8;"> Behaviour:</span>
                <span style="color:#e2e8f0;"> total_spent, visits, session_time</span></div>
            <div style="padding:6px 0;"><span style="color:#10b981;">●</span>
                <span style="color:#94a3b8;"> Engagement:</span>
                <span style="color:#e2e8f0;"> pages_per_visit, cart_abandonment</span></div>
            <div style="padding:6px 0;"><span style="color:#f59e0b;">●</span>
                <span style="color:#94a3b8;"> Satisfaction:</span>
                <span style="color:#e2e8f0;"> NPS, support_tickets, refunds</span></div>
            <div style="padding:6px 0;"><span style="color:#ef4444;">●</span>
                <span style="color:#94a3b8;"> Financial:</span>
                <span style="color:#e2e8f0;"> marketing_spend, delivery_delays</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Business Value ───────────────────────────────────────────
st.markdown(section_header("💼 Business Value"), unsafe_allow_html=True)

v1, v2, v3 = st.columns(3)
with v1:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2.5rem;">5-7×</div>
        <div style="color:#00d4ff;font-weight:600;margin-top:4px;">Cost Reduction</div>
        <div style="color:#64748b;font-size:0.8rem;margin-top:8px;">
        Retaining a customer costs 5-7× less than acquiring a new one</div>
    </div>""", unsafe_allow_html=True)
with v2:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2.5rem;">82%</div>
        <div style="color:#10b981;font-weight:600;margin-top:4px;">Churn Detection</div>
        <div style="color:#64748b;font-size:0.8rem;margin-top:8px;">
        Our model catches 82% of churning customers before they leave</div>
    </div>""", unsafe_allow_html=True)
with v3:
    st.markdown("""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size:2.5rem;">4</div>
        <div style="color:#7c3aed;font-weight:600;margin-top:4px;">Risk Segments</div>
        <div style="color:#64748b;font-size:0.8rem;margin-top:8px;">
        Actionable tiers with personalised retention strategies</div>
    </div>""", unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 16px 0;">
    <div style="font-size:0.8rem;color:#64748b;">
        Built with ❤️ as an Applied Machine Learning project
    </div>
    <div style="font-size:0.75rem;color:#475569;margin-top:4px;">
        RetainAI v1.0.0 — Powered by XGBoost, scikit-learn & Streamlit
    </div>
</div>
""", unsafe_allow_html=True)
