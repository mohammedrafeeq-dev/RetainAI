# 🔄 RetainAI

> An end-to-end Applied Machine Learning pipeline that predicts customer churn and generates personalised retention strategies using behavioural data.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-006600)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Results](#-key-results)
- [Pipeline Architecture](#-pipeline-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Methodology](#-methodology)
- [License](#-license)

---

## 🎯 Overview

Customer churn is one of the most critical challenges in business — **retaining existing customers is 5–7× cheaper** than acquiring new ones. 

**RetainAI** is an end-to-end Applied ML solution that:


1. **Predicts** which customers are likely to churn using an optimised XGBoost classifier
2. **Segments** customers into risk tiers using K-Means clustering
3. **Recommends** personalised retention strategies based on customer similarity and risk profile

### Problem Statement

Given a dataset of ~10,000 customers with 30 features (demographics, purchase behaviour, engagement metrics), build a model that accurately identifies at-risk customers while addressing severe class imbalance (~85/15 split).

---

## 📊 Key Results

| Metric | Value | Notes |
|--------|-------|-------|
| **ROC-AUC** | 0.91+ | XGBoost on test set |
| **Recall (Churn)** | 0.82 | Catches 82% of churning customers |
| **Stability Gap** | < 0.03 | Low gap between Test and CV scores |
| **Risk Segments** | 4 | Critical, High, Moderate, Low risk tiers |

### Why Not Just Accuracy?

The baseline model achieved **85% accuracy** — but this was misleading. With 85% non-churn data, a model predicting "no churn" for everyone gets 85% accuracy while catching **zero** actual churners. We used **ROC-AUC** and **Recall** as primary metrics.

---

## 🏗️ Pipeline Architecture

```
Raw Data (30 features)
    │
    ├── Data Preprocessing
    │       ├── Missing value imputation (mode/median)
    │       ├── Feature engineering (spend_per_visit, total_time_spent)
    │       └── Outlier treatment (IQR capping)
    │
    ├── Exploratory Data Analysis
    │       ├── Distribution analysis
    │       ├── Class imbalance assessment
    │       └── Correlation heatmap
    │
    ├── Feature Engineering
    │       ├── One-Hot Encoding (categorical)
    │       └── Standard Scaling (numerical)
    │
    ├── Modeling
    │       ├── SMOTE (train-only resampling)
    │       ├── 3-model comparison (LR, RF, XGBoost)
    │       ├── Stratified 5-Fold Cross-Validation
    │       ├── Combined Score & Stability Gap selection
    │       └── GridSearchCV hyperparameter tuning
    │
    └── Recommendation Engine
            ├── Cosine similarity matrix
            ├── K-Means customer segmentation (k=4)
            ├── Segment-to-strategy mapping
            └── Per-customer retention reports
```

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.10+ |
| **Data** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **ML Models** | scikit-learn, XGBoost |
| **Imbalance** | imbalanced-learn (SMOTE) |
| **Clustering** | scikit-learn (K-Means) |
| **Similarity** | scikit-learn (Cosine Similarity) |
| **Environment** | Google Colab / Jupyter Notebook |

---

## 📁 Project Structure

```
Applied ML/
├── Customer_Churn_Prediction.ipynb   # Main notebook (full pipeline)
├── data/
│   └── Sales_Marketing_Customer_Dataset.csv
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── LICENSE                            # MIT License
└── README.md                          # This file
```

---

## 🌐 Live Demo

Try it here: https://retainai.streamlit.app/

## 🚀 Quick Start


### Option 1: Google Colab (Recommended)

1. Upload `Customer_Churn_Prediction.ipynb` to [Google Colab](https://colab.research.google.com/)
2. Upload the dataset CSV to Colab's `data/` folder
3. Run all cells (`Runtime → Run all`)

### Option 2: Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Applied-ML.git
cd Applied-ML

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook Customer_Churn_Prediction.ipynb
```

---

## 🔬 Methodology

### 1. Class Imbalance Strategy

Applied **SMOTE** (Synthetic Minority Over-sampling Technique) **only on the training set** to avoid data leakage. Additionally, configured model-level imbalance handling:
- Logistic Regression: `class_weight='balanced'`
- Random Forest: `class_weight='balanced'`
- XGBoost: `scale_pos_weight` calibrated to imbalance ratio

### 2. Model Selection Framework

Instead of picking the model with the highest single metric, we developed a **dual-evaluation framework**:

| Criterion | Description |
|-----------|-------------|
| **Combined Score** | Average of Test ROC-AUC and CV ROC-AUC |
| **Stability Gap** | `|Test ROC-AUC − CV ROC-AUC|` — lower = more reliable |

The model with the **highest Combined Score** and **lowest Stability Gap** wins.

### 3. Recommendation Engine

A content-based system combining:
- **Cosine Similarity:** Finds the most behaviourally similar customers
- **K-Means Segmentation:** Groups customers into 4 risk tiers
- **Strategy Mapping:** Assigns retention interventions per segment (e.g., personal outreach for Critical Risk, automated campaigns for High Risk)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <i>Built as part of an Applied Machine Learning course project.</i>
</p>
