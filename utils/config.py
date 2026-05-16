"""Centralized configuration constants."""

APP_TITLE = "RetainAI"
APP_ICON = "🔄"
APP_SUBTITLE = "Advanced Customer Retention & Intelligence Platform"

COLORS = {
    "primary": "#00d4ff",
    "secondary": "#7c3aed",
    "accent": "#f59e0b",
    "success": "#10b981",
    "danger": "#ef4444",
    "warning": "#f97316",
    "bg_dark": "#0a0e27",
    "bg_card": "#111633",
    "bg_glass": "rgba(255,255,255,0.04)",
    "border": "rgba(255,255,255,0.08)",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "critical": "#ef4444",
    "high": "#f97316",
    "moderate": "#f59e0b",
    "low": "#10b981",
}

SEGMENT_COLORS = {
    "Critical Risk": "#ef4444",
    "High Risk": "#f97316",
    "Moderate Risk": "#f59e0b",
    "Low Risk": "#10b981",
}

RETENTION_STRATEGIES = {
    'Critical Risk': (
        'Immediate personal outreach by a senior account manager. '
        'Offer a premium loyalty reward, exclusive discount (20-30%), '
        'and a dedicated support line. Schedule a satisfaction survey '
        'call within 48 hours.'
    ),
    'High Risk': (
        'Trigger an automated win-back email series with a time-limited '
        'coupon (10-15%). Invite to a loyalty programme and highlight new '
        'features/products matching their purchase history.'
    ),
    'Moderate Risk': (
        'Enrol in a re-engagement campaign: monthly newsletter with '
        'personalised product recommendations, and a small birthday '
        'or anniversary gift voucher.'
    ),
    'Low Risk': (
        'Maintain engagement via regular product updates and a referral '
        'programme incentive. Reward loyalty with early access to new '
        'products or features.'
    ),
}

MODEL_NAMES = ["Logistic Regression", "Random Forest", "XGBoost"]
MODEL_COLORS = {
    "Logistic Regression": "#00d4ff",
    "Random Forest": "#10b981",
    "XGBoost": "#7c3aed",
}
