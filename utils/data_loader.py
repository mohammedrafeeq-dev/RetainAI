"""Data & model loading utilities with Streamlit caching."""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os

from pathlib import Path
BASE = Path.cwd()
MODELS_DIR = BASE / "models"

def safe_load(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error loading resource: {e}")
        st.stop()


@st.cache_resource(show_spinner=False)
def load_model(name: str):
    path = os.path.join(MODELS_DIR, f"{name.lower().replace(' ', '_')}.joblib")
    return joblib.load(path)


@st.cache_resource(show_spinner=False)
def load_all_models():
    from utils.config import MODEL_NAMES
    return {n: load_model(n) for n in MODEL_NAMES}


@st.cache_resource(show_spinner=False)
def load_scaler():
    return joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))


@st.cache_resource(show_spinner=False)
def load_encoder():
    return joblib.load(os.path.join(MODELS_DIR, "encoder.joblib"))


@st.cache_resource(show_spinner=False)
def load_kmeans():
    return joblib.load(os.path.join(MODELS_DIR, "kmeans.joblib"))


@st.cache_data(show_spinner=False)
def load_metrics():
    with open(os.path.join(MODELS_DIR, "metrics.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_data_info():
    with open(os.path.join(MODELS_DIR, "data_info.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_feature_names():
    with open(os.path.join(MODELS_DIR, "feature_names.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_categorical_columns():
    with open(os.path.join(MODELS_DIR, "categorical_columns.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_customer_profiles():
    return pd.read_csv(os.path.join(MODELS_DIR, "customer_profiles.csv"))


@st.cache_data(show_spinner=False)
def load_processed_data():
    return pd.read_csv(os.path.join(MODELS_DIR, "processed_data.csv"))


@st.cache_data(show_spinner=False)
def load_scaled_data():
    return np.load(os.path.join(MODELS_DIR, "data_scaled.npy"))


@st.cache_data(show_spinner=False)
def load_class_distribution():
    with open(os.path.join(MODELS_DIR, "class_distribution.json")) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def compute_similarity_matrix():
    from sklearn.metrics.pairwise import cosine_similarity
    scaled = load_scaled_data()
    return cosine_similarity(scaled)


def get_similar_customers(idx, top_n=5):
    sim_matrix = compute_similarity_matrix()
    scores = sim_matrix[idx]
    similar = scores.argsort()[::-1]
    similar = similar[similar != idx][:top_n]
    return pd.DataFrame({
        'customer_index': similar,
        'similarity_score': scores[similar].round(4)
    }).reset_index(drop=True)


def predict_single(input_dict: dict):
    """Predict churn for a single customer from raw feature dict."""
    encoder = load_encoder()
    scaler = load_scaler()
    cat_cols = load_categorical_columns()
    feat_names = load_feature_names()
    model = load_model("XGBoost")

    # Build numeric part
    num_data = {k: v for k, v in input_dict.items() if k not in cat_cols}

    # Build encoded categorical part
    cat_df = pd.DataFrame([{c: input_dict[c] for c in cat_cols}])
    cat_encoded = encoder.transform(cat_df)
    cat_feat_names = encoder.get_feature_names_out(cat_cols)

    # Combine
    row = pd.DataFrame([num_data])
    cat_encoded_df = pd.DataFrame(cat_encoded, columns=cat_feat_names, dtype=int)
    combined = pd.concat([row.reset_index(drop=True), cat_encoded_df], axis=1)
    combined = combined.reindex(columns=feat_names, fill_value=0)

    # Scale
    scaled = scaler.transform(combined)

    prob = model.predict_proba(scaled)[0][1]
    pred = int(prob >= 0.5)
    return prob, pred, scaled
