"""Model Performance - Professional ML evaluation dashboard."""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(page_title="Model Performance | RetainAI", page_icon="📊", layout="wide")

from utils.styles import inject_css, page_header, section_header, glow_divider, metric_card
from utils.data_loader import load_metrics
from utils.config import MODEL_COLORS, MODEL_NAMES

inject_css()
st.markdown(page_header("Model Performance",
    "Comprehensive ML evaluation and model comparison dashboard"), unsafe_allow_html=True)

metrics = load_metrics()
results = metrics['results']
cm_data = metrics['confusion_matrices']
roc_data = metrics['roc_data']
cv_data = metrics['cv_results']

# ── Best Model KPIs ──────────────────────────────────────────
st.markdown(section_header("🏆 Best Model — XGBoost"), unsafe_allow_html=True)
xgb = results['XGBoost']
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(metric_card("🎯", f"{xgb['Accuracy']:.1%}", "Accuracy", "blue"), unsafe_allow_html=True)
with c2:
    st.markdown(metric_card("🔬", f"{xgb['Precision']:.1%}", "Precision", "purple"), unsafe_allow_html=True)
with c3:
    st.markdown(metric_card("📡", f"{xgb['Recall']:.1%}", "Recall", "green"), unsafe_allow_html=True)
with c4:
    st.markdown(metric_card("⚖️", f"{xgb['F1 Score']:.1%}", "F1 Score", "amber"), unsafe_allow_html=True)
with c5:
    st.markdown(metric_card("📈", f"{xgb['ROC-AUC']:.1%}", "ROC-AUC", "blue"), unsafe_allow_html=True)

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── ROC Curves ───────────────────────────────────────────────
col_roc, col_cm = st.columns([1, 1])

with col_roc:
    st.markdown(section_header("📈 ROC Curves — All Models"), unsafe_allow_html=True)
    fig_roc = go.Figure()
    # Random baseline
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode='lines', name='Random Baseline',
        line=dict(dash='dash', color='rgba(255,255,255,0.15)', width=1.5),
    ))
    for name in MODEL_NAMES:
        fpr = roc_data[name]['fpr']
        tpr = roc_data[name]['tpr']
        auc_val = results[name]['ROC-AUC']
        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr, mode='lines',
            name=f"{name} (AUC={auc_val:.3f})",
            line=dict(color=MODEL_COLORS[name], width=2.5),
            fill='tonexty' if name == 'XGBoost' else None,
            fillcolor=f"rgba({','.join(str(int(MODEL_COLORS[name].lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.05)" if name == 'XGBoost' else None,
        ))
    fig_roc.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=40, l=40, r=20), height=420,
        xaxis=dict(title="False Positive Rate", gridcolor='rgba(255,255,255,0.04)',
                   zerolinecolor='rgba(255,255,255,0.06)'),
        yaxis=dict(title="True Positive Rate", gridcolor='rgba(255,255,255,0.04)',
                   zerolinecolor='rgba(255,255,255,0.06)'),
        legend=dict(x=0.4, y=0.05, bgcolor='rgba(0,0,0,0)', font=dict(size=11)),
        font=dict(color='#94a3b8'),
    )
    st.plotly_chart(fig_roc, width='stretch')

# ── Confusion Matrices ───────────────────────────────────────
with col_cm:
    st.markdown(section_header("🔢 Confusion Matrices"), unsafe_allow_html=True)
    tabs = st.tabs(MODEL_NAMES)
    for tab, name in zip(tabs, MODEL_NAMES):
        with tab:
            cm = np.array(cm_data[name])
            labels = ['Not Churned', 'Churned']
            fig_cm = go.Figure(data=go.Heatmap(
                z=cm, x=labels, y=labels,
                text=cm, texttemplate="%{text}",
                textfont=dict(size=20, color='white'),
                colorscale=[[0, '#0a0e27'], [0.5, MODEL_COLORS[name] + '80'],
                            [1, MODEL_COLORS[name]]],
                showscale=False, hoverinfo='skip',
            ))
            fig_cm.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=10, b=40, l=80, r=20), height=350,
                xaxis=dict(title="Predicted", side='bottom'),
                yaxis=dict(title="Actual", autorange='reversed'),
                font=dict(color='#94a3b8', size=13),
            )
            st.plotly_chart(fig_cm, width='stretch')

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Model Comparison ─────────────────────────────────────────
st.markdown(section_header("⚔️ Model Comparison"), unsafe_allow_html=True)

