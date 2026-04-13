import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
import shap

# --- Page Config ---
st.set_page_config(
    page_title="Intrusion Detection System",
    page_icon="🛡️",
    layout="wide"
)

# --- Header ---
st.title(" Explainable Network Intrusion Detection System")
st.markdown("""
**Grambling State University | Undergraduate Research Project**

This system uses a Deep Neural Network trained on the NSL-KDD dataset to classify 
network traffic into 5 categories with SHAP-based explanations.
""")

st.divider()

# --- Class Names ---
class_names = {0: "Normal", 1: "DoS", 2: "Probe", 3: "R2L", 4: "U2R"}
class_colors = {
    "Normal": "green", "DoS": "red",
    "Probe": "orange", "R2L": "purple", "U2R": "darkred"
}
class_descriptions = {
    "Normal": "Legitimate network traffic — no threat detected.",
    "DoS": "Denial of Service attack — system is being flooded.",
    "Probe": "Network scanning — attacker mapping vulnerabilities.",
    "R2L": "Remote to Local — unauthorized remote access attempt.",
    "U2R": "User to Root — privilege escalation attempt detected."
}

# --- Feature Names ---
feature_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

# --- Load Model ---
@st.cache_resource
def load_artifacts():
    try:
        model = load_model("results/dnn_model.keras")
        with open("results/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

model, scaler = load_artifacts()

# --- Sidebar ---
st.sidebar.title("Input Network Features")
st.sidebar.markdown("Adjust the sliders to simulate network traffic:")

# Key features with sliders
duration = st.sidebar.slider("Duration (seconds)", 0, 60000, 0)
src_bytes = st.sidebar.slider("Source Bytes", 0, 100000, 181)
dst_bytes = st.sidebar.slider("Destination Bytes", 0, 100000, 5450)
logged_in = st.sidebar.selectbox("Logged In", [0, 1])
count = st.sidebar.slider("Count", 0, 512, 8)
srv_count = st.sidebar.slider("Srv Count", 0, 512, 8)
serror_rate = st.sidebar.slider("Error Rate", 0.0, 1.0, 0.0)
same_srv_rate = st.sidebar.slider("Same Service Rate", 0.0, 1.0, 1.0)
dst_host_count = st.sidebar.slider("Dst Host Count", 0, 255, 9)
dst_host_srv_count = st.sidebar.slider("Dst Host Srv Count", 0, 255, 9)

# --- Preset Attack Scenarios ---
st.sidebar.divider()
st.sidebar.markdown("### Quick Presets")
preset = st.sidebar.selectbox("Load Attack Scenario:", [
    "Custom",
    "Normal Traffic",
    "DoS Attack",
    "Probe Attack",
    "R2L Attack",
    "U2R Attack"
])


# --- Build Feature Vector ---
def build_feature_vector(duration, src_bytes, dst_bytes, logged_in,
                          count, srv_count, serror_rate, same_srv_rate,
                          dst_host_count, dst_host_srv_count):
    vec = np.zeros(41)
    vec[0] = duration
    vec[4] = src_bytes
    vec[5] = dst_bytes
    vec[11] = logged_in
    vec[22] = count
    vec[23] = srv_count
    vec[24] = serror_rate
    vec[28] = same_srv_rate
    vec[31] = dst_host_count
    vec[32] = dst_host_srv_count
    return vec

# --- Apply Presets ---
if preset == "Normal Traffic":
    duration, src_bytes, dst_bytes = 0, 181, 5450
    logged_in, count, srv_count = 1, 8, 8
    serror_rate, same_srv_rate = 0.0, 1.0
    dst_host_count, dst_host_srv_count = 9, 9
elif preset == "DoS Attack":
    duration, src_bytes, dst_bytes = 0, 0, 0
    logged_in, count, srv_count = 0, 511, 511
    serror_rate, same_srv_rate = 1.0, 1.0
    dst_host_count, dst_host_srv_count = 255, 255
elif preset == "Probe Attack":
    duration, src_bytes, dst_bytes = 0, 0, 0
    logged_in, count, srv_count = 0, 1, 1
    serror_rate, same_srv_rate = 0.0, 0.04
    dst_host_count, dst_host_srv_count = 255, 4
elif preset == "R2L Attack":
    duration, src_bytes, dst_bytes = 1, 250, 0
    logged_in, count, srv_count = 0, 1, 1
    serror_rate, same_srv_rate = 0.0, 1.0
    dst_host_count, dst_host_srv_count = 1, 1
elif preset == "U2R Attack":
    duration, src_bytes, dst_bytes = 0, 335, 0
    logged_in, count, srv_count = 1, 1, 1
    serror_rate, same_srv_rate = 0.0, 1.0
    dst_host_count, dst_host_srv_count = 1, 1

# --- Main Panel ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" Prediction")
    if model is not None:
        # Build and scale input
        input_vec = build_feature_vector(
            duration, src_bytes, dst_bytes, logged_in,
            count, srv_count, serror_rate, same_srv_rate,
            dst_host_count, dst_host_srv_count
        )
        input_scaled = scaler.transform(input_vec.reshape(1, -1))

        # Predict
        proba = model.predict(input_scaled, verbose=0)[0]
        pred_class = np.argmax(proba)
        confidence = proba[pred_class] * 100
        pred_name = class_names[pred_class]
        pred_color = class_colors[pred_name]

        # Display prediction
        color_map = {
        "Normal": "#4CAF50", "DoS": "#F44336",
        "Probe": "#FF9800", "R2L": "#9C27B0", "U2R": "#B71C1C"}
               
        st.markdown(f"### Predicted: <span style='color:{color_map[pred_name]}'>{pred_name}</span>",
            unsafe_allow_html=True)
        st.markdown(f"**Confidence: {confidence:.2f}%**")
        st.info(class_descriptions[pred_name])

        # Confidence bar chart
        st.subheader("Class Probabilities")
        prob_df = pd.DataFrame({
            "Class": list(class_names.values()),
            "Probability": proba * 100
        })
        st.bar_chart(prob_df.set_index("Class"))

with col2:
    st.subheader(" Project Results Summary")
    results_df = pd.DataFrame({
        "Model": ["Decision Tree", "Random Forest", "DNN"],
        "Accuracy": ["79.02%", "74.85%", "75.62%"],
        "Precision": ["96.29%", "79.70%", "80.23%"],
        "Recall": ["65.68%", "74.85%", "75.62%"],
        "F1-Score": ["78.09%", "70.13%", "72.86%"]
    })
    st.dataframe(results_df, use_container_width=True)

    st.subheader(" Per Class F1 — RF vs DNN")
    f1_df = pd.DataFrame({
        "Class": ["Normal", "DoS", "Probe", "R2L", "U2R"],
        "Random Forest": [0.78, 0.85, 0.78, 0.01, 0.05],
        "DNN": [0.80, 0.84, 0.66, 0.27, 0.15]
    })
    st.bar_chart(f1_df.set_index("Class"), use_container_width=True)

# --- Footer ---
st.divider()
st.markdown("""
**Project:** Explainable Multi-Class Network Intrusion Detection System  
**Dataset:** NSL-KDD (125,973 records)  
**Models:** Decision Tree, Random Forest, Deep Neural Network  
**Explainability:** SHAP (Shapley Additive Explanations)  
**Author:** Grambling State University — Undergraduate Research  
""")
