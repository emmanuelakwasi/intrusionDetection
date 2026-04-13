
# 🛡️ Explainable Multi-Class Network Intrusion Detection System

> 

---

## What is This Project?

This project builds an AI-powered **Network Intrusion Detection System (IDS)** that:
- Classifies network traffic into 5 categories — Normal, DoS, Probe, R2L, and U2R
- Explains every prediction using SHAP (Shapley Additive Explanations)
- Reports a confidence score for every detection
- Compares three ML models — Decision Tree, Random Forest, and a Deep Neural Network
- Includes an interactive web application for live demonstration

Most existing IDS research uses binary classification (normal vs attack) and ignores rare attack types. This project directly addresses those gaps by combining multi-class classification, SMOTE balancing, and SHAP explainability in one unified pipeline — something no existing paper has fully achieved.

---

## Attack Categories Detected

| Class | Category | Examples | Risk Level |
|---|---|---|---|
| 0 | Normal | Legitimate traffic | None |
| 1 | DoS | neptune, smurf, back, teardrop | High |
| 2 | Probe | nmap, portsweep, satan, ipsweep | Medium |
| 3 | R2L | guess_passwd, ftp_write, imap | High |
| 4 | U2R | buffer_overflow, rootkit, perl | Critical |

---

## What Makes This Project Different

| Feature | This Project | Most Existing Work |
|---|---|---|
| Classification | Multi-class (5 categories) | Binary only |
| Class Balancing | SMOTE across all 5 classes | Not addressed |
| Explainability | Per-class SHAP analysis | Not included |
| Confidence Scores | Per-prediction confidence | Not reported |
| Models Compared | 3 models side by side | Usually 1 model |
| Web App | Interactive Streamlit demo | Not built |
| Cross-dataset Test | Tested on CICIDS2017 | Not attempted |

---

## Results

### Overall Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Decision Tree (Binary) | 79.02% | 96.29% | 65.68% | 78.09% |
| Random Forest (Multi-class) | 74.85% | 79.70% | 74.85% | 70.13% |
| **DNN (Multi-class)** | **75.62%** | **80.23%** | **75.62%** | **72.86%** |

### Per Class F1-Score — Random Forest vs DNN

| Class | Random Forest | DNN | Improvement |
|---|---|---|---|
| Normal | 0.78 | 0.80 | +2.6% |
| DoS | 0.85 | 0.84 | -1.2% |
| Probe | 0.78 | 0.66 | -15.4% |
| R2L | 0.01 | 0.27 | **+2,600%** |
| U2R | 0.05 | 0.15 | **+200%** |

### DNN Confidence Scores
- Average Confidence: **97.81%**
- Min Confidence: 38.12%
- Max Confidence: 100%

---

## SHAP Explainability Findings

SHAP analysis revealed class-specific feature importance profiles:

- **Normal & DoS** — primarily identified by `protocol_type` and `duration`
- **Probe** — identified by `duration` — scanning behavior creates distinct timing patterns
- **R2L** — identified by `service` type — these attacks target specific network services
- **U2R** — identified by `duration` — privilege escalation takes time and creates unique patterns

---

## Cross-Dataset Evaluation

The model was tested on CICIDS2017 (2.5M records) after training on NSL-KDD. Results showed significant performance degradation due to **domain shift** — the two datasets use fundamentally different feature representations. This confirms a well-documented open challenge in IDS research and motivates future work on domain adaptation techniques.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Primary language |
| pandas & numpy | Data manipulation |
| scikit-learn | Decision Tree, Random Forest, metrics |
| TensorFlow/Keras | Deep Neural Network |
| imbalanced-learn | SMOTE oversampling |
| SHAP | Explainability |
| matplotlib & seaborn | Visualization |
| Streamlit | Web application |
| Jupyter Notebook | Development environment |
| GitHub | Version control |

---

## Project Structure

```
ids_project/
│
├── app.py                  # Streamlit web application
│
├── data/                   # Dataset files (not uploaded)
│   ├── KDDTrain+.txt
│   ├── KDDTest+.txt
│   └── cicids2017_cleaned.csv
│
├── notebooks/
│   └── exploration.ipynb   # Full pipeline notebook
│
├── results/                # Saved models and charts
│   ├── dnn_model.keras
│   ├── scaler.pkl
│   ├── dnn_confusion_matrix.png
│   ├── rf_confusion_matrix.png
│   ├── dnn_training_history.png
│   ├── shap_global_importance.png
│   ├── shap_per_class.png
│   ├── model_comparison.png
│   ├── per_class_f1_comparison.png
│   └── cicids_confusion_matrix.png
│
└── README.md
```

---

## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/emmanuelakwasi/intrusionDetection.git
cd ml-intrusion-detection
```

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn tensorflow imbalanced-learn shap matplotlib seaborn streamlit jupyter
```

### 3. Download Datasets
- NSL-KDD: https://www.kaggle.com/datasets/hassan06/nslkdd
- CICIDS2017: https://www.kaggle.com/datasets/cicdataset/cicids2017
- Place both in the `data/` folder

### 4. Run the Notebook
```bash
jupyter notebook notebooks/exploration.ipynb
```

### 5. Run the Web App
```bash
streamlit run app.py
```

---

## Reference Papers

1. *Unravelling Complexity: Investigating the Effectiveness of SHAP Algorithm for Improving Explainability in Network Intrusion System Across Machine and Deep Learning Models*
2. *Enhancing Intrusion Detection for Minority Attack Classes: A SHAP-Based Feature Selection Approach with Deep Neural Networks*
3. *Explainable Deep Neural Network for a Reliable Intrusion Detection System with Shapley Additive Explanation Method*
4. *An Explainable Ensemble Deep Learning Approach for Intrusion Detection in Industrial Internet of Things*
5. *A Federated and Transfer Learning Framework for High-Accuracy, Explainable Intrusion Detection in Next-Generation Data Centers*
6. *Explainable AI-Driven Intrusion Detection System for DoS Attack Classification Using Deep Learning and Optimization Techniques*

---

##  Limitations & Future Work

- Cross-dataset generalization requires domain adaptation techniques
- Real-time SHAP computation is computationally expensive
- Model requires retraining as attack patterns evolve (concept drift)
- Federated learning needed for privacy-preserving distributed deployment
- Adversarial robustness testing not yet conducted

---

## Author

**Grambling State University**
EMMANUEL A. OPOKU
Submitted to N-SEA 2026 — National Symposium on Effective and Ethical AI

---

## If you found this project useful, please give it a star on GitHub!
