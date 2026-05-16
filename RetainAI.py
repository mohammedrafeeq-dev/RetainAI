"""ChurnGuard AI - Enterprise Customer Intelligence Platform."""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ChurnGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_css, metric_card, page_header, section_header, glow_divider
from utils.data_loader import (load_customer_profiles, load_metrics,
                               load_processed_data, load_class_distribution)
from utils.config import SEGMENT_COLORS, COLORS

inject_css()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🔄 RetainAI")
    st.markdown("""<div style='color:#64748b;font-size:0.8rem;margin:-8px 0 20px 0;'>
    Predictive Retention & Analytics</div>""", unsafe_allow_html=True)
    st.markdown(glow_divider(), unsafe_allow_html=True)
    st.markdown("""<div style='color:#64748b;font-size:0.75rem;padding:8px 0;'>
    <b style='color:#94a3b8;'>Platform Version</b> 1.0.0<br>
    <b style='color:#94a3b8;'>Model</b> XGBoost v2.0<br>
    <b style='color:#94a3b8;'>Status</b> <span style='color:#10b981;'>● Online</span>
    </div>""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────
try:
    profiles = load_customer_profiles()
    metrics = load_metrics()
    data = load_processed_data()
    class_dist = load_class_distribution()

    total = len(profiles)
    churn_rate = profiles['high_risk'].mean()
    high_risk_n = profiles['high_risk'].sum()
    best_auc = metrics['results']['XGBoost']['ROC-AUC']
except Exception as e:
    st.error(f"📡 Data sync in progress... Please refresh in 30 seconds. ({e})")
    st.stop()

# ── Header ───────────────────────────────────────────────────
st.markdown(page_header("Dashboard", "Real-time customer churn analytics overview"), unsafe_allow_html=True)

# ── KPI Row ──────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(metric_card("👥", f"{total:,}", "Total Customers", "blue", "Active database"),
                unsafe_allow_html=True)
with c2:
    st.markdown(metric_card("⚠️", f"{churn_rate:.1%}", "Churn Rate", "red" if churn_rate > 0.3 else "amber",
                            "Predicted at-risk"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_card("🚨", f"{high_risk_n:,}", "High-Risk", "red",
                            f"{high_risk_n/total:.1%} of total"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_card("🎯", f"{best_auc:.1%}", "Model ROC-AUC", "green", "XGBoost best"),
                unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Charts Row ───────────────────────────────────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown(section_header("📊 Risk Segment Distribution"), unsafe_allow_html=True)
    seg_counts = profiles['segment_label'].value_counts()
    order = ['Critical Risk', 'High Risk', 'Moderate Risk', 'Low Risk']
    seg_counts = seg_counts.reindex(order).fillna(0)
    colors = [SEGMENT_COLORS[s] for s in order]

    fig = go.Figure(data=[go.Pie(
        labels=seg_counts.index, values=seg_counts.values,
        hole=0.6, marker=dict(colors=colors, line=dict(width=2, color='#0a0e27')),
        textinfo='label+percent', textfont=dict(size=12, color='#e2e8f0'),
        hoverinfo='label+value+percent',
    )])
    fig.update_layout(
        showlegend=False, paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20,l=20,r=20),
        height=360,
        annotations=[dict(text=f"<b>{total:,}</b><br>Customers",
                          x=0.5, y=0.5, font_size=16, font_color='#94a3b8', showarrow=False)]
    )
    st.plotly_chart(fig, width='stretch')

with col_right:
    st.markdown(section_header("📈 Churn Probability by Segment"), unsafe_allow_html=True)
    fig2 = go.Figure()
    for seg in order:
        seg_data = profiles[profiles['segment_label'] == seg]['churn_probability']
        fig2.add_trace(go.Box(
            y=seg_data, name=seg, marker_color=SEGMENT_COLORS[seg],
            boxmean='sd', line=dict(width=1.5),
        ))
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20,b=20,l=40,r=20), height=360, showlegend=False,
        yaxis=dict(title="Churn Probability", gridcolor='rgba(255,255,255,0.04)',
                   zerolinecolor='rgba(255,255,255,0.06)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
        font=dict(color='#94a3b8'),
    )
    st.plotly_chart(fig2, width='stretch')

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── High Risk Table ──────────────────────────────────────────
st.markdown(section_header("🚨 Top High-Risk Customers"), unsafe_allow_html=True)

high_risk = profiles[profiles['high_risk'] == 1].nlargest(10, 'churn_probability')
display_cols = ['churn_probability', 'segment_label']
# Add original data columns if available
for col in ['age', 'gender', 'total_spent', 'satisfaction_score']:
    if col in data.columns:
        high_risk[col] = data.loc[high_risk.index, col].values
        display_cols.append(col)

display_df = high_risk[display_cols].copy()
display_df['churn_probability'] = display_df['churn_probability'].apply(lambda x: f"{x:.1%}")
display_df.columns = [c.replace('_', ' ').title() for c in display_df.columns]
display_df.index = [f"Customer #{i}" for i in display_df.index]

st.dataframe(display_df, width='stretch', height=400)

# ── Download ─────────────────────────────────────────────────
csv = profiles[profiles['high_risk']==1].to_csv(index=False)
st.download_button("📥 Export High-Risk Customers (CSV)", csv,
                   "high_risk_customers.csv", "text/csv")