metrics_list = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC']
fig_comp = go.Figure()
for name in MODEL_NAMES:
    vals = [results[name][m] for m in metrics_list]
    fig_comp.add_trace(go.Bar(
        x=metrics_list, y=vals, name=name,
        marker=dict(color=MODEL_COLORS[name], line=dict(width=0)),
        text=[f"{v:.1%}" for v in vals],
        textposition='outside',
        textfont=dict(size=11),
    ))
fig_comp.update_layout(
    barmode='group',
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=30, b=40, l=40, r=20), height=400,
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)'),
    yaxis=dict(title="Score", gridcolor='rgba(255,255,255,0.04)',
               range=[0, 1.12], zerolinecolor='rgba(255,255,255,0.06)'),
    legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center',
                bgcolor='rgba(0,0,0,0)', font=dict(size=12)),
    font=dict(color='#94a3b8'),
)
st.plotly_chart(fig_comp, width='stretch')

st.markdown(glow_divider(), unsafe_allow_html=True)

# ── Cross-Validation ─────────────────────────────────────────
st.markdown(section_header("🔄 Cross-Validation Results (5-Fold Stratified)"), unsafe_allow_html=True)

cv_col1, cv_col2 = st.columns([1, 1])

with cv_col1:
    # CV comparison chart
    fig_cv = go.Figure()
    for name in MODEL_NAMES:
        test_auc = results[name]['ROC-AUC']
        cv_auc = cv_data[name]['mean']
        gap = abs(test_auc - cv_auc)
        fig_cv.add_trace(go.Bar(
            x=[name], y=[test_auc], name='Test ROC-AUC',
            marker=dict(color=MODEL_COLORS[name]),
            text=f"{test_auc:.3f}", textposition='outside',
            showlegend=(name == MODEL_NAMES[0]),
            legendgroup='test',
        ))
        fig_cv.add_trace(go.Bar(
            x=[name], y=[cv_auc], name='CV ROC-AUC',
            marker=dict(color=MODEL_COLORS[name], opacity=0.5),
            text=f"{cv_auc:.3f}", textposition='outside',
            showlegend=(name == MODEL_NAMES[0]),
            legendgroup='cv',
        ))
    fig_cv.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=40, l=40, r=20), height=350,
        yaxis=dict(title="ROC-AUC", gridcolor='rgba(255,255,255,0.04)',
                   range=[0, 1.12], zerolinecolor='rgba(255,255,255,0.06)'),
        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'),
        font=dict(color='#94a3b8'),
    )
    st.plotly_chart(fig_cv, width='stretch')

with cv_col2:
    # Stability analysis table
    st.markdown("""
    <div class="glass-card">
        <h4 style="color:#e2e8f0;margin-top:0;">Stability Analysis</h4>
        <table style="width:100%;border-collapse:collapse;margin-top:12px;">
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
                <th style="text-align:left;padding:10px;color:#64748b;font-size:0.8rem;">Model</th>
                <th style="text-align:center;padding:10px;color:#64748b;font-size:0.8rem;">Test AUC</th>
                <th style="text-align:center;padding:10px;color:#64748b;font-size:0.8rem;">CV AUC</th>
                <th style="text-align:center;padding:10px;color:#64748b;font-size:0.8rem;">Gap</th>
            </tr>
    """, unsafe_allow_html=True)

    rows_html = ""
    for name in MODEL_NAMES:
        test_v = results[name]['ROC-AUC']
        cv_v = cv_data[name]['mean']
        gap = abs(test_v - cv_v)
        gap_color = '#10b981' if gap < 0.03 else '#f59e0b' if gap < 0.05 else '#ef4444'
        rows_html += f"""
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:10px;color:#e2e8f0;font-weight:600;">{name}</td>
                <td style="text-align:center;padding:10px;color:{MODEL_COLORS[name]};">{test_v:.4f}</td>
                <td style="text-align:center;padding:10px;color:#94a3b8;">{cv_v:.4f}</td>
                <td style="text-align:center;padding:10px;color:{gap_color};font-weight:700;">{gap:.4f}</td>
            </tr>"""

    st.markdown(rows_html + "</table></div>", unsafe_allow_html=True)

    st.markdown("""<div style='margin-top:16px;padding:12px;border-radius:8px;
        background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.1);'>
        <span style='color:#00d4ff;font-weight:600;'>💡 Insight:</span>
        <span style='color:#94a3b8;font-size:0.85rem;'> A smaller gap between Test and CV scores
        indicates better generalisation. The model is less likely to overfit.</span>
    </div>""", unsafe_allow_html=True)
