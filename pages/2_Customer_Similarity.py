"""Customer Similarity - Find similar customers and generate retention recommendations."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Customer Similarity | RetainAI", page_icon="🤝", layout="wide")

from utils.styles import (inject_css, page_header, section_header, glow_divider,
                          metric_card, risk_badge)
from utils.data_loader import (load_customer_profiles, load_processed_data,
                               get_similar_customers)
from utils.config import SEGMENT_COLORS, RETENTION_STRATEGIES

inject_css()
st.markdown(page_header("Customer Similarity Engine",
    "Find behaviourally similar customers and generate retention recommendations"),
    unsafe_allow_html=True)

# ── Load ─────────────────────────────────────────────────────
profiles = load_customer_profiles()
raw_data = load_processed_data()
total = len(profiles)

# ── Customer Selector ────────────────────────────────────────
st.markdown(section_header("🔎 Select Customer"), unsafe_allow_html=True)

col_sel, col_n = st.columns([3, 1])
with col_sel:
    cust_id = st.number_input("Customer Index", min_value=0, max_value=total-1,
                              value=0, step=1, help="Enter a customer index (0 to {:,})".format(total-1))
with col_n:
    top_n = st.slider("Similar Customers", 3, 10, 5)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Customer Profile ─────────────────────────────────────────
cust = profiles.iloc[cust_id]
cust_raw = raw_data.iloc[cust_id] if cust_id < len(raw_data) else None

prob = cust['churn_probability']
seg = cust.get('segment_label', 'Unknown')
seg_color = SEGMENT_COLORS.get(seg, '#64748b')

st.markdown(section_header("👤 Customer Profile"), unsafe_allow_html=True)

# Profile cards
pc1, pc2, pc3, pc4 = st.columns(4)
with pc1:
    st.markdown(metric_card("🆔", f"#{cust_id}", "Customer ID", "blue"), unsafe_allow_html=True)
with pc2:
    color = "red" if prob >= 0.5 else "amber" if prob >= 0.3 else "green"
    st.markdown(metric_card("⚡", f"{prob:.1%}", "Churn Risk", color), unsafe_allow_html=True)
with pc3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🏷️</div>
        <div style="margin-top:8px;">{risk_badge(seg)}</div>
        <div class="metric-label" style="margin-top:10px;">Risk Segment</div>
    </div>""", unsafe_allow_html=True)
with pc4:
    if cust_raw is not None and 'total_spent' in cust_raw.index:
        st.markdown(metric_card("💰", f"${cust_raw['total_spent']:,.0f}",
                                "Total Spent", "purple"), unsafe_allow_html=True)
    else:
        st.markdown(metric_card("📊", "N/A", "Total Spent", "purple"), unsafe_allow_html=True)

# Show more details in expander
if cust_raw is not None:
    with st.expander("📋 Full Customer Details"):
        detail_cols = st.columns(4)
        items = [(k, v) for k, v in cust_raw.items() if k != 'churn']
        for i, (k, v) in enumerate(items):
            with detail_cols[i % 4]:
                label = k.replace('_', ' ').title()
                val = f"{v:.2f}" if isinstance(v, float) else str(v)
                st.markdown(f"**{label}:** {val}")

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Similar Customers ────────────────────────────────────────
st.markdown(section_header(f"🤝 Top {top_n} Similar Customers"), unsafe_allow_html=True)

with st.spinner("Computing similarity scores..."):
    similar_df = get_similar_customers(cust_id, top_n)

# Render customer cards
for _, row in similar_df.iterrows():
    idx = int(row['customer_index'])
    sim_score = row['similarity_score']
    sim_cust = profiles.iloc[idx]
    sim_raw = raw_data.iloc[idx] if idx < len(raw_data) else None

    sim_prob = sim_cust['churn_probability']
    sim_seg = sim_cust.get('segment_label', 'Unknown')
    sim_seg_color = SEGMENT_COLORS.get(sim_seg, '#64748b')

    gender_icon = "👨" if (sim_raw is not None and sim_raw.get('gender') == 'Male') else "👩"
    age_str = f", Age {int(sim_raw['age'])}" if (sim_raw is not None and 'age' in sim_raw.index) else ""
    spent_str = f"${sim_raw['total_spent']:,.0f}" if (sim_raw is not None and 'total_spent' in sim_raw.index) else "N/A"

    st.markdown(f"""
    <div class="customer-card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div class="card-row">
                <div class="avatar" style="background:linear-gradient(135deg,{sim_seg_color}80,{sim_seg_color}40);">
                    {gender_icon}
                </div>
                <div class="card-info">
                    <h4>Customer #{idx}{age_str}</h4>
                    <p>Spent: {spent_str} &nbsp;|&nbsp; Risk: {sim_prob:.1%} &nbsp;|&nbsp;
                       {risk_badge(sim_seg)}</p>
                </div>
            </div>
            <div style="text-align:right;">
                <div class="sim-score">{sim_score:.1%}</div>
                <div style="color:#64748b;font-size:0.75rem;">Similarity</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Similarity Chart ─────────────────────────────────────────
st.markdown(section_header("📊 Similarity Scores"), unsafe_allow_html=True)

fig = go.Figure(go.Bar(
    x=[f"#{int(r['customer_index'])}" for _, r in similar_df.iterrows()],
    y=similar_df['similarity_score'],
    marker=dict(
        color=similar_df['similarity_score'],
        colorscale=[[0, '#1e3a5f'], [0.5, '#00d4ff'], [1, '#7c3aed']],
        line=dict(width=0),
    ),
    text=[f"{s:.1%}" for s in similar_df['similarity_score']],
    textposition='outside',
    textfont=dict(color='#94a3b8', size=12),
))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=30, b=40, l=40, r=20), height=320,
    xaxis=dict(title="Customer", gridcolor='rgba(255,255,255,0.04)'),
    yaxis=dict(title="Cosine Similarity", gridcolor='rgba(255,255,255,0.04)',
               range=[0, 1.05], zerolinecolor='rgba(255,255,255,0.06)'),
    font=dict(color='#94a3b8'),
)
st.plotly_chart(fig, width='stretch')

# ── Retention Strategy ───────────────────────────────────────
strategy = RETENTION_STRATEGIES.get(seg, "No specific strategy available.")
st.markdown(f"""
<div class="strategy-box">
    <h4>💡 Recommended Strategy for {seg} Customers</h4>
    <p>{strategy}</p>
</div>
""", unsafe_allow_html=True)

# Export
export_data = similar_df.copy()
export_data['target_customer'] = cust_id
csv = export_data.to_csv(index=False)
st.download_button("📥 Export Similarity Report", csv,
                   f"similarity_customer_{cust_id}.csv", "text/csv")
