"""Churn Predictor - Real-time churn prediction for individual customers."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Churn Predictor | RetainAI", page_icon="🔮", layout="wide")

from utils.styles import inject_css, metric_card, page_header, section_header, glow_divider, risk_badge
from utils.data_loader import load_data_info, predict_single, load_model, load_feature_names
from utils.config import COLORS, RETENTION_STRATEGIES

inject_css()
st.markdown(page_header("Churn Predictor",
    "Input customer features to get a real-time churn risk assessment"), unsafe_allow_html=True)

# ── Load feature info ────────────────────────────────────────
data_info = load_data_info()

# ── Input Form ───────────────────────────────────────────────
st.markdown(section_header("🔧 Customer Features"), unsafe_allow_html=True)

input_vals = {}

# Organize fields into columns
col1, col2, col3 = st.columns(3)

field_layout = {
    col1: ['gender', 'age', 'city', 'device_type', 'subscription_type', 'refund_requested'],
    col2: ['total_spent', 'total_visits', 'avg_session_time', 'pages_per_visit',
           'cart_abandonment_rate', 'support_tickets'],
    col3: ['delivery_delay_days', 'satisfaction_score', 'nps_score',
           'marketing_spend_per_user', 'last_3_month_purchase_freq'],
}

for col, fields in field_layout.items():
    with col:
        for field in fields:
            if field not in data_info:
                continue
            info = data_info[field]
            label = field.replace('_', ' ').title()
            if info['type'] == 'categorical':
                input_vals[field] = st.selectbox(label, info['values'], key=field)
            else:
                mn, mx = info['min'], info['max']
                default = info['median']
                if field in ('refund_requested',):
                    input_vals[field] = st.selectbox(label, [0, 1], key=field)
                elif field in ('support_tickets', 'delivery_delay_days', 'nps_score',
                               'last_3_month_purchase_freq'):
                    input_vals[field] = st.number_input(label, min_value=int(mn),
                        max_value=int(mx)+5, value=int(default), key=field)
                else:
                    input_vals[field] = st.slider(label, float(mn), float(mx),
                        float(default), key=field)

# Derived features
if 'total_spent' in input_vals and 'total_visits' in input_vals:
    input_vals['spend_per_visit'] = input_vals['total_spent'] / (input_vals['total_visits'] + 1e-6)
if 'avg_session_time' in input_vals and 'total_visits' in input_vals:
    input_vals['total_time_spent'] = input_vals['avg_session_time'] * input_vals['total_visits']

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Predict ──────────────────────────────────────────────────
if st.button("🔮 Predict Churn Risk", width='stretch'):
    with st.spinner("Analyzing customer profile..."):
        prob, pred, scaled = predict_single(input_vals)

    # Determine risk level
    if prob >= 0.75:
        risk_label = "Critical Risk"
        risk_color = COLORS['critical']
    elif prob >= 0.5:
        risk_label = "High Risk"
        risk_color = COLORS['high']
    elif prob >= 0.3:
        risk_label = "Moderate Risk"
        risk_color = COLORS['moderate']
    else:
        risk_label = "Low Risk"
        risk_color = COLORS['low']

    # ── Results ──────────────────────────────────────────
    st.markdown(section_header("📋 Prediction Results"), unsafe_allow_html=True)

    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={'suffix': '%', 'font': {'size': 48, 'color': '#e2e8f0'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#64748b',
                         'tickfont': {'color': '#64748b'}},
                'bar': {'color': risk_color, 'thickness': 0.3},
                'bgcolor': 'rgba(255,255,255,0.03)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(16,185,129,0.08)'},
                    {'range': [30, 50], 'color': 'rgba(245,158,11,0.08)'},
                    {'range': [50, 75], 'color': 'rgba(249,115,22,0.08)'},
                    {'range': [75, 100], 'color': 'rgba(239,68,68,0.08)'},
                ],
                'threshold': {
                    'line': {'color': risk_color, 'width': 3},
                    'thickness': 0.8, 'value': prob * 100
                }
            },
            title={'text': "Churn Probability", 'font': {'color': '#94a3b8', 'size': 16}},
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', height=300,
            margin=dict(t=60, b=20, l=40, r=40),
            font=dict(color='#e2e8f0'),
        )
        st.plotly_chart(fig, width='stretch')

    with res_col2:
        # Risk assessment card
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;padding:32px;">
            <div style="font-size:3rem;margin-bottom:12px;">
                {'🔴' if prob >= 0.5 else '🟡' if prob >= 0.3 else '🟢'}
            </div>
            <div style="margin-bottom:12px;">{risk_badge(risk_label)}</div>
            <div style="font-size:0.9rem;color:#94a3b8;margin-top:16px;line-height:1.6;">
                This customer has a <b style="color:{risk_color}">{prob:.1%}</b> probability
                of churning. {'Immediate intervention recommended.' if prob >= 0.5
                else 'Monitor and engage proactively.' if prob >= 0.3
                else 'Customer appears healthy.'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Strategy recommendation
    strategy = RETENTION_STRATEGIES.get(risk_label, "")
    if strategy:
        st.markdown(f"""
        <div class="strategy-box">
            <h4>💡 Recommended Retention Strategy</h4>
            <p>{strategy}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(glow_divider(), unsafe_allow_html=True)

    # Feature importance
    st.markdown(section_header("🔍 Key Risk Factors"), unsafe_allow_html=True)
    model = load_model("XGBoost")
    feat_names = load_feature_names()

    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        top_idx = np.argsort(importances)[-12:]
        top_names = [feat_names[i].replace('_', ' ').title() for i in top_idx]
        top_vals = importances[top_idx]

        fig3 = go.Figure(go.Bar(
            x=top_vals, y=top_names, orientation='h',
            marker=dict(
                color=top_vals,
                colorscale=[[0, '#1e3a5f'], [0.5, '#00d4ff'], [1, '#7c3aed']],
                line=dict(width=0),
            ),
        ))
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=20, l=140, r=20), height=380,
            xaxis=dict(title="Importance", gridcolor='rgba(255,255,255,0.04)',
                       zerolinecolor='rgba(255,255,255,0.06)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
            font=dict(color='#94a3b8', size=12),
        )
        st.plotly_chart(fig3, width='stretch')

    # Download report
    report = pd.DataFrame([{
        'Churn Probability': f"{prob:.4f}",
        'Risk Level': risk_label,
        'Prediction': 'Will Churn' if pred else 'Will Stay',
        'Strategy': strategy,
        **{k.replace('_',' ').title(): v for k,v in input_vals.items()
           if k not in ('spend_per_visit','total_time_spent')}
    }])
    csv = report.to_csv(index=False)
    st.download_button("📥 Download Prediction Report", csv,
                       "churn_prediction_report.csv", "text/csv")
